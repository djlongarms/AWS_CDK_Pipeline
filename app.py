#!/usr/bin/env python3
import aws_cdk as cdk
import json

from stacks.pipeline_stack import GenericBackendPipelineStack

# Initializes App
app = cdk.App()

# Retrieves config file and branch context variable
conf = json.load(open("config/config.json"))
branch = app.node.try_get_context("branch")

# Initializes pipeline 
GenericBackendPipelineStack(
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
