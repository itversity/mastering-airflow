from datetime import timedelta

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
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
    dag_id='22_serial_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(7),
    dagrun_timeout=timedelta(minutes=10)
)

pre_processing = BashOperator(
    task_id='pre_processing_task',
    bash_command='echo "Pre Processing started at `date`"',
    dag=dag
)

extract = BashOperator(
    task_id='extract_task',
    bash_command='echo "Extract started at `date`"',
    dag=dag
)

transform = BashOperator(
    task_id='transform_task',
    bash_command='echo "Transformation started at `date`"',
    dag=dag
)

load = BashOperator(
    task_id='load_task',
    bash_command='echo "Loading started at `date`"',
    dag=dag
)

post_processing = BashOperator(
    task_id='post_processing_task',
    bash_command='echo "Post Processing started at `date`"',
    dag=dag
)

# pre_processing >> extract >> transform >> load >> post_processing
# chain(pre_processing, extract, transform, load, post_processing)

pre_processing.set_downstream(extract)
extract.set_downstream(transform)
load.set_upstream(transform)
load.set_downstream(post_processing)