#!/bin/bash
# Author: Rohtash Lakra
echo
if [ $# -gt 0 ]; then
  gunicorn -c iws/webapp/gunicorn.conf.py iws.webapp:app
else
  python -m flask --app iws/webapp run --port 8080 --debug
fi
echo
