#!/usr/bin/env bash
# Run in root dir
set -euo pipefail
IFS=$'\n\t'

PYTHONPATH=/usr/local/lib/python3.6/site-packages \
  uvicorn --host="0.0.0.0" remy_rs.api.api:api
# TODO: change for gunicorn in prod
