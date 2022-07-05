from os import path
import sys
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3_assets,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)
from .tensor_generic_backend_stage import TensorGenericBackendStage

try:
    sys.path.append(path.dirname(path.dirname(__file__)))
    from zip_file_code.zip_file_code import zip_repo_code
except:
    pass

class TensorGenericBackendPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, env_name: str, branch_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        try:
            zip_repo_code()
        except:
            pass

        repo_code_asset = aws_s3_assets.Asset(
            self, "RepositoryCodeAsset",
            exclude=['.venv', 'cdk.out', '.git'],
            path=path.join(path.dirname(path.dirname(__file__)), 'tensor_generic_backend.zip')
        )

        repo = codecommit.Repository(
            self, "GenericBackendRepo",
            repository_name="GenericBackendRepo",
            code=codecommit.Code.from_asset(repo_code_asset, "main")
        )

        prod_pipeline = pipelines.CodePipeline(
            self, "GenericBackendPipeline{0}".format("Prod"),
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        prod_deploy = TensorGenericBackendStage(
            self, "DeployProd",
            env_name=env_name
        )
        prod_deploy_stage = prod_pipeline.add_stage(prod_deploy)

        staging_pipeline = pipelines.CodePipeline(
            self, "GenericBackendPipeline{0}".format("Staging"),
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "staging"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        staging_deploy = TensorGenericBackendStage(
            self, "DeployStaging",
            env_name=env_name
        )
        staging_deploy_stage = staging_pipeline.add_stage(staging_deploy)

        dev_pipeline = pipelines.CodePipeline(
            self, "GenericBackendPipeline{0}".format("Dev"),
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "dev"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )

        dev_deploy = TensorGenericBackendStage(
            self, "DeployDev",
            env_name=env_name
        )
        dev_deploy_stage = dev_pipeline.add_stage(dev_deploy)
