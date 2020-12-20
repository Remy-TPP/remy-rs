FROM apache/airflow AS dev

WORKDIR /opt/airflow

# RUN pip install apache-airflow

# COPY Pipfile Pipfile.lock ./
# RUN pip install --user pipenv && \
#     pipenv --python 3.7 && \
#     pipenv install psycopg2-binary && \
#     pipenv install
    # TODO: use frozen packages

USER 0
RUN whoami && groups
RUN apt-get update -qqy && \
    apt-get install -qy gcc g++ libpq-dev

# USER airflow
# RUN whoami && groups
# COPY build/requirements.txt Pipfile Pipfile.lock ./
COPY requirements.txt Pipfile Pipfile.lock ./
RUN pip --version && \
    python --version && \
    pip install numpy && \
    pip install -r requirements.txt

USER airflow


FROM dev AS production

COPY ./remy_rs/dags /opt/airflow/dags
COPY ./remy_rs /opt/airflow/remy_rs
COPY ./scripts /opt/airflow/scripts
COPY ./setup.py ./airflow.cfg /opt/airflow/

USER 0
RUN python3 setup.py -q install

# nginx
# COPY ./scripts/nginx.conf /etc/nginx/conf.d/default.conf
# RUN apt update -qqy && \
#     apt install -qy nginx
    # systemctl enable nginx  && \
    # systemctl start nginx && \
    # systemctl status nginx | cat
USER airflow

COPY --chown=airflow:root scripts/airflow_docker_entrypoint.sh /entrypoint
RUN chmod a+x /entrypoint
# ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
# RUN ["/usr/bin/dumb-init", "--", "/entrypoint"]

# ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint", "bash", "./scripts/appserver_entrypoint.sh"]
ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]


# ARG DATABASE_URL
# ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=${DATABASE_URL}
