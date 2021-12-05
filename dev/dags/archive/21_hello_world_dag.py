from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow'
}

# with DAG(
#     dag_id='21_hello_world_dag',
#     default_args=args,
#     schedule_interval='0 0 * * *',
#     start_date=days_ago(7),
#     dagrun_timeout=timedelta(minutes=10)
# ) as dag:
#     hello_world = DummyOperator(
#         task_id='hello_world_task'
#     )
#
#     hello_world

dag = DAG(
    dag_id='21_hello_world_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(7),
    dagrun_timeout=timedelta(minutes=10)
)

hello_world = DummyOperator(
    task_id='hello_world_task',
    dag=dag
)

hello_world