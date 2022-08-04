"""This file is where resources will be placed to be created in the stack.
The pipeline will create a deployment for each stage and deploy resources
as described here. A user can create resource files in the 'resources' folder,
import them here, and instantiate them in the stack. Then, once deployed,
the resources will be created in the AWS account associated with the stage."""
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
  """This is the resource stack for the resources to be deployed."""
  def __init__(self, scope: Construct, construct_id: str, conf, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    print(conf)
    