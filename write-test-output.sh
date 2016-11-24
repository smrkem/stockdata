#!/bin/bash

echo "Number args: $#"

if [ $# -eq 0 ]; then
  echo "usage write-test-output output_filename"
else
  FILEPATH="docs/test_messages/$1.txt"
  TESTRUN_SEPARATOR="------
\\\\\\\\\\\\
//////
-"

  echo "Running tests to $FILEPATH..."
  docker-compose run --rm web sh runtests.sh unit >> $FILEPATH 2>&1
  echo "





$TESTRUN_SEPARATOR" >> $FILEPATH
fi
