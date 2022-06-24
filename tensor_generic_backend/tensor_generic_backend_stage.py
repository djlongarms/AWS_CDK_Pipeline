from constructs import Construct
from aws_cdk import (
    Stage
)
from .tensor_generic_backend_stack import TensorGenericBackendStack

class TensorGenericBackendStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = TensorGenericBackendStack(self, "TensorGenericBackend")