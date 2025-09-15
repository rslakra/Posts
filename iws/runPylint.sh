#!/bin/bash
# Author: Rohtash Lakra
echo
pylint $(git ls-files '*.py') --rcfile ./../.pylintrc
echo
