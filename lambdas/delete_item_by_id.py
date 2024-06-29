import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    # item_id = event['pathParameters']['id'] #this is used to retrieve the id from the URL path. Same as get by id
    item_id = json.loads(event['body'])
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
    try:
        client.delete_item(
            TableName=table_name,
            #Uses a similar syntax to put_item:
            Key=item_id
            # Key={
            #     'id': {
            #         'S': item_id,
            #     }
            # }
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