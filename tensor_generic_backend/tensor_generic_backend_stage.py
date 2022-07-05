from constructs import Construct
from aws_cdk import (
    Stage,
    Environment
)
from .tensor_generic_backend_stack import TensorGenericBackendStack

class TensorGenericBackendStage(Stage):
    def __init__(self, scope: Construct, id: str, env_name: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = TensorGenericBackendStack(
            self, "TensorGenericBackend{0}".format(env_name)
        )