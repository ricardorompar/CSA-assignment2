import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    item_id = event['pathParameters']['id'] #this is used to retrieve the id from the URL path. Same as get by id

    try:
        client.delete_item(
            TableName=table_name,
            #Uses a similar syntax to put_item:
            Key={
                'id': {
                    'S': item_id,
                }
            }
        )

        return {
            'statusCode':204,
            'body':json.dumps({'message':'Item deleted'})
        }
            
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(Exception)})
        }