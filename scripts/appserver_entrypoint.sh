#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "PWD: $PWD"
export PORT=${PORT:=8000}
echo "PORT: ${PORT}"

# This is the db for Airflow
AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN:=${DATABASE_URL}}
echo "AIRFLOW__CORE__SQL_ALCHEMY_CONN: ${AIRFLOW__CORE__SQL_ALCHEMY_CONN}"
echo "PYTHONPATH: ${PYTHONPATH:=not set}"
export AIRFLOW_PORT=${AIRFLOW_PORT:=8080}
echo "AIRFLOW_PORT: ${AIRFLOW_PORT}"


# Remy API's db is expected as REMY_API_DB_URL
echo "REMY_API_DB_URL: ${REMY_API_DB_URL}"
export API_PORT=${API_PORT:=${PORT}}
echo "API_PORT: ${API_PORT}"


# echo "Starting airflow webserver"
# # TODO: could also daemonize with -d, but should redirect stdout/stderr
# /home/airflow/.local/bin/airflow webserver -p ${AIRFLOW_PORT} &

if [[ ${ENV:=dev} == 'dev' ]]; then
  # Launch scheduler
  # /home/airflow/.local/bin/airflow upgradedb
  # TODO: could also daemonize with --daemon, but should redirect stdout/stderr
  /home/airflow/.local/bin/airflow scheduler &
fi
# Train
sleep 4
# /home/airflow/.local/bin/airflow dags trigger basic_interactions_train
# airflow dags trigger basic_interactions_train

echo "Starting API"
if [[ ${ENV:=dev} == 'production' ]]; then
  echo "Running gunicorn"
  /home/airflow/.local/bin/gunicorn -b "0.0.0.0:${API_PORT}" -w 1 -k uvicorn.workers.UvicornWorker remy_rs.api.api:api
else
  echo "Running uvicorn"
  /home/airflow/.local/bin/uvicorn \
    --host "0.0.0.0" --port "${API_PORT}" \
    --reload --reload-dir remy_rs/ \
    -- remy_rs.api.api:api
fi
