FROM apache/airflow:1.10.14-python3.8 AS dev

WORKDIR /opt/airflow

# Install needed system packages
USER 0
RUN whoami && groups
RUN apt-get update -qqy && \
    apt-get install -qy gcc g++ libpq-dev
USER airflow
RUN whoami && groups

COPY requirements.txt Pipfile Pipfile.lock ./
RUN pip --version && \
    python --version && \
    pip install -r requirements.txt

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]


FROM dev AS production

COPY ./remy_rs/dags /opt/airflow/dags
COPY ./remy_rs /opt/airflow/remy_rs
COPY ./scripts /opt/airflow/scripts
COPY ./setup.py /opt/airflow/

RUN mkdir -p /opt/airflow/model && \
    chown airflow /opt/airflow/model && \
    ls -lA /opt/airflow/

USER 0
RUN python3 setup.py -q install

USER airflow

COPY --chown=airflow:root scripts/airflow_docker_entrypoint.sh /entrypoint
RUN chmod a+x /entrypoint

RUN pip freeze

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]


# ARG DATABASE_URL
# ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=${DATABASE_URL}
