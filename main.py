import sys

import generate

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
        generate.create_pdf(input_pdf, output_pdf, text, email, image_path, x_coordinate, y_coordinate, last_page_to_merge)
        