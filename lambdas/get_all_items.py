import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')

    try:
        response = client.scan(
            TableName=table_name
        )

        if response['Items']:
            return {
                'statusCode':200,
                'body':json.dumps({"count":f"{len(response['Items'])}", "items":response['Items']})
            }
        else:
            return {
                'statusCode':404,
                'body':json.dumps({"message":"No items found"})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(e)})
        }