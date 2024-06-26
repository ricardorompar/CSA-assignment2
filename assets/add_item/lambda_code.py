import json
import boto3
import os

def handler(event, context):
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    #the body of the event contains the information that we want to put in the catalog:
    # new_item = json.loads(event['body'])
    new_item = event #TODO check if this works with the API gateway
    client.put_item(
        TableName=table_name,
        Item=new_item
    )

    return {
        'statusCode': 201,  #status code for resource creation
        'body': json.dumps({'message': 'Item added', 'item_id': new_item[id]})
    }

'''
Item should be in format:
{
    "id":{
        "S":"sylCSA2025"
    },
    "name":{
        "S":"Syllabus for Cloud Solutions Architecture 2025"
    },
    "type":{
        "S":"PDF"
    }
}
Acording to https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
'''