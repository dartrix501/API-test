from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = FastAPI()

origins = ["https://testeos-chi.vercel.app"]

# Conexión a MongoDB Atlas
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["Test"]
coleccion = db["contactos"]

# Verificar conexión al iniciar
def verificar_conexion():
    try:
        client.admin.command('ping')
        print("✅ Conectado a MongoDB Atlas correctamente")
    except Exception as e:
        print("❌ Error al conectar a MongoDB Atlas:", e)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Contacto(BaseModel):
    nombre: str
    email: str

@app.on_event("startup")
def startup_event():
    verificar_conexion()

@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

@app.get("/test-db")
def test_db():
    try:
        doc = {"nombre": "Test", "email": "test@mail.com"}
        resultado = coleccion.insert_one(doc)
        return {"mensaje": "Inserción exitosa", "id": str(resultado.inserted_id)}
    except Exception as e:
        return {"mensaje": "Error al insertar en DB", "error": str(e)}

@app.post("/procesar")
def procesar(contacto: Contacto):
    mensaje = {"mensaje": f"Datos recibidos correctamente: {contacto.nombre}, {contacto.email}"}
    print(mensaje)
    # Guardar en la DB
    coleccion.insert_one({"nombre": contacto.nombre, "email": contacto.email})
    return mensaje

@app.get("/contactos")
def obtener_contactos():
    contactos = list(coleccion.find({}, {"_id": 0}))  # lista de documentos sin _id
    return contactos

print("Hello word")