from os import path
from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_s3_assets,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    CfnOutput,
    BundlingOptions,
    DockerImage
)
from .pipeline_stage import TensorGenericBackendStage
import json

# Pipeline Stack class
class TensorGenericBackendPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, conf, branch, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Check if user wants repo created by stack
        if conf['conditions']['CREATE_REPO']:
            # Sets condition to false for future deployments
            conf['conditions']['CREATE_REPO'] = False
            with open(path.join(path.dirname(path.dirname(__file__)), "config/config.json"), 'w') as f:
                json.dump(conf, f, indent=4)
            
            # Creates asset for uploading to repo
            repo_code_asset = aws_s3_assets.Asset(
                self, conf['resource_ids']['repo_code_asset_id'],
                path=path.dirname(path.dirname(__file__)),
                bundling=BundlingOptions(
                    image=DockerImage.from_registry(
                        image="public.ecr.aws/docker/library/alpine:latest"
                    ),
                    command=[
                        "sh",
                        "-c",
                        """
                            apk update && apk add zip
                            zip -r /asset-output/code.zip ./* -x "./cdk.out/*"
                            """,
                    ],
                    user="root",
                ),
            )

            # Creates repo
            repo = codecommit.Repository(
                self, conf['resource_ids']['repo_id'],
                repository_name=conf['resource_names']['repo_name'],
                code=codecommit.Code.from_asset(repo_code_asset, branch)
            )

            # Changes removal policy so destroying stack doesn't destroy repo
            repo.apply_removal_policy(RemovalPolicy.RETAIN)

            # Outputs repo clone url for easy connection to new repo.
            self._repo_clone_url = CfnOutput(
                self, conf['resource_ids']['repo_id'] + "URL",
                value=repo.repository_clone_url_http
            )
        else:
            # Connects to already existing repo
            repo = codecommit.Repository.from_repository_name(
                self, conf['resource_ids']['repo_id'],
                repository_name=conf['resource_names']['repo_name']
            )

        # Creates pipeline using given branch name as distinguishing factor
        pipeline = pipelines.CodePipeline(
            self, f"{conf['resource_ids']['pipeline_id']}-{branch}",
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

        # Iterates over stages wanted for the current branch
        for stage in conf['branches'][branch]['stages']:
            # Creates deploy stage for pipeline to automatically deploy code from given branch
            deploy = TensorGenericBackendStage(
                self, f"{conf['resource_ids']['pipeline_stage_id']}-{stage['stage_name']}",
                stage_name=stage['stage_name'],
                manual_approval=stage['manual_approval'],
                conf=conf
            )

            post = []

            if stage['manual_approval']:
                post.append(pipelines.ManualApprovalStep("Approve"))

            deploy_stage = pipeline.add_stage(
                deploy,
                post=post
            )

