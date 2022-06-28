#!/usr/bin/env python3
import aws_cdk as cdk
from tensor_generic_backend.tensor_generic_backend_pipeline import TensorGenericBackendPipelineStack

app = cdk.App()

TensorGenericBackendPipelineStack(
    app, "TensorGenericBackendStack",
    env=cdk.Environment(
        account='647309936627',
        region='us-west-2'
    )
)

app.synth()
