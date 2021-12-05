from datetime import timedelta

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator

from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow'
}

with DAG(
    dag_id='24_short_circuit_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(7),
    dagrun_timeout=timedelta(minutes=10)
) as dag:

    pre_processing = ShortCircuitOperator(
        task_id='pre_processing_task',
        python_callable=lambda: False
    )

    extract = BashOperator(
        task_id='extract_task',
        bash_command='echo "Extract started at `date`"'
    )

    transform = BashOperator(
        task_id='transform_task',
        bash_command='echo "Transformation started at `date`"'
    )

    load = BashOperator(
        task_id='load_task',
        bash_command='echo "Loading started at `date`"'
    )

    post_processing = BashOperator(
        task_id='post_processing_task',
        bash_command='echo "Post Processing started at `date`"'
    )

    # pre_processing >> extract >> transform >> load >> post_processing
    # chain(pre_processing, extract, transform, load, post_processing)

    pre_processing.set_downstream(extract)
    extract.set_downstream(transform)
    load.set_upstream(transform)
    load.set_downstream(post_processing)