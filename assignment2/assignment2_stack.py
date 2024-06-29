'''
- Adding local secondary indexes: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/LocalSecondaryIndexProps.html
- Examples of API Gateway REST API: https://github.dev/awslabs/aws-lambda-powertools-python/blob/2236c89dd451495d6f634ccc0881957acf02903f/tests/e2e/event_handler/infrastructure.py#L72#L72

'''

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as api,
    Duration,    #this is for configuring the lambda timeout
    RemovalPolicy,
    CfnOutput

)
from constructs import Construct

class Assignment2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # stack definition:

        '''
        1. DYNAMODB TABLE
        '''
        table = dynamodb.Table(
            self, "Table",
            table_name= "items_catalog",
            #Since the requirement is using name and course as id I use both parameters as partition and sort keys:
            partition_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="course", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY #force/ensure table destruction with CDK
        )

        #adding year as a secondary local index to make faster queries:
        table.add_local_secondary_index(
            index_name="year",
            sort_key=dynamodb.Attribute(name="course", type=dynamodb.AttributeType.STRING)
        )
        
        '''
        2. LAMBDA FUNCTIONS:
        '''
        get_all_items_lambda = lambda_.Function(
            self, "GetAllItemsFunction",    #specify the name, otherwise i get error "There is already a Construct with name"
            handler='get_all_items.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='get_all_items',
            code=lambda_.Code.from_asset("./lambdas"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        add_item_lambda = lambda_.Function(
            self, "AddItemFunction",
            handler='add_item.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='add_item',
            code=lambda_.Code.from_asset("./lambdas"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        get_item_by_id_lambda = lambda_.Function(
            self, "GetItemByIdFunction",
            handler='get_item_by_id.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='get_item_by_id',
            code=lambda_.Code.from_asset("./lambdas"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        #Granting permissions to perform the different actions of the functions:
        #TODO: fine-tune the permissions. These are too broad:
        table.grant_read_data(get_all_items_lambda)
        table.grant_read_data(get_item_by_id_lambda)
        table.grant_write_data(add_item_lambda)

        '''
        3. API GATEWAY
        '''
        apigw = api.RestApi(
            self, "CatalogAPI"
        )

        catalog_items = apigw.root.add_resource("catalog_items")

        get_all_integration = api.LambdaIntegration(get_all_items_lambda)
        catalog_items.add_method("GET", get_all_integration)

        add_item_integration = api.LambdaIntegration(add_item_lambda)
        catalog_items.add_method("PUT", add_item_integration)

        #For the get_by_id function I want to use path parameters so it's in the format items_catalog/<id>
        get_by_id_resource = catalog_items.add_resource('{id}') #first add another resource 
        get_by_id_integration = api.LambdaIntegration(get_item_by_id_lambda)
        get_by_id_resource.add_method("GET", get_by_id_integration) #then attach the lambda to it

        #DELETE:

        #We'll need the URL for calling the API endpoints:
        CfnOutput(
            self, 'ApiEndpoint',
            value=apigw.url,
            key='ApiEndpoint'
        )
