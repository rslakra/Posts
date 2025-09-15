#!/bin/bash
# Author: Rohtash Lakra
echo
#if [ $# -gt 0 ]; then
if [ "$1" == "production" ]; then
  gunicorn -c gunicorn.conf.py wsgi:app
else
  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8082} --reload
fi
echo

