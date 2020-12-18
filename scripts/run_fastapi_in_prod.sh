#!/usr/bin/env bash
# Run in project root dir
set -euo pipefail
IFS=$'\n\t'

mkdir -p /tmp/remy_rs/models/
touch /tmp/remy_rs/models/model.dump
ls /tmp/remy_rs/models/model.dump

ENV=production
PYTHONPATH=/usr/local/lib/python3.6/site-packages
echo "ENV: ${ENV}"
echo "PYTHONPATH: ${PYTHONPATH}"

/usr/local/bin/uvicorn --host "0.0.0.0" --port "${PORT:=8000}" -- remy_rs.api.api:api
# TODO: change for gunicorn in prod
# gunicorn -b "0.0.0.0:${PORT:=8000}" -w 4 -k uvicorn.workers.UvicornWorker remy_rs.api.api:api
