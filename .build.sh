npm install -g aws-cdk
pip install -r requirements.txt
pylint --rcfile=./.pylintrc `pwd` || pylint-exit -wfail -efail -cfail $?
if [ $? -ne 0 ]; then
  exit $?
fi
cdk synth -c branch=$BRANCH