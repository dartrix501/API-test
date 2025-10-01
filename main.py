# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Contacto(BaseModel):
    nombre: str
    email: str

@app.post("/procesar")
def procesar(contacto: Contacto):
    print(f"Nombre: {contacto.nombre}, Email: {contacto.email}")
    return {"mensaje": f"Datos recibidos: {contacto.nombre}, {contacto.email}"}
