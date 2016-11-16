if [ $# -eq 0 ]; then
  testcommand='test'
else
  testcommand="test --testtype=$1"
fi

xvfb-run python manage.py $testcommand
exit 0
