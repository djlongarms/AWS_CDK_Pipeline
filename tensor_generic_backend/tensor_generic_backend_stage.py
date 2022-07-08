from constructs import Construct
from aws_cdk import (
    Stage
)
from .tensor_generic_backend_stack import TensorGenericBackendStack

# Deployment stage for automatically deploying associated stack resources
class TensorGenericBackendStage(Stage):
    def __init__(self, scope: Construct, id: str, conf, branch: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Initializes Stack with names based on branch name
        service = TensorGenericBackendStack(
            self, f"{conf.resource_ids.stack_id}-{branch}"
        )