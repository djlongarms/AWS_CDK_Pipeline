"""This file bootstraps each account listed in the config file,
then deploys stacks according to each branch's specifications
as detailed in the config.json file. This file should be run once
everything else has been prepared for the pipeline(s)."""
import os
import json

COMMAND = "python3 bootstrap_accounts.py"

os.system(COMMAND)

with open("config/config.json", encoding='UTF-8') as conf_file:
  branches = json.load(conf_file)['branches']

for branch in list(branches):
  COMMAND = f"cdk deploy -c branch={branch} --all --require-approval never"
  os.system(COMMAND)
