import os
import json

command = "python3 bootstrap_accounts.py"

os.system(command)

branches = json.load(open("config/config.json"))['branches']

for branch in list(branches):
    command = f"cdk deploy -c branch={branch} --all --require-approval never"
    os.system(command)
