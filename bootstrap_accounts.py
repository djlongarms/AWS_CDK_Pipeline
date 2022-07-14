import os
import json

conf = json.load(open("config/config.json"))

tools_account = conf['aws']['account']
region = conf['aws']['region']
cli_profile = conf['aws']['cli_profile']

if tools_account is None or region is None or cli_profile is None:
    print("Please ensure Account Number, Region, and CLI Profile for tools account is set in the config.json file.")
    exit()

os.system(f"cdk bootstrap {tools_account}/{region} --no-bootstrap-customer-key --cloudformation-execution-policies 'arn:aws:iam::aws:policy/AdministratorAccess' --profile {cli_profile} -c branch=dev")

bootstrapped_accounts = {
    tools_account: [region]
}

branches = conf['branches']

for branch in branches:
    for stage in branches[branch]['stages']:
        account = stage['account']
        region = stage['region']
        cli_profile = stage['cli_profile']

        if account is None:
            continue

        current_account = bootstrapped_accounts.get(account)

        if current_account is None:
            bootstrapped_accounts.update({
                account: [region]
            })
        elif bootstrapped_accounts[account].count(region) == 0:
            bootstrapped_accounts[account].append(region)
        else:
            continue

        os.system(f"cdk bootstrap {account}/{region} --no-bootstrap-customer-key --cloudformation-execution-policies 'arn:aws:iam::aws:policy/AdministratorAccess' --trust {tools_account} --trust-for-lookup {tools_account} --profile {cli_profile} -c branch=dev")
