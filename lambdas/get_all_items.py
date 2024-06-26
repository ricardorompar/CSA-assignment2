import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')

    response = client.scan(
        TableName=table_name
    )

    return {
        'statusCode':200,
        'body':json.dumps(response['Items'])
    }