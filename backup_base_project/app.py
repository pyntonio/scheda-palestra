from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from oroscope.oroscope import genera_oroscopo
import os
from models import OroscopoRequest  # Importa il modello che hai creato
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sostituisci con il dominio del frontend in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint per generare l'oroscopo
@app.post("/genera_oroscopo/") 
async def genera_oroscopo_api(data: dict, background_tasks: BackgroundTasks):
    try:
        # Genera l'oroscopo e il PDF tramite la funzione principale
        result = await genera_oroscopo(data)  # Genera l'oroscopo e il PDF
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Estrai il nome del PDF dal percorso restituito
        pdf_filename = result.get("pdf_path").split("/")[-1]  # Estrai il nome del PDF dal path
        
        # Recupera il testo dell'oroscopo (contenuto in markdown)
        oroscopo_text = result.get("testo", "")  # Prendi il testo in markdown

        # Restituisci il risultato
        return {
            "message": "Oroscopo generato e PDF in fase di creazione.",
            "oroscopo_text": oroscopo_text,  # Restituisci anche il testo dell'oroscopo
            "pdf_filename": pdf_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint per scaricare il PDF generato
@app.get("/download_oroscopo/{pdf_filename}")
async def download_oroscopo(pdf_filename: str):
    percorso_pdf = os.path.join("static", "oroscopi", pdf_filename)
    
    # Verifica che il PDF esista
    if not os.path.exists(percorso_pdf):
        raise HTTPException(status_code=404, detail="PDF non trovato")
    
    # Restituisci il PDF come risposta
    return FileResponse(percorso_pdf, media_type="application/pdf", filename=pdf_filename)
