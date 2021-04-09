# This file is ignored when stack is set to container;
# in which case better look for heroku.yml
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker remy_rs.api.api:api
worker: airflow scheduler
