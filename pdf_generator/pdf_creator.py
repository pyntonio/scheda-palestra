import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from markdown import markdown
import re

# Funzione per rimuovere i tag HTML dal contenuto
def remove_html_tags(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)

# Funzione per aggiungere i paragrafi al PDF con ritorni a capo dinamici e formattazione grassetto
def add_paragraphs_to_pdf(c, text, font_size, y_position, title=False):
    """
    Aggiunge i paragrafi al PDF. Gestisce titoli e testo ordinario, applicando il grassetto dove necessario.
    :param c: oggetto canvas di reportlab
    :param text: testo da aggiungere
    :param font_size: dimensione del font
    :param y_position: posizione verticale
    :param title: se True, il testo è trattato come titolo (formattato in modo diverso)
    :return: nuova posizione verticale
    """
    width, height = letter  # otteniamo le dimensioni della pagina
    margin = 40  # margine sinistro
    max_width = width - 2 * margin  # larghezza massima del testo (senza margini)

    # Imposta il font (titoli in grassetto, testo normale in normale)
    if title:
        c.setFont("Helvetica-Bold", font_size + 2)
    else:
        c.setFont("Helvetica", font_size)
    
    # Dividi il testo in righe che non superano la larghezza massima
    lines = split_text_to_fit(c, text, max_width)
    
    # Aggiungi le righe al PDF
    for line in lines:
        c.drawString(margin, y_position, line)
        y_position -= font_size * 1.5  # Spaziatura tra le righe
        
        # Se la posizione è troppo bassa, aggiungi una nuova pagina
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", font_size)
            y_position = 750  # Reset della posizione verticale
    
    return y_position

# Funzione per dividere il testo in righe che si adattano alla larghezza massima
def split_text_to_fit(c, text, max_width):
    """
    Divide il testo in righe che si adattano alla larghezza massima consentita.
    :param text: il testo da dividere
    :param max_width: la larghezza massima in cui il testo deve stare
    :param c: oggetto canvas per calcolare la lunghezza del testo
    :return: lista di righe che si adattano alla larghezza
    """
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        # Prova ad aggiungere la parola alla riga corrente
        test_line = current_line + ' ' + word if current_line else word
        width = c.stringWidth(test_line, "Helvetica", 12)
        
        # Se la riga supera la larghezza, inizia una nuova riga
        if width > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    
    # Aggiungi l'ultima riga
    if current_line:
        lines.append(current_line)
    
    return lines

# Funzione per analizzare il Markdown e separare i titoli e il testo grassetto
def process_markdown(markdown_text):
    """
    Converte il Markdown in testo puro, separando i titoli e i grassetti.
    :param markdown_text: testo in Markdown
    :return: lista di tuples (testo, tipo) dove tipo è 'title', 'bold' o 'text'
    """
    lines = markdown_text.splitlines()
    result = []
    
    for line in lines:
        if line.startswith("**"):  # Grassetto (rilevato dagli asterischi)
            result.append((line.strip('*'), "bold"))
        elif line.startswith("#"):  # Titoli
            result.append((line.lstrip("# ").strip(), "title"))
        else:  # Testo normale
            result.append((line.strip(), "text"))
    
    return result

# Funzione principale per generare il PDF da Markdown
async def genera_pdf_da_markdown(markdown_text: str, output_filename: str):
    try:
        if not isinstance(markdown_text, str):
            raise ValueError("Il parametro 'markdown_text' deve essere una stringa.")

        print("Inizio generazione PDF...")

        html_content = markdown(markdown_text)
        print("Markdown convertito in HTML.")
        
        clean_text = remove_html_tags(html_content)
        print("HTML pulito e tag rimossi.")

        content = process_markdown(markdown_text)

        pdf_path = os.path.join("static", "oroscopi", output_filename)
        print(f"Percorso del PDF: {pdf_path}")
        
        output_dir = os.path.dirname(pdf_path)
        if not os.path.exists(output_dir):
            print(f"Cartella non trovata. Creazione cartella {output_dir}.")
            os.makedirs(output_dir)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        y_position = 750
        for line, line_type in content:
            if line_type == "title":
                y_position = add_paragraphs_to_pdf(c, line, 14, y_position, title=True)
            elif line_type == "bold":
                # Aggiungi il testo in grassetto
                y_position = add_paragraphs_to_pdf(c, line, 12, y_position, title=False)
            else:
                y_position = add_paragraphs_to_pdf(c, line, 12, y_position, title=False)
        
        c.showPage()
        c.save()
        print(f"PDF salvato in: {pdf_path}")

        return pdf_path

    except Exception as e:
        print(f"Errore durante la generazione del PDF: {str(e)}")
        return {"error": "Errore durante la generazione del PDF", "details": str(e)}
