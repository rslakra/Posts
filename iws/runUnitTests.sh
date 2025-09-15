#!/bin/bash
# Author: Rohtash Lakra
echo
if [ "$1" == "production" ]; then
  echo "python -m unittest discover -s ./tests -p 'test_*.py'"
  python -m unittest discover -s ./tests -p "test_*.py"
else
  echo "python3 -m unittest"
  python3 -m unittest
fi
echo
