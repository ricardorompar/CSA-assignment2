from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway,
    Duration,    #this is for configuring the lambda timeout
    RemovalPolicy,
    CfnOutput

)
from constructs import Construct

class Assignment2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #1. DYNAMODB TABLE
        table = dynamodb.Table(
            self, "Table",
            table_name= "items_catalog",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY #force/ensure table destruction with CDK
        )
        
        #2. LAMBDA FUNCTIONS:
        get_all_items_lambda = lambda_.Function(
            self, "GetAllItemsFunction",    #specify the name, otherwise i get error "There is already a Construct with name"
            handler='lambda_code.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='get_all_items',
            code=lambda_.Code.from_asset("./assets/get_all_items"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        add_item_lambda = lambda_.Function(
            self, "AddItemFunction",
            handler='lambda_code.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='add_item',
            code=lambda_.Code.from_asset("./assets/add_item"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        get_item_ID_lambda = lambda_.Function(
            self, "GetItemIDFunction",
            handler='lambda_code.handler',
            timeout=Duration.minutes(1),    #1 minute timeout
            runtime=lambda_.Runtime.PYTHON_3_12,
            function_name='get_item_by_ID',
            code=lambda_.Code.from_asset("./assets/get_item_by_ID"),
            #need the table name to use it in the function:
            environment={
                'TABLE':table.table_name
            }
        )

        #Granting permissions to perform the different actions of the functions:
        #TODO: fine-tune the permissions. These are too broad:
        table.grant_read_data(get_all_items_lambda)
        table.grant_read_data(get_item_ID_lambda)
        table.grant_write_data(add_item_lambda)

        #3. API GATEWAY
        api = aws_apigateway.RestApi(
            self, "CatalogAPI",
            
        )
        #How to create outputs?
        CfnOutput(
            self, 'OutputTableARN', 
            value = table.table_arn,
            key = 'OutputTableARN'
        )
