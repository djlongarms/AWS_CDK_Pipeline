import sys
import os
from constructs import Construct
from aws_cdk import (
    Stack
)

# Append resources folder to path for importing resources.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from resources import (
#   Import resources from resources folder here.
# )


# Resource stack for deployment through pipeline
class TensorGenericBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, conf, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        