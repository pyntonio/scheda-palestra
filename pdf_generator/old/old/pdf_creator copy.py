import os
from markdown import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

async def genera_pdf_da_markdown(markdown_text: str, output_filename: str):
    """
    Genera un PDF da una stringa Markdown e lo salva con il nome specificato.
    """
    # Converte il markdown in HTML
    html_content = markdown(markdown_text)
    
    # Percorso completo per salvare il PDF
    pdf_path = os.path.join("static", "oroscopi", output_filename)
    
    # Log per verificare il percorso del file
    print(f"Generazione PDF: {pdf_path}")

    # Verifica che la cartella esista, altrimenti la crea
    if not os.path.exists(os.path.dirname(pdf_path)):
        os.makedirs(os.path.dirname(pdf_path))  # Crea la cartella se non esiste
        print(f"Cartella creata: {os.path.dirname(pdf_path)}")

    # Crea il file PDF
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Imposta il font e la dimensione del testo
    c.setFont("Helvetica", 12)

    # Aggiungi il contenuto del Markdown convertito come testo
    text_object = c.beginText(40, 750)  # Posizione iniziale
    text_object.setFont("Helvetica", 12)

    # Parso l'HTML in righe di testo per il PDF
    for line in html_content.splitlines():
        text_object.textLine(line.strip())

    # Disegna il testo sul canvas
    c.drawText(text_object)

    # Salva il PDF
    c.showPage()
    c.save()

    # Log per confermare il salvataggio del file
    if os.path.exists(pdf_path):
        print(f"PDF salvato in: {pdf_path}")
    else:
        print(f"Errore nel salvataggio del PDF.")

    return pdf_path  # Puoi anche loggare o fare altre azioni con il percorso
