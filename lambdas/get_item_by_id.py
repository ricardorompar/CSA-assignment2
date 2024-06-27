import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    item_id = event['pathParameters']['id'] #this is used to retrieve the id from the URL path

    try:
        response = client.get_item(
            TableName=table_name,
            #Uses a similar syntax to put_item:
            Key={
                'id': {
                    'S': item_id,
                }
            }
        )

        if response['Item']:   #if it was found. In get_item, the response JSON includes an 'Item' object, as opposed to the 'Items' from scan 
            return {
                'statusCode':200,
                'body':json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode':404,
                'body':json.dumps({"message":"Item not found"})
            }
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(Exception)})
        }

    