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
    except:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the id of the item'})
        }

    try:
        #now i separate the name and course:
        item_name = item_id.split('@')[0]
        item_course = item_id.split('@')[1]
    except IndexError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the id of the item in the format name@course'})
        }

    try:
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

        try: #tryception
            return {
                'statusCode':200,
                'body':json.dumps(response['Item'])
            }
        except KeyError:    #this would mean the response object doesn't have the 'Item' field, aka not found:
            return {
                'statusCode':404,
                'body':json.dumps({"message":"Item not found"})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(e)})
        }

    