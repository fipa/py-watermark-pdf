import boto3
from botocore.exceptions import NoCredentialsError

import generate

s3 = boto3.client('s3')
 
def lambda_handler(event, context):
    action = event["action"]

    if (action == "test"):
        return {
            "statusCode": 200,
            "body": {
                "message": "hello world"
            }
        }
    
    input_bucket = "bitacoraemocional"
    input_key = "pdfs/" + event["input_pdf"] + ".pdf"

    try:
        s3.download_file(input_bucket, input_key, '/tmp/input.pdf')
    except NoCredentialsError:
        return {
            "statusCode": 500,
            "body": {
                 "error": "Unable to access S3. Check AWS credentials to read."
            }
        }


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "hello world successful",
    }    

def my_lambda_handler(event, context):
    input_pdf = "pdfs/" + event["input_pdf"] + ".pdf"
    x_coordinate = 0
    y_coordinate = 0
    image_path = "imgs/footer.png"
    text = event["text"]
    output_pdf = "pdfs/generated/" + event["text"] + "_" + dynamic_text.replace(" ", "") + ".pdf"
    email = event["email"]
    last_page_to_merge = int(event["last_page"]) if "last_page" in event else None
    generate.create_pdf(input_pdf, output_pdf, text, email, image_path, x_coordinate, y_coordinate, last_page_to_merge)

    output_bucket = "bitacoraemocional"
    output_key = "pdfs/generated/" + event["input_pdf"] + "_" + event["text"].replace(" ", "") + ".pdf"

    try:
        s3.upload_file('/tmp/output.pdf', output_bucket, output_key)
    except NoCredentialsError:
        return {
            "statusCode": 500,
            "body": {
                "error": "Unable to upload to S3. Check AWS credentials to write."
            }
        }

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
