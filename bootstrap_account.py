import os
import json

conf = json.load(open("config/config.json"))

tools_account = conf['aws']['account']
region = conf['aws']['region']
cli_profile = conf['aws']['cli_profile']

if tools_account is not None and region is not None:
    os.system(f"cdk bootstrap {tools_account}/{region} --no-bootstrap-customer-key --cloudformation-execution-policies 'arn:aws:iam::aws:policy/AdministratorAccess' --profile {cli_profile} -c branch=dev")
else:
    os.system("cdk bootstrap")

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
