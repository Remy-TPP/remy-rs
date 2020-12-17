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
RUN apt-get update -qy && \
    apt-get install -qy gcc g++ libpq-dev

# USER airflow
# RUN whoami && groups
COPY build/requirements.txt Pipfile Pipfile.lock ./
RUN pip --version && \
    python --version && \
    pip install numpy && \
    pip install -r requirements.txt && \
    pip install pipenv

USER airflow

RUN pipenv --python 3.6 && \
    pipenv install


FROM dev AS production

COPY ./remy_rs/dags /opt/airflow/dags
COPY ./remy_rs /opt/airflow/remy_rs
COPY ./setup.py /opt/airflow/

USER 0
RUN python3 setup.py -q install
USER airflow
