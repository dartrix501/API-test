from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://testeos-chi.vercel.app/"
]

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

@app.post("/procesar")
def procesar(contacto: Contacto):
    return {"mensaje": f"Datos recibidos correctamente: {contacto.nombre}, {contacto.email}"}

if __name__ == "__main__":
    print("Hello world")