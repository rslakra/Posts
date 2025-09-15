#!/bin/bash
# Author: Rohtash Lakra
echo
#if [ $# -gt 0 ]; then
if [ "$1" == "production" ]; then
  gunicorn -c gunicorn.conf.py wsgi:app
else
  python -m flask --app wsgi run --port 8080 --debug
fi
echo

