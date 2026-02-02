#!/bin/bash
# Author: Rohtash Lakra
# Common version function used by build and run scripts

# Build Version Function
function buildVersion() {
  local VERSION="0.0"
  local SNAPSHOT_ARG="${1:-}"
  
  GIT_COMMIT_COUNT=$(git rev-list HEAD --count 2>/dev/null)
  if [ $? -ne 0 ] || [ -z "$GIT_COMMIT_COUNT" ]; then
    VERSION="${VERSION}.1"
  else
    VERSION="${VERSION}.${GIT_COMMIT_COUNT}"
  fi
  
  if [[ ! -z "${SNAPSHOT_ARG}" ]]; then
      VERSION="${VERSION}-SNAPSHOT"
  fi

  echo "${VERSION}";
}

