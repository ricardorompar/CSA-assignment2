import aws_cdk as core
import aws_cdk.assertions as assertions

from assignment2.assignment2_stack import Assignment2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in assignment2/assignment2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Assignment2Stack(app, "assignment2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
