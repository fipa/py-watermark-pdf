import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

def create_pdf(input_pdf, output_pdf, text, image_path, x, y):
    # Create a buffer to hold the modified PDF content
    buffer = BytesIO()

    # Open the existing PDF and create a canvas to add text
    existing_pdf = PdfFileReader(open(input_pdf, "rb"))
    output_pdf_writer = PdfFileWriter()

    # Create a new PDF with the same pages
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    pdf.pages = []

    # Define a custom PageTemplate with a Frame
    frame = Frame(x, y, pdf.width, pdf.height / 10, id="normal")
    template = PageTemplate(id="test", frames=[frame])

    # Create a Story (list of flowable elements)
    story = []
    
    # Set the font and font size
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = 'Helvetica'
    style.fontSize = 10

    # Create a Paragraph with the dynamic text
    p = Paragraph(text, style)

    # Add the Paragraph to the Story
    story.append(p)

    # Add the image to the Story
    # img = Image(image_path, width=450, height=75)  # Adjust the width and height as needed
    # img.hAlign = 'LEFT'  # Horizontal alignment
    # img.vAlign = 'BOTTOM'  # Vertical alignment
    # story.append(img)

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
    with open(output_pdf, "wb") as f:
        output_pdf_writer.write(f)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 create_pdf.py output_pdf dynamic_text")
    else:
        input_pdf = "pdfs/document.pdf"
        x_coordinate = 0
        y_coordinate = 0
        # image_path = "imgs/footer.jpg"

        output_pdf = "pdfs/generated/" + sys.argv[1] + ".pdf"
        dynamic_text = sys.argv[2]
        create_pdf(input_pdf, output_pdf, dynamic_text, image_path, x_coordinate, y_coordinate)