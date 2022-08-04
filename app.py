"""This file is run when deploying stacks to CloudFormation.
This file should not be changed unless absolutely necessary."""
#!/usr/bin/env python3
import json
import aws_cdk as cdk

from stacks.pipeline_stack import TensorGenericBackendPipelineStack

# Initializes App
app = cdk.App()

# Retrieves config file and branch context variable
with open("config/config.json", encoding='UTF-8') as conf_file:
  conf = json.load(conf_file)
branch = app.node.try_get_context("branch")

# Initializes pipeline
TensorGenericBackendPipelineStack(
  app, f"{conf['resource_ids']['pipeline_stack_id']}-{branch}",
  env = cdk.Environment(
    account=conf['aws']['account'],
    region=conf['aws']['region']
  ),
  conf=conf,
  branch=branch
)

# Synthesizes application for cloud deployment
app.synth()
