#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "PWD: $PWD"
export PORT=${PORT:=8000}
echo "PORT: ${PORT}"

# TODO: temp, borrar
sleep 5

# This is the db for Airflow
AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN:=${DATABASE_URL}}
echo "AIRFLOW__CORE__SQL_ALCHEMY_CONN: ${AIRFLOW__CORE__SQL_ALCHEMY_CONN}"
export PYTHONPATH=/usr/local/lib/python3.6/site-packages:/home/airflow/.local/lib/python3.6/site-packages
echo "PYTHONPATH: ${PYTHONPATH:=not set}"
export AIRFLOW_PORT=${AIRFLOW_PORT:=8080}
echo "AIRFLOW_PORT: ${AIRFLOW_PORT}"


# Remy API's db is expected as REMY_API_DB_URL
echo "REMY_API_DB_URL: ${REMY_API_DB_URL}"
export API_PORT=${API_PORT:=${PORT}}
echo "API_PORT: ${API_PORT}"


# TODO: could also daemonize with --daemon, but should redirect stdout/stderr
/home/airflow/.local/bin/airflow scheduler &


# /home/airflow/.local/bin/airflow upgradedb

# echo "Starting airflow webserver"
# # TODO: could also daemonize with -d, but should redirect stdout/stderr
# /home/airflow/.local/bin/airflow webserver -p ${AIRFLOW_PORT} &


echo "Starting API"
if [[ ${ENV:=dev} == 'production' ]]; then
  echo "Running gunicorn"
  /home/airflow/.local/bin/gunicorn -b "0.0.0.0:${API_PORT}" -w 1 -k uvicorn.workers.UvicornWorker remy_rs.api.api:api
else
  echo "Running uvicorn"
  /usr/local/bin/uvicorn --host "0.0.0.0" --port "${API_PORT}" -- remy_rs.api.api:api
fi
