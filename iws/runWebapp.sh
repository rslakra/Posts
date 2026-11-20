#!/bin/bash
# Author: Rohtash Lakra
echo
if [ "$1" == "production" ]; then
  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8082} --workers ${WORKERS:-2}
else
  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8082} --reload
fi
echo

