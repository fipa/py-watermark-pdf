import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from io import BytesIO

def create_pdf(input_pdf, output_pdf, text, email, image_path, x, y):
    tmp_output_pdf = output_pdf.replace(".pdf", "_tmp.pdf")
    img_resize = 0.18
    width = 1506 * img_resize
    height = 93 * img_resize
    frame_resize = 3
    img = build_image(image_path, width, height)
    # overlay_frame(input_pdf, tmp_output_pdf, img, width + 6, height * frame_resize, x, y)

    p = build_paragraph(text, email, 'ShadowsIntoLight-Regular')
    #overlay_frame(tmp_output_pdf, output_pdf, p, 300, height * frame_resize * 0.8, x + 140, y + 3)
    new_overlay(input_pdf, output_pdf, img, p, width + 6, height * frame_resize, x, y)

def new_overlay(input_pdf_path, output_pdf, img, p, width, height, x, y):
    buffer = BytesIO()

    existing_pdf = PdfFileReader(open(input_pdf_path, "rb"))
    output_pdf_writer = PdfFileWriter()

    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    pdf.pages = []

    frame_width = width  # Divide the page width in half
    frame_img = Frame(x, y, frame_width, height, id="img_frame")
    frame_img.showBoundary = True
    frame_text = Frame(x + frame_width, y, frame_width, height, id="text_frame")
    frame_text.showBoundary = True

    available_space = frame_text.height - p.wrap(frame_text.width, frame_text.height)[1]  # Height of the text frame minus wrapped paragraph height
    spacer = Spacer(1, available_space) if available_space > 0 else Spacer(1, 1)  # Spacer to take up available space, but ensure it's at least 1 unit high

    template = PageTemplate(id="custom_template", frames=[frame_img, frame_text])
    story = [img, spacer, p]  # Use Spacer to separate image and text
    pdf.addPageTemplates([template])
    pdf.build(story)

    output_pdf_writer.addPage(existing_pdf.getPage(0))
    # for i in range(1, existing_pdf.getNumPages()):
    for i in range(1, 3):
        page = existing_pdf.getPage(i)
        overlay_page = PdfFileReader(buffer).getPage(0)
        page.mergeTranslatedPage(overlay_page, x, y)
        output_pdf_writer.addPage(page)
    output_pdf_writer.addPage(existing_pdf.getPage(existing_pdf.getNumPages() - 1))

    with open(output_pdf, "wb") as f:
        output_pdf_writer.write(f)

def overlay_frame(input_pdf, output_pdf, element, width, height, x, y):
    buffer = BytesIO()

    existing_pdf = PdfFileReader(open(input_pdf, "rb"))
    output_pdf_writer = PdfFileWriter()

    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    pdf.pages = []

    frame = Frame(x, y, width, height, id="normal")
    # frame.showBoundary = True

    template = PageTemplate(id="test", frames=[frame])  
    story = []
    story.append(element)
    pdf.addPageTemplates([template])
    pdf.build(story)

    output_pdf_writer.addPage(existing_pdf.getPage(0))
    for i in range(1, existing_pdf.getNumPages() - 1):
        page = existing_pdf.getPage(i)
        overlay_page =   PdfFileReader(buffer).getPage(0)
        page.mergeTranslatedPage(overlay_page, x, y)
        output_pdf_writer.addPage(page)
    output_pdf_writer.addPage(existing_pdf.getPage(existing_pdf.getNumPages() - 1))        

    with open(output_pdf, "wb") as f:
        output_pdf_writer.write(f)

def build_paragraph(text, email, font):
    pdfmetrics.registerFont(TTFont(font, 'fonts/' + font + '.ttf'))
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = font
    style.fontSize = 12

    p = Paragraph(text.upper() + " - " + email, style)
    p.hAlign = 'RIGHT'
    p.vAlign = 'BOTTOM'
    return p

def build_image(image_path, width, height):
    img = Image(image_path, width, height)
    img.hAlign = 'LEFT'
    img.vAlign = 'BOTTOM'
    return img


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 create_pdf.py file dynamic_text email")
    else:
        input_pdf = "pdfs/" + sys.argv[1] + ".pdf"
        x_coordinate = 0
        y_coordinate = 0
        image_path = "imgs/footer.png"

        dynamic_text = sys.argv[2]
        output_pdf = "pdfs/generated/" + sys.argv[1] + "_" + dynamic_text.replace(" ", "") + ".pdf"
        email = sys.argv[3]
        create_pdf(input_pdf, output_pdf, dynamic_text, email, image_path, x_coordinate, y_coordinate)