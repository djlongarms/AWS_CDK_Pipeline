from constructs import Construct
from aws_cdk import (
    Stack
)

# Resource stack for deployment through pipeline
class TensorGenericBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, conf, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        