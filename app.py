#!/usr/bin/env python3
import this
import aws_cdk as cdk
from tensor_generic_backend.tensor_generic_backend_pipeline import TensorGenericBackendPipelineStack

app = cdk.App()

TensorGenericBackendPipelineStack(
    app, "TensorGenericBackendStack",
    env=cdk.Environment(
        account=cdk.CfnParameter(this, "accountID", type="String",
    description="The account number where the stack will be deployed."),
        region=cdk.CfnParameter(this, "region", type="String",
    description="The region where the stack will be deployed.")
    )
)

app.synth()
