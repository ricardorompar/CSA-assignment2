'''
boto3 delete_item documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_item.html
'''

import json
import boto3
import os

def handler(event, context):
    '''
    This is almost the same function as get by id
    '''
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
        #i first check if exists:
        response = client.get_item(
            TableName=table_name,
            Key={
                'name':{
                    'S':item_name
                },
                'course':{
                    'S':item_course
                }
            }
        )

        if 'Item' in response:
            #In that case i can delete:
            client.delete_item(
                TableName=table_name,
                Key={
                    'name':{
                        'S':item_name
                    },
                    'course':{
                        'S':item_course
                    }
                }
            )

            return {
                'statusCode':200,
                'body':json.dumps({"message":f"Item {item_id} deleted successfully"})
            }
        
        else:    #this would mean the response object doesn't have the 'Item' field, aka not found:
            return {
                'statusCode':404,
                'body':json.dumps({"message":"Item not found. Cannot delete"})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(e)})
        }