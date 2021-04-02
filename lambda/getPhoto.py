import random
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json
import boto3

host = 'search-elastic-yelp-final-hunkmkikl3kafz5esv3cu6v5tu.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

lex = boto3.client('lex-runtime')

def get_photo(labels):
    must = []
    for label in labels:
        match = {"match": {"label": label}}
        must.append(match)
    searchBody = {
        "query": {
            "bool": {
                "must": must
            }
        }
    }
    response = es.search(index="photos", doc_type="photo", body=searchBody)
    hits = response['hits']['hits']
    ids = []
    for id in hits:
        ids.append(id['_source']['key'])
    return ids

def lambda_handler(event, context):
    message = event['queryStringParameters']['q'].replace('+', ' ')
    parsed_request = lex.post_text(
        botName='photoSearchBot',
        botAlias='Prod',
        userId='test',
        inputText = message
    )
    slots = parsed_request['slots']
    labels = set()
    for slot in slots:
        if(slots[slot]):
            labels.add(slots[slot])
    print(labels)
    ids = get_photo(labels)
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers':{"Access-Control-Allow-Origin": "*"},
        'body': json.dumps({
            'ids': ids
        })
    }
