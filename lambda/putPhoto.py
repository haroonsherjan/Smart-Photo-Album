from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

host = 'search-elastic-yelp-final-hunkmkikl3kafz5esv3cu6v5tu.us-east-1.es.amazonaws.com'
region = 'us-east-1'  # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

rekognition = boto3.client('rekognition')
s3 = boto3.resource('s3')


def pushToES(object, labels):
    entryBody = {
        "bucket": object.bucket_name,
        "key": object.key,
        "label": labels
    }
    id = entryBody['bucket'] + " " + entryBody['key']
    index = "photos"
    type = "photo"
    if object.key == "621629_218395458289199_762026099_o.jpg":
        index = "test"
        type = "test"
    response = es.index(index=index, doc_type=type, id=id, body=entryBody)

    if es.indices.exists(index="test"):
        es.indices.delete(index="test")
        print("Deleted test")


def getRekognitionLabels(object):
    image = {
        'S3Object': {
            'Bucket': object.bucket_name,
            'Name': object.key
        }
    }
    return rekognition.detect_labels(Image=image, MinConfidence=0.75)


def lambda_handler(event, context):
    # print(event)
    for entry in event['Records']:
        bucket = entry['s3']['bucket']['name']
        objectKey = entry['s3']['object']['key']
        object = s3.Object(bucket, objectKey)
        metadata = object.metadata
        labels = []
        if metadata.length > 0:
            labels = metadata['customlabels'].split(', ')
        rekognitionLabels = getRekognitionLabels(object)
        for label in rekognitionLabels['Labels']:
            labels.append(label['Name'])
        print(labels)
        pushToES(object, labels)