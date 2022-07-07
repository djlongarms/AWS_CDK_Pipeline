#!/usr/bin/env python3
import aws_cdk as cdk
from tensor_generic_backend.tensor_generic_backend_pipeline import TensorGenericBackendPipelineStack
from omegaconf import OmegaConf

conf = OmegaConf.load("config/config.yaml")

app = cdk.App()

branch = app.node.try_get_context("branch")

TensorGenericBackendPipelineStack(
    app, f"{conf.resource_ids.pipeline_stack_id}-{branch}",
    env = cdk.Environment(
        account=conf.aws.account,
        region=conf.aws.region
    ),
    conf=conf
)

app.synth()
