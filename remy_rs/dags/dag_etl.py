# """Airflow DAG to do ETL of Recipe interactions."""
# from datetime import timedelta
# import logging

# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator
# from airflow import DAG
# from airflow.utils import dates

# logging.basicConfig(format="%(name)s-%(levelname)s-%(asctime)s-%(message)s", level=logging.INFO)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# DEFAULT_ARGS = {
#     "owner": "remy",
#     "depends_on_past": False,
#     "start_date": dates.days_ago(1),  # TODO: i think there's a cleaner way
#     "retries": 2,
#     "retry_delay": timedelta(minutes=5),  # timedelta(seconds=30), TODO
#     "provide_context": False,
# }

# dag = DAG(
#     "basic_interactions_etl",
#     description=(
#         "DAG to do ETL of Recipe interactions"
#     ),
#     schedule_interval=timedelta(minutes=5),  # TODO
#     # catchup=
#     default_args=DEFAULT_ARGS,
# )


# # def make_dataset(**kwargs):
# #     logger.info('these are the kwargs:')
# #     logger.info(kwargs)


# def sample_callable2():
#     logger.info('bro!')


# with dag:
#     sample = BashOperator(
#         task_id="make_dataset",
#         bash_command="/opt/airflow/app/remy_rs/data/make_dataset.sh ",
#         # bash_command="/app/remy_rs/data/make_dataset.sh",
#     )

#     sample2 = PythonOperator(
#         task_id="sample2",
#         python_callable=sample_callable2,
#     )

#     sample >> sample2
