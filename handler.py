import boto3
import urllib

rekognition = boto3.client('rekognition')

def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response
    
# def detect_custom_labels(bucket, key):    
#     response = rekognition.detect_custom_labels(ProjectVersionArn='arn:aws:rekognition:us-east-1:018413147376:project/carne-moida/version/carne-moida.2020-10-09T00.57.23/1602215843140',Image={'S3Object': {'Bucket': bucket,'Name': key,}},MaxResults=10,MinConfidence=0.5)
#     return response

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = detect_labels(bucket, key)
        return response
    except Exception as RekoException:
        print(RekoException)
        raise RekoException("Error processing object {} from bucket {}. ".format(key, bucket)) 
        
