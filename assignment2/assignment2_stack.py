'''
- Adding secondary indexes: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/GlobalSecondaryIndexProps.html
- Examples of API Gateway REST API: https://github.dev/awslabs/aws-lambda-powertools-python/blob/2236c89dd451495d6f634ccc0881957acf02903f/tests/e2e/event_handler/infrastructure.py#L72#L72
- Actions for DynamoDB IAM policies: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazondynamodb.html
'''

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as api,
    Duration,    #this is for configuring the lambda timeout
    RemovalPolicy,
    CfnOutput,
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

        #adding a course GSI to make faster queries:
        table.add_global_secondary_index(
            index_name="course_index",
            partition_key=dynamodb.Attribute(name="course", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING)
        )

        table.add_global_secondary_index(
            index_name="year_index",
            partition_key=dynamodb.Attribute(name="year", type=dynamodb.AttributeType.NUMBER),
            sort_key=dynamodb.Attribute(name="name", type=dynamodb.AttributeType.STRING)
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

        delete_item_by_id_lambda = lambda_.Function(
            self, "DeleteItemByIdFunction",
            handler='delete_item_by_id.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='delete_item_by_id',
            code=lambda_.Code.from_asset("./lambdas"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        get_items_by_course_lambda = lambda_.Function(
            self, "GetItemsByCourseFunction",
            handler='get_items_by_course.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='get_items_by_course',
            code=lambda_.Code.from_asset("./lambdas"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        get_items_by_year_lambda = lambda_.Function(
            self, "GetItemsByYearFunction",
            handler='get_items_by_year.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='get_items_by_year',
            code=lambda_.Code.from_asset("./lambdas"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        #Granting permissions to perform the different actions of the functions:
        table.grant(get_all_items_lambda, "dynamodb:Scan")
        table.grant(get_item_by_id_lambda, "dynamodb:GetItem")
        table.grant(get_items_by_course_lambda, "dynamodb:Query")
        table.grant(get_items_by_year_lambda, "dynamodb:Query")
        table.grant(add_item_lambda, "dynamodb:PutItem")
        table.grant(delete_item_by_id_lambda, "dynamodb:GetItem", "dynamodb:DeleteItem") #this function first checks that the item exists and then deletes


        '''
        3. API GATEWAY
        '''
        apigw = api.RestApi(
            self, "CatalogAPI"
        )
        #endpoint <base>/catalog_items
        catalog_items = apigw.root.add_resource("catalog_items")
        #GET all items:
        get_all_integration = api.LambdaIntegration(get_all_items_lambda)
        catalog_items.add_method("GET", get_all_integration)
        #PUT add new item:
        add_item_integration = api.LambdaIntegration(add_item_lambda)
        catalog_items.add_method("PUT", add_item_integration)

        #endpoint <base>/catalog_items/by_id
        by_id_resource = catalog_items.add_resource("by_id") #first add another resource 
        #GET by id
        get_by_id_integration = api.LambdaIntegration(get_item_by_id_lambda)
        by_id_resource.add_method("GET", get_by_id_integration) #then attach the lambda to it
        #DELETE by id
        delete_by_id_integration = api.LambdaIntegration(delete_item_by_id_lambda)
        by_id_resource.add_method("DELETE", delete_by_id_integration)

        #endpoint <base>/catalog_items/by_course
        by_course_resource = catalog_items.add_resource("by_course") #another resource 
        #GET by course
        get_by_course_integration = api.LambdaIntegration(get_items_by_course_lambda)
        by_course_resource.add_method("GET", get_by_course_integration) #then attach the lambda to it

        #endpoint <base>/catalog_items/by_year
        by_year_resource = catalog_items.add_resource("by_year") #another resource 
        #GET by year
        get_by_year_integration = api.LambdaIntegration(get_items_by_year_lambda)
        by_year_resource.add_method("GET", get_by_year_integration) #then attach the lambda to it


        #We'll need the URL for calling the API endpoints:
        CfnOutput(
            self, 'ApiEndpoint',
            value=apigw.url,
            key='ApiEndpoint'
        )
