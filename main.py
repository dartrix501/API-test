from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os


app = FastAPI()

origins = ["https://testeos-chi.vercel.app"]


MONGO_URI = os.environ.get("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["Test"]
coleccion = db["contactos"]



async def verificar_conexion():
    try:
        await client.admin.command('ping')
        print("✅ Conectado a MongoDB Atlas correctamente")
    except Exception as e:
        print("❌ Error al conectar a MongoDB Atlas:", e)



# Permitir peticiones desde cualquier origen (Vercel incluido)
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


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}

@app.post("/procesar")
def procesar(contacto: Contacto):
    mensaje = {"mensaje": f"Datos recibidos correctamente: {contacto.nombre}, {contacto.email}"}
    print(mensaje)
    return mensaje

@app.get("/contactos")
async def obtener_contactos():
    contactos = await coleccion.find().to_list(100)
    return contactos

print("Hello world")