import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from io import BytesIO

MILIMITERS_TO_POINTS = 72 / 25.4

def create_pdf(input_pdf, output_pdf, text, email, image_path, x, y, last_page_to_merge = None):
    print("create_pdf: {}, {}, {}, {}, {}, {}, {}, {}".format(input_pdf, output_pdf, text, email, image_path, x, y, last_page_to_merge))
    img_resize = 0.18
    width = 1506 * img_resize
    height = 93 * img_resize
    frame_resize = 2
    img = build_image(image_path, width, height)

    p = build_paragraph(text, email, 'ShadowsIntoLight-Regular')
    overlay(input_pdf, output_pdf, img, p, height * frame_resize, x, y, last_page_to_merge)

def overlay(input_pdf_path, output_pdf, img, p, height, x, y, last_page_to_merge):
    buffer = BytesIO()

    existing_pdf = PdfFileReader(open(input_pdf_path, "rb"))
    output_pdf_writer = PdfFileWriter()

    page_width = 283 * MILIMITERS_TO_POINTS
    page_height = 216 * MILIMITERS_TO_POINTS

    pdf = SimpleDocTemplate(buffer, pagesize=(page_width, page_height))
    pdf.pages = []

    frame_width = pdf.width * 0.45  # Divide the page width in half
    frame_img = Frame(x, y, frame_width, height, id="img_frame")
    frame_text = Frame(x + frame_width, y, frame_width, height, id="text_frame")
    # frame_img.showBoundary = True
    # frame_text.showBoundary = True

    template = PageTemplate(id="custom_template", frames=[frame_img, frame_text])
    story = [img, p]
    pdf.addPageTemplates([template])
    pdf.build(story)

    overlay_page = PdfFileReader(buffer).getPage(0)
    overlay_page.compressContentStreams()

    output_pdf_writer.addPage(existing_pdf.getPage(0))
    last_page = min(last_page_to_merge if last_page_to_merge != None else existing_pdf.getNumPages() - 1, existing_pdf.getNumPages() - 1)
    print("merging {} pages".format(last_page))
    for i in range(1, last_page):
        page = existing_pdf.getPage(i)
        page.mergeTranslatedPage(overlay_page, x, y)
        page.compressContentStreams()
        output_pdf_writer.addPage(page)
        if i%5 == 0 : print("merged {}/{}".format(i, last_page))
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

def lambda_handler(event, context):
    action = event["action"]

    if (action == "test"):
        return {
            "statusCode": 200,
            "body": {
                "message": "hello world"
            }
        }
    
    input_pdf = "pdfs/" + event["input_pdf"] + ".pdf"
    x_coordinate = 0
    y_coordinate = 0
    image_path = "imgs/footer.jpg"
    
    text = event["text"]
    output_pdf = "pdfs/generated/" + event["input_pdf"] + "_" + text.replace(" ", "") + ".pdf"
    email = event["email"]
    last_page_to_merge = int(event["last_page"]) if "last_page" in event else None
    create_pdf(input_pdf, output_pdf, text, email, image_path, x_coordinate, y_coordinate, last_page_to_merge)

    return {
        "statusCode": 200,
        "body": {
            "message": "PDF generation successful",
            "input_pdf": input_pdf,
            "text": text,
            "output_pdf": output_pdf,
            "email": email
        },
    }

if __name__ == "__main__":
    if (len(sys.argv) != 4 and len(sys.argv) != 5):
        print("Usage: python3 create_pdf.py file text email (optional) last_page_to_merge")
    else:
        input_pdf = "pdfs/" + sys.argv[1] + ".pdf"
        x_coordinate = 0
        y_coordinate = 0
        image_path = "imgs/footer.jpg"

        text = sys.argv[2]
        output_pdf = "pdfs/generated/" + sys.argv[1] + "_" + text.replace(" ", "") + ".pdf"
        email = sys.argv[3]
        last_page_to_merge = int(sys.argv[4]) if len(sys.argv) == 5 else None
        create_pdf(input_pdf, output_pdf, text, email, image_path, x_coordinate, y_coordinate, last_page_to_merge)
        