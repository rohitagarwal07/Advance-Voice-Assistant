from fpdf import FPDF
import os
import datetime

def save_text_as_pdf(text, output_dir="pdfs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"speech_{datetime.datetime.now().strftime('%y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Times", size=12)

    pdf.multi_cell(0, 10, text)
    pdf.output(filepath)

    return filepath
