import generate

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
    generate.create_pdf(input_pdf, output_pdf, text, email, image_path, x_coordinate, y_coordinate, last_page_to_merge)

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