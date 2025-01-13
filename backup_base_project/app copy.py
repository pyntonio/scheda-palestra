from fastapi import FastAPI
from oroscope.oroscope import genera_oroscopo
from models import OroscopoRequest  # Importa il modello che hai creato

app = FastAPI()

# Endpoint per generare l'oroscopo
@app.post("/oroscopo")
async def oroscopo(data: OroscopoRequest):  # Usa il modello come parametro
    return await genera_oroscopo(data.dict())  # Converte il modello in un dizionario per passarlo a genera_oroscopo
