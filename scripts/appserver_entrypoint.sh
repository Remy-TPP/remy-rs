#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo $PWD
# This is the db for Airflow
AIRFLOW__CORE__SQL_ALCHEMY_CONN=${DATABASE_URL}
echo "AIRFLOW__CORE__SQL_ALCHEMY_CONN: ${AIRFLOW__CORE__SQL_ALCHEMY_CONN}"

# /home/airflow/.local/bin/airflow scheduler &
# TODO: next thing to try is copying the entrypoint
# from the airflow docker repository
# https://github.com/apache/airflow/blob/master/scripts/in_container/prod/entrypoint_prod.sh


# Remy API's db is expected as REMY_API_DB_URL
echo "REMY_API_DB_URL: ${REMY_API_DB_URL:=not set}"
export PYTHONPATH=/usr/local/lib/python3.6/site-packages:/home/airflow/.local/lib/python3.6/site-packages
echo "PYTHONPATH: ${PYTHONPATH:=not set}"

echo "STARTING..."

if [[ ${ENV:=dev} == 'production' ]]; then
  echo "Running gunicorn"
  /home/airflow/.local/bin/gunicorn -b "0.0.0.0:${PORT:=8000}" -w 4 -k uvicorn.workers.UvicornWorker remy_rs.api.api:api
else
  echo "Running uvicorn"
  /usr/local/bin/uvicorn --host "0.0.0.0" --port "${PORT:=8000}" -- remy_rs.api.api:api
fi
