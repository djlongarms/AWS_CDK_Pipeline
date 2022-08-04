npm install -g aws-cdk
pip install -r requirements.txt
pylint --rcfile=./.pylintrc `pwd` || pylint-exit -wfail -efail -cfail $?
cdk synth -c branch=$BRANCH