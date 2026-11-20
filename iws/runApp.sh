#!/bin/bash
# Author: Rohtash Lakra
echo
if [ "$1" == "prod" ]; then
  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --workers ${WORKERS:-2}
else
  uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --reload
fi
echo

