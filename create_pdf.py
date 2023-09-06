import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

def create_pdf(input_pdf, output_pdf, text, image_path, x, y):
    new_output_pdf = output_pdf + "_2"
    img = build_image(image_path, 400, 75)
    overlay_frame(input_pdf + '.pdf', output_pdf, img, 410, 90, x, y)

    p = build_paragraph(text)
    overlay_frame(output_pdf + '.pdf', new_output_pdf, p, 150, 50, x + 210, y)


def overlay_frame(input_pdf, output_pdf, element, width, height, x, y):
    # Create a buffer to hold the modified PDF content
    buffer = BytesIO()

    # Open the existing PDF and create a canvas to add text
    existing_pdf = PdfFileReader(open(input_pdf, "rb"))
    output_pdf_writer = PdfFileWriter()

    # Create a new PDF with the same pages
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    pdf.pages = []

    frame = Frame(x, y, width, height, id="normal")
    # frame.showBoundary = True

    template = PageTemplate(id="test", frames=[frame])
    story = []
    story.append(element)
    # Build the PDF with the Story and PageTemplate
    pdf.addPageTemplates([template])
    pdf.build(story)

    # Merge the existing PDF with the new PDF (overlay)
    for i in range(existing_pdf.getNumPages()):
        page = existing_pdf.getPage(i)
        overlay_page = PdfFileReader(buffer).getPage(0)
        page.mergeTranslatedPage(overlay_page, x, y)
        output_pdf_writer.addPage(page)

    # Write the modified content to the output PDF file
    with open(output_pdf + ".pdf", "wb") as f:
        output_pdf_writer.write(f)


def build_paragraph(text):
    # Set the font and font size
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = 'Helvetica'
    style.fontSize = 15
    # Create a Paragraph with the dynamic text
    p = Paragraph(text, style)
    p.hAlign = 'RIGHT'
    p.vAlign = 'BOTTOM'
    return p

def build_image(image_path, width, height):
    img = Image(image_path, width, height)
    img.hAlign = 'LEFT'
    img.vAlign = 'BOTTOM'
    return img


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 create_pdf.py output_pdf dynamic_text")
    else:
        input_pdf = "pdfs/empty" # "pdfs/document.pdf"
        x_coordinate = 0
        y_coordinate = 10
        image_path = "imgs/footer.jpg"

        output_pdf = "pdfs/generated/" + sys.argv[1]
        dynamic_text = sys.argv[2]
        create_pdf(input_pdf, output_pdf, dynamic_text, image_path, x_coordinate, y_coordinate)