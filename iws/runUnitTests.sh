#!/bin/bash
# Author: Rohtash Lakra
# ENV_TYPE=test selects '.env.test', so the tests never touch the development database.
export ENV_TYPE=test
echo
if [ "$1" == "prod" ]; then
  echo "python -m unittest discover -s ./tests -p 'test_*.py'"
  python -m unittest discover -s ./tests -p "test_*.py"
else
  echo "python3 -m unittest"
  python3 -m unittest
fi
echo
