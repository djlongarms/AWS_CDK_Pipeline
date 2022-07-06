from os import path
import sys
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3_assets,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    CfnOutput
)
from .tensor_generic_backend_stage import TensorGenericBackendStage

try:
    sys.path.append(path.dirname(path.dirname(__file__)))
    from zip_file_code.zip_file_code import zip_repo_code
except:
    pass

class TensorGenericBackendPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, conf, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        try:
            zip_repo_code()
        except:
            pass

        repo_code_asset = aws_s3_assets.Asset(
            self, conf.resource_ids.repo_code_asset_id,
            exclude=['.venv', 'cdk.out', '.git'],
            path=path.join(path.dirname(path.dirname(__file__)), 'tensor_generic_backend.zip')
        )

        repo = codecommit.Repository(
            self, conf.resource_ids.repo_id,
            repository_name=conf.resource_names.repo_name,
            code=codecommit.Code.from_asset(repo_code_asset, "main")
        )

        self._repo_clone_url = CfnOutput(
            self, conf.resource_ids.repo_id + "URL",
            value=repo.repository_clone_url_http
        )

        prod_pipeline = pipelines.CodePipeline(
            self, "{0}Prod".format(conf.resource_ids.pipeline_id),
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
            self, "{0}Prod".format(conf.resource_ids.pipeline_stage_id),
            env_name="Prod",
            conf=conf
        )
        prod_deploy_stage = prod_pipeline.add_stage(prod_deploy)

        staging_pipeline = pipelines.CodePipeline(
            self, "{0}Staging".format(conf.resource_ids.pipeline_id),
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
            self, "{0}Staging".format(conf.resource_ids.pipeline_stage_id),
            env_name="Staging",
            conf=conf
        )
        staging_deploy_stage = staging_pipeline.add_stage(staging_deploy)

        dev_pipeline = pipelines.CodePipeline(
            self, "{0}Dev".format(conf.resource_ids.pipeline_id),
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
            self, "{0}Dev".format(conf.resource_ids.pipeline_stage_id),
            env_name="Dev",
            conf=conf
        )
        dev_deploy_stage = dev_pipeline.add_stage(dev_deploy)
