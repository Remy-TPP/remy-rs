#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo $PWD
echo STARTING

# This is the db for Airflow
AIRFLOW__CORE__SQL_ALCHEMY_CONN=${DATABASE_URL}
echo "AIRFLOW__CORE__SQL_ALCHEMY_CONN: ${AIRFLOW__CORE__SQL_ALCHEMY_CONN}"

# /home/airflow/.local/bin/airflow scheduler &
# TODO: next thing to try is copying the entrypoint
# from the airflow docker repository
# https://github.com/apache/airflow/blob/master/scripts/in_container/prod/entrypoint_prod.sh


# Remy API's db is expected as REMY_API_DB_URL
echo "REMY_API_DB_URL: ${REMY_API_DB_URL}"
PYTHONPATH=/usr/local/lib/python3.6/site-packages
echo "PYTHONPATH: ${PYTHONPATH}"

if [[ ${ENV} == 'production' ]]; then
  /home/airflow/.local/bin/gunicorn -b "0.0.0.0:${PORT:=8000}" -w 4 -k uvicorn.workers.UvicornWorker remy_rs.api.api:api
else
  /usr/local/bin/uvicorn --host "0.0.0.0" --port "${PORT:=8000}" -- remy_rs.api.api:api
fi
