import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    # item_id = event['pathParameters']['id'] #this is used to retrieve the id from the URL path
    # item_id = json.loads(event['body'])
    '''
    Assuming item_id in the format. The id is the composite between partition/sort keys -> name/course
    {
        'name':{
            'S':'Syllabus for the CSA class'
        },
        'course':{
            'S':'Cloud Solutions Architecture'
        }
    }
    '''
    # getting the query parameters:
    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['name']) and (
                event['queryStringParameters']['name'] is not None):
            item_name = event['queryStringParameters']['name']
    except KeyError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the name of the item'})
        }
    
    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['course']) and (
                event['queryStringParameters']['course'] is not None):
            item_course = event['queryStringParameters']['course']
    except KeyError:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the course of the item'})
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

    