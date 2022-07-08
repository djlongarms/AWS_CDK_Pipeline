from os import path
import sys
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_s3_assets,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    CfnOutput
)
from .tensor_generic_backend_stage import TensorGenericBackendStage
from omegaconf import OmegaConf

sys.path.append(path.dirname(path.dirname(__file__)))
from zip_file_code.zip_file_code import zip_repo_code

class TensorGenericBackendPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, conf, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        branch = self.node.try_get_context("branch")

        if conf.conditions.CREATE_REPO:
            conf.conditions.CREATE_REPO = False
            OmegaConf.save(config=conf, f=path.join(path.dirname(path.dirname(__file__)), "config/config.yaml"))

            zip_repo_code()
            
            repo_code_asset = aws_s3_assets.Asset(
                self, conf.resource_ids.repo_code_asset_id,
                exclude=['.venv', 'cdk.out', '.git'],
                path=path.join(path.dirname(path.dirname(__file__)), 'tensor_generic_backend.zip')
            )

            repo = codecommit.Repository(
                self, conf.resource_ids.repo_id,
                repository_name=conf.resource_names.repo_name,
                code=codecommit.Code.from_asset(repo_code_asset, branch)
            )

            repo.apply_removal_policy(RemovalPolicy.RETAIN)

            self._repo_clone_url = CfnOutput(
                self, conf.resource_ids.repo_id + "URL",
                value=repo.repository_clone_url_http
            )
        else:
            repo = codecommit.Repository.from_repository_name(
                self, conf.resource_ids.repo_id,
                repository_name=conf.resource_names.repo_name
            )

        pipeline = pipelines.CodePipeline(
            self, f"{conf.resource_ids.pipeline_id}-{branch}",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, branch),
                env={
                    "BRANCH": branch
                },
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth -c branch=$BRANCH"
                ]
            )
        )

        deploy = TensorGenericBackendStage(
            self, f"{conf.resource_ids.pipeline_stage_id}-{branch}",
            env_name=branch,
            conf=conf
        )
        deploy_stage = pipeline.add_stage(deploy) 
