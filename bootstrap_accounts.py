"""This script bootstraps each account listed in the config file. The main account
will be given trust to deploy resources in any other accounts that may be listed
for deployment in all the different branches and/or stages desired."""
import os
import json
import sys

# Loads config file
with open("config/config.json", encoding='UTF-8') as conf_file:
  conf = json.load(conf_file)

# Checks if user wants stack to create repo
CREATE_REPO = conf['conditions']['CREATE_REPO']

# Retrieves account number, region, and associated AWS CLI profile for tools account
tools_account = conf['aws']['account']
region = conf['aws']['region']
cli_profile = conf['aws']['cli_profile']

# Checks retrieved details to ensure they have been provided by the user
if tools_account is None or region is None or cli_profile is None:
  print("Please ensure Account Number, Region, and CLI Profile for tools account is set in the config.json file.")
  sys.exit()

# Retrieves all desired branches
branches = conf['branches']

# Bootstraps tools account and region for CDK compatibility
os.system(f"""
  cdk bootstrap {tools_account}/{region} \
  --no-bootstrap-customer-key \
  --cloudformation-execution-policies 'arn:aws:iam::aws:policy/AdministratorAccess' \
  --profile {cli_profile} \
  -c branch={list(branches)[0]}
""")

# Keeps track of bootstrapped accounts and regions so no account/region coombo gets bootstrapped twice
bootstrapped_accounts = {
  tools_account: [region]
}

# Iterates over each branch
for branch in branches:
  # Iterates over each stage in current branch
  for stage in branches[branch]['stages']:
    # Retrieves account number, region, and AWS CLI profile
    account = stage['account']
    region = stage['region']
    cli_profile = stage['cli_profile']

    # If no account number is provided, it will deploy to tools account and region, so bootstrapping is skipped
    if account is None:
      continue

    # Retrieves regions associated with account number from bootstrapped account
    current_account = bootstrapped_accounts.get(account)

    # Check if retrieved list is actually 'None'
    if current_account is None:
      # If 'None', add account and region to list of bootstrapped accounts
      bootstrapped_accounts.update({
        account: [region]
      })
    elif bootstrapped_accounts[account].count(region) == 0:
      # If not 'None', but region is not part of list, add region to list of bootstrapped accounts
      bootstrapped_accounts[account].append(region)
    else:
      # If not 'None' and region is part of list, account and region are already bootstrapped, so skip bootstrapping
      continue

    # If reaching this point, bootstrap account and region with policy that trusts tools account to deploy to this account and region
    os.system(f"""
      cdk bootstrap {account}/{region} \
      --no-bootstrap-customer-key \
      --cloudformation-execution-policies 'arn:aws:iam::aws:policy/AdministratorAccess' \
      --trust {tools_account} \
      --trust-for-lookup {tools_account} \
      --profile {cli_profile} \
      -c branch={branch}
    """)

# If user wants stack to create new repo, resets CREATE_REPO condition to true
if CREATE_REPO:
  conf['conditions']['CREATE_REPO'] = True
  with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/config.json"), 'w', encoding='UTF-8') as f:
    json.dump(conf, f, indent=4)
