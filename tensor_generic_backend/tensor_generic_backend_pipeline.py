from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines
)
from .tensor_generic_backend_stage import TensorGenericBackendStage

class TensorGenericBackendPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo = codecommit.Repository(
            self, "GenericBackendRepo",
            repository_name="GenericBackendRepo"
        )

        pipeline = pipelines.CodePipeline(
            self, "GenericPipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk cynth"
                ]
            )
        )

        deploy = TensorGenericBackendStage(self, "Deploy")
        deploy_stage = pipeline.add_stage(deploy)
