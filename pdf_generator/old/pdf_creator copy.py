import os
from markdown import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from html import unescape  # Cambiato HTMLParser con html.unescape

# Funzione per pulire i tag HTML
def clean_html(html_content):
    """
    Pulisce il contenuto HTML dai tag non necessari
    """
    return unescape(html_content)

# Funzione per aggiungere il testo al PDF con il wrapping automatico
def add_wrapped_text(c, text, x, y, font="Helvetica", size=12, max_width=550):
    """
    Aggiunge testo al PDF con wrapping automatico.
    """
    c.setFont(font, size)
    lines = text.splitlines()
    for line in lines:
        wrapped_lines = wrap_text(line, max_width, c)
        for wrapped_line in wrapped_lines:
            c.drawString(x, y, wrapped_line)
            y -= 14  # Spazio tra le linee
            if y < 50:
                c.showPage()  # Aggiungi una nuova pagina se il testo è troppo lungo
                c.setFont(font, size)
                y = 750  # Ripristina la posizione verticale

    return y  # Restituisce la posizione finale del cursore

# Funzione per eseguire il wrapping del testo per adattarlo alla larghezza massima
def wrap_text(text, max_width, c, font="Helvetica", size=12):
    """
    Esegue il wrapping del testo per adattarlo alla larghezza massima.
    """
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        width = c.stringWidth(test_line, font, size)
        if width < max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())  # Aggiungi l'ultima linea
    return lines

# Funzione principale per generare il PDF da Markdown
async def genera_pdf_da_markdown(markdown_text: str, output_filename: str):
    """
    Genera un PDF da una stringa Markdown e lo salva con il nome specificato.
    """
    try:
        print("Inizio generazione PDF...")

        # Converte il markdown in HTML
        html_content = markdown(markdown_text)
        print("Markdown convertito in HTML.")
        
        # Pulisce il contenuto HTML
        cleaned_text = clean_html(html_content)
        print("HTML pulito.")

        # Percorso completo per salvare il PDF
        # Verifica che il percorso di salvataggio sia corretto e non venga duplicato
        pdf_path = os.path.join("static", "oroscopi", output_filename)
        print(f"Percorso del PDF: {pdf_path}")
        
        # Verifica che la cartella esista, altrimenti la crea
        output_dir = os.path.dirname(pdf_path)
        if not os.path.exists(output_dir):
            print(f"Cartella non trovata. Creazione cartella {output_dir}.")
            os.makedirs(output_dir)

        # Crea il file PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Imposta il font e la dimensione del testo
        c.setFont("Helvetica", 12)
        
        # Aggiungi il testo con wrapping
        y_position = 750
        y_position = add_wrapped_text(c, cleaned_text, 40, y_position)
        
        # Salva il PDF
        c.showPage()
        c.save()
        print(f"PDF salvato in: {pdf_path}")

        return pdf_path

    except Exception as e:
        print(f"Errore durante la generazione del PDF: {str(e)}")
        return {"error": "Errore durante la generazione del PDF", "details": str(e)}
