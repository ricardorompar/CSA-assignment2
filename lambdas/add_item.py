'''
DynamoDB Client put_item documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
'''

import json
import boto3
import os

def handler(event, context):
    '''
    Item should be in format:
    {
        "name":{"S":"Syllabus 2025"},
        "course":{"S":"Cloud Solutions Architecture"},
        "year":{"N":"2025"},
        "type":{"S":"PDF"}
    }
    '''
    table_name = os.environ['TABLE']
    client = boto3.client('dynamodb')
    
    try:
        #the body of the event contains the information that we want to put in the catalog:
        new_item = json.loads(event['body'])

        new_id = { #the id will be the combination between course and name. It will be unique because these two fields are the identifiers of each item
            "S":f"{new_item['name']['S']}@{new_item['course']['S']}"  #i define the id in the required format
        }
        new_item['id'] = new_id 
        # E.g: Syllabus@Cloud Solutions Architecture

        client.put_item(
            TableName=table_name,
            Item=new_item
        )

        return {
            'statusCode': 201,  #status code for resource creation
            'body': json.dumps({'message': 'Item added successfully', 'Item ID': new_item['id']['S']})
        }
    
    except KeyError:    #this error occurs when either name or course is not present
        if 'name' in new_item:
            return {
                'statusCode': 405,  #method not allowed
                'body': json.dumps({'message': 'Please specify the item course'})
            }
        elif 'course' in new_item:
            return {
                'statusCode': 405, 
                'body': json.dumps({'message': 'Please specify the item name'})
            }
        else:   #this would mean both name and course are absent
            return {
                'statusCode': 405, 
                'body': json.dumps({'message': 'Please specify the item name and course'})
            }
    
    except:
        return {
            'statusCode': 405,  #method not allowed
            'body': json.dumps({'message': 'Not allowed. Did you forget to specify the item data types?'})
        }

