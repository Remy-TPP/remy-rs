"""Airflow DAG to train RS model from Recipe interactions."""
import os
from datetime import timedelta
import logging

from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow.utils import dates

SCHEDULE_INTERVAL_MINUTES = int(float(os.getenv('TRAIN_DAG_SCHEDULE_INTERVAL_MINUTES', '30')))

logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_ARGS = {
    "owner": "remy",
    "depends_on_past": False,  # TODO: recheck
    "start_date": dates.days_ago(1),  # TODO: i think there's a cleaner way
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
    "provide_context": False,
}

dag = DAG(
    "basic_interactions_train",
    description=(
        "DAG to train RS model from Recipe interactions"
    ),
    schedule_interval=timedelta(minutes=SCHEDULE_INTERVAL_MINUTES),
    # catchup=
    default_args=DEFAULT_ARGS,
)
# TODO: have a sensor or something to start this DAG?


with dag:
    etl_op = BashOperator(
        task_id="make_training_dataset",
        bash_command="/opt/airflow/remy_rs/data/make_dataset.sh ",
    )

    train_model_op = BashOperator(
        task_id="train_model",
        bash_command="/opt/airflow/remy_rs/models/train_model.sh ",
    )

    # save_model_op = BashOperator(
    #     task_id="save_trained_model",
    #     bash_command="/opt/airflow/app/data/....sh ",
    # )

    etl_op >> train_model_op  # >> save_model_op


# TODO: make new DAG for testing and reporting
