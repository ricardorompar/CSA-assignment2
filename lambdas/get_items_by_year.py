'''
Very similar to get_items_by_course
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
        if (query_params) and (query_params['year']) and (query_params['year'] is not None):
            item_year = query_params['year']
    except:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Please specify the year of the item'})
        }

    try:
        response = client.query(
            TableName=table_name,
            IndexName='year_index', #here i use the index created for the table
            ExpressionAttributeValues={
                ':value': {
                    'N': item_year,
                },
            },
            ExpressionAttributeNames = {"#y":"year"},   #this is needed because apparently 'year' is a reserved keyword in dynamo so can't use it for queries
            KeyConditionExpression = '#y = :value'
            
        )

        if response['Items']: 
            return {
                'statusCode':200,
                'body':json.dumps({"count":f"{len(response['Items'])}", "Items":response['Items']})
            }
        else:
            return {
                'statusCode':404,
                'body':json.dumps({"message":f"No items found for year {item_year}"})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'cause':str(e)})
        }