import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')

    # getting the query parameters i.e. ID  :
    try:
        query_params = event['queryStringParameters']
        if (query_params) and (query_params['id']) and (query_params['id'] is not None):
            item_id = query_params['id']
    except KeyError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the id of the item'})
        }

    try:
        #now i separate the name and course:
        item_name = item_id.split('#')[0]
        item_course = item_id.split('#')[1]
        
        response = client.get_item(
            TableName=table_name,
            #Uses a similar syntax to put_item:
            Key={
                'name':{
                    'S':item_name
                },
                'course':{
                    'S':item_course
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
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(e.message)})
        }

    