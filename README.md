
# I. Generic Pipeline Project

This code is meant to serve as the basis for backend projects being built using the AWS CDK to facilitate easier creation of CICD Pipelines in any account in any region.

This is achieved by creating a stack which connects to an AWS CodeCommit repository and running code from each branch desired by the developers into its own pipeline to create different environments as desired.

![An example layout of a deployment from AWS CDK on a personal computer, deploying resources to multiple AWS accounts.](imgs/CDK_Pipeline.jpg?raw=true "Example deployment from AWS CDK to multiple accounts.")

# II. Deploying the First Pipeline(s)

When attempting to deploy this code for a project, the following should be done the first time:

1. Clone/Download this repo to your local machine. If you clone it, please make sure to run `git remote remove origin` before anything so as to not modify the code in this repo.

2. Create a virtual environment, source the environment, and install the items in the 'requirements.txt' file.

3. Run `git init` and connect your local repo to a new AWS CodeCommit repository. Upload this code into that repsository under whatever branch name you'd like as the default branch for the project.

4. Run the following command to make the build file executable in CodeBuild: `git update-index --chmod=+x .build.sh`

5. Modify the 'config.json' file. The items in this file are the ids/names for the basic resources needed for this project to work, so make sure the naming scheme reflects what you want for the project. The `aws` section of the file should be filled in with an account number and region to act as a "tools" account for the pipeline, as well as the name of the AWS CLI Profile with proper credentials for the given account.

6. In particular, make sure the 'repo_name' attribute of the config.json file is the same as the name of the AWS CodeCommit repo you connected to before. (More on this in section VI)

7. Under the `branches` section of the config.json, modify the keys to reflect the branches you'd like to have in the repository. Each branch item should have a list object named `stages` in it. This list must be comprised of dictionary objects containing the following: an account number and region where this stage will be deployed, the AWS CLI Profile name with credentials for the given account, the stage name for the stage, and whether or not the stage should have a manual approval after the stage is complete. The account number and region can be left null for a stage if you want that stage in the same account and region as the "tools" account.

8. Commit and push this code into the AWS CodeCommit repository. Make sure to create and push each of the branches you created in the `branches` section of the config file.

9. Run the provided `deploy_all.py` script in the root folder of the project.

10. Your initial stack or set of stacks is now deployed! You can view the progress of the pipeline in AWS CodePipeline.

This will create one environment for your resources, with a pipeline to deploy those resources as you add/modify them using the AWS CDK. This will be explained more in section V of the README.

# III. Deploying Subsequent Pipelines

Once the first set of pipelines is deployed, you may wish to create more pipelines for separate coding environments. This can be done with the following:

1. Create a new local branch and push it up the connected Repository.

2. Add a new branch to the `branches` section of the config file with the relevant fields needed for deployment.

3. Run `cdk deploy -c branch=<branch_name>` with '<branch_name>' replaced with the name of the new branch.

4. Your new stack is now deployed! This will create a brand new pipeline, unconnected to already existing pipelines.

This can be used to create new pipelines for each each environment you desire, with each branch having it's own pipeline and set of deployed resources. Deleting a branch will not delete the pipeline or resources, that will be discussed in the section IV.

# IV. Deleting a Pipeline and its Resources

If you finish work done in a certain environment and wish to delete it, you can accomplish this by running `cdk destroy -c branch=<branch_name>` with '<branch_name>' replaced with the name of the branch to be deleted. This will destroy the stack along with the resources created by the pipeline. This will not delete the repository itself, nor will it delete the branch in the repository. Some deployed resources may not be deleted depending on the type, so it is always recommended you confirm each resource has been deleted after running.

# V. Deploying Resources

Resources can be deployed using the AWS CDK. For a tutorial on how this works, here is a workshop great workshop that walks through the concept: https://cdkworkshop.com/

There is a 'resources' folder in the 'tensor_generic_pipeline' folder where you can place code for resource creation. Importing these resources into the 'tensor_generic_backend_stack.py' file and calling them in the stack's '__init__' method will add them to the pipeline when you commit and push them to the repository.

Since each branch has its own pipeline, pushing to one branch will only deploy/modify resources in that environment without affecting the separate environments.

# VI. Defining vs Referencing a Codecommit Repo

There are two ways to go about integrating your repository into the cdk stack:

    # by having cdk deploy the repo for you:
    repo = codecommit.Repository(self, 'DemoRepo',repository_name="DemoRepo")
    # or by grabbing the already deployed repo:
    repo = codecommit.Repository.from_repository_name(self, "DemoRepo", "DemoRepo")
If you are using the first method, where the repo is created as part of your cdk stack, under these circumstances **your repository, all code, commits, and branches will be deleted without warning**:

 - The repo was created in a prior deployment; then,    
 - The repo instantiation line is removed, or otherwise not ran on runtime 
 - This code is then committed, kicking off the codepipeline process
     -or-
 - a user runs a `cdk destroy` command

The preferred method is to create the repository manually, then reference it inside your cdk stack to avoid these issues.

If you still wish to have the stack create a repository for you, modify the config.json file so that the CREATE_REPO condition is 'true' instead of 'false,' then make sure to leave it alone. Deploying the stack will switch it back to 'false' once the repository has been added to the stack creation code.
