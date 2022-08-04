"""This file creates the deployment in the pipeline. There can be
multiple stages per pipeline, and each will deploy resources as defined
by the imported stack. Each stage will be deployed sequentially.
This file should not be changed unless absolutely necessary."""
from constructs import Construct
from aws_cdk import (
  Stage
)

from .resource_stack import TensorGenericBackendStack

# Deployment stage for automatically deploying associated stack resources
class TensorGenericBackendStage(Stage):
  """This class is the deployment stage for the pipeline."""
  def __init__(self, scope: Construct, idn: str, stage_name: str, conf, **kwargs):
    super().__init__(scope, idn, **kwargs)

    # Initializes Stack with names based on branch name
    TensorGenericBackendStack(
      self, f"{conf['resource_ids']['stack_id']}-{stage_name}",
      conf=conf
    )
