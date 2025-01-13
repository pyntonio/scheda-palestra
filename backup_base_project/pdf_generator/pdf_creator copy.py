from markdown import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

import os
from html import unescape

# Funzione per pulire e convertire il contenuto HTML
def clean_and_format_html(html_content):
    """
    Pulisce e formatta il contenuto HTML in un formato leggibile per il PDF.
    """
    html_content = unescape(html_content)
    
    # Gestione delle intestazioni (h1, h2, h3)
    html_content = html_content.replace('<h1>', '<p style="font-size:18px; font-weight: bold;">') \
                               .replace('</h1>', '</p>')
    html_content = html_content.replace('<h2>', '<p style="font-size:16px; font-weight: bold;">') \
                               .replace('</h2>', '</p>')
    html_content = html_content.replace('<h3>', '<p style="font-size:14px; font-weight: bold;">') \
                               .replace('</h3>', '</p>')
    
    # Gestione dei paragrafi (p)
    html_content = html_content.replace('<p>', '<p style="font-size:12px; line-height: 1.5;">') \
                               .replace('</p>', '</p>')
    
    # Gestione del testo in grassetto e corsivo
    html_content = html_content.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html_content = html_content.replace('<em>', '<i>').replace('</em>', '</i>')
    
    return html_content

# Funzione per aggiungere il testo al PDF con wrapping automatico
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
        
        # Pulisce e formatta il contenuto HTML
        formatted_text = clean_and_format_html(html_content)
        print("HTML formattato.")

        # Percorso completo per salvare il PDF
        pdf_path = os.path.join("static", "oroscopi", output_filename)
        print(f"Percorso del PDF: {pdf_path}")
        
        # Verifica che la cartella esista, altrimenti la crea
        output_dir = os.path.dirname(pdf_path)
        if not os.path.exists(output_dir):
            print(f"Cartella non trovata. Creazione cartella {output_dir}.")
            os.makedirs(output_dir)

        # Crea il file PDF con reportlab
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Aggiunge il testo con wrapping
        y_position = 750
        y_position = add_wrapped_text(c, formatted_text, 40, y_position)
        
        # Salva il PDF
        c.showPage()
        c.save()
        print(f"PDF salvato in: {pdf_path}")

        return pdf_path

    except Exception as e:
        print(f"Errore durante la generazione del PDF: {str(e)}")
        return {"error": "Errore durante la generazione del PDF", "details": str(e)}
