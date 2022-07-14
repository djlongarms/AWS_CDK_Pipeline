import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.resource_stack import TensorGenericBackendStack

# example tests. To run these tests, uncomment this file along with the example
# resource in tensor_generic_backend/tensor_generic_backend_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TensorGenericBackendStack(app, "tensor-generic-backend")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
