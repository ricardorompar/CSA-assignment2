'''
boto3 query documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/query.html
Querying with indexes: https://stackoverflow.com/questions/35758924/how-do-we-query-on-a-secondary-index-of-dynamodb-using-boto3
'''

import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')

    # getting the query parameters i.e. course  :
    try:
        query_params = event['queryStringParameters']
        if (query_params) and (query_params['course']) and (query_params['course'] is not None):
            item_course = query_params['course']
    except:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the course of the item'})
        }

    try:
        response = client.query(
            TableName=table_name,
            IndexName='course_index', #here i use the index created for the table
            ExpressionAttributeValues={
                ':value': {
                    'S': item_course,
                },
            },
            KeyConditionExpression = 'course = :value'
        )

        if response['Items']:
            return {
                'statusCode':200,
                'body':json.dumps({"count":f"{len(response['Items'])}", "Items":response['Items']})
            }
        else:
            return {
                'statusCode':404,
                'body':json.dumps({"message":f"No items found for course {item_course}"})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(e)})
        }

    