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
    output_bucket = "bitacoraemocional"
    output_key = "pdfs/generated/" + event["input_pdf"] + "_" + event["text"].replace(" ", "") + ".pdf"

    try:
        s3.download_file(input_bucket, input_key, '/tmp/input.pdf')
    except NoCredentialsError:
        return {
            "statusCode": 500,
            "body": {
                "error": "Unable to access S3. Check AWS credentials to read."
            }
        }

    input_pdf = "/tmp/input.pdf"
    x_coordinate = 0
    y_coordinate = 0
    image_path = "imgs/footer.jpg"
    
    text = event["text"]
    output_pdf = "/tmp/output.pdf"
    email = event["email"]
    last_page_to_merge = int(event["last_page"]) if "last_page" in event else None
    generate.create_pdf(input_pdf, output_pdf, text, email, image_path, x_coordinate, y_coordinate, last_page_to_merge)

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