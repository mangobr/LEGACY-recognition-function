import boto3
import urllib
import os

ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

rekognition = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def detect_labels(bucket, key):
    rekognition_response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return rekognition_response

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    try:
        lambda_handler_response = detect_labels(bucket, key)
        return lambda_handler_response
    except Exception as RekoException:
        print(RekoException)
        raise RekoException("Error processing object {} from bucket {}. ".format(key, bucket))