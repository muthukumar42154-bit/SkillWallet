import os
import time
from fpdf import FPDF

def clean_text_for_pdf(text: str) -> str:
    """PDF-ல் ஆதரிக்கப்படாத Unicode குறியீடுகளை ASCII எழுத்துக்களாக மாற்றும்."""
    if not text:
        return ""
    replacements = {
        '\u2014': '-',      # em-dash
        '\u2013': '-',      # en-dash
        '\u2018': "'",      # left single quote
        '\u2019': "'",      # right single quote
        '\u201c': '"',      # left double quote
        '\u201d': '"',      # right double quote
        '\u2026': '...',    # ellipsis
        '\u00a0': ' ',      # non-breaking space
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    # latin-1 ஆதரிக்காத பிற குறியீடுகளைப் பிழையின்றி நீக்குதல்
    return text.encode('latin-1', 'ignore').decode('latin-1')

def save_pdf(layout: list) -> str:
    output_dir = os.path.join("static", "pdf")
    os.makedirs(output_dir, exist_ok=True)
    pdf_filename = f"comic_{int(time.time())}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    for idx, panel in enumerate(layout):
        pdf.add_page()
        
        # தலைப்பு
        pdf.set_font("Helvetica", style="B", size=16)
        title = clean_text_for_pdf(f"Panel {idx + 1}: {panel.get('title', 'Scene')}")
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.ln(5)

        # படம் சேர்த்தல்
        image_path = panel.get('image', '').lstrip('/')
        if os.path.exists(image_path):
            try:
                # மையத்தில் படம் அமைத்தல் (அகலம்: 150mm)
                pdf.image(image_path, x=30, y=pdf.get_y(), w=150)
                pdf.ln(115)  # படத்தின் உயரத்திற்கு ஏற்ப இடைவெளி
            except Exception as img_err:
                print(f"PDF Image render error: {img_err}")
                pdf.ln(10)
        else:
            pdf.ln(10)

        # கதை மற்றும் வசனங்கள்
        pdf.set_font("Helvetica", size=11)
        cleaned_body = clean_text_for_pdf(panel.get('text', ''))
        pdf.multi_cell(0, 7, cleaned_body)

    pdf.output(pdf_path)
    return "/" + pdf_path.replace("\\", "/")