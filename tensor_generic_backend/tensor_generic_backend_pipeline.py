from os import path
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    Environment,
    CfnParameter,
    aws_codecommit as codecommit,
    pipelines as pipelines
)
from .tensor_generic_backend_stage import TensorGenericBackendStage

class TensorGenericBackendPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        env = Environment(
            account=CfnParameter(self, "accountID", type="String",
    description="The account number where the stack will be deployed."),
            region=CfnParameter(self, "region", type="String",
    description="The region where the stack will be deployed.")
        )

        print("Environment Set.")

        repo = codecommit.Repository(
            self, "GenericBackendRepo",
            repository_name="GenericBackendRepo"
        )

        repo.apply_removal_policy(RemovalPolicy.DESTROY)

        print("CodeCommit Repository Created.")

        pipeline = pipelines.CodePipeline(
            self, "GenericBackendPipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "master"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        print("Pipeline Created")

        deploy = TensorGenericBackendStage(
            self, "Deploy",
            env = Environment(
                account=env.account.value_as_string,
                region=env.region.value_as_string
            )
        )
        deploy_stage = pipeline.add_stage(deploy)

        print("Deployment Stage Created.")
