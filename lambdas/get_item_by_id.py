import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    item_id = event['pathParameters']['id'] #this is used to retrieve the id from the URL path
    # getting the partition and sort keys:
    #I know that the ID is name#course, so:
    item_name = item_id.split('#')[0]
    item_course = item_id.split('#')[1]
    
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

    