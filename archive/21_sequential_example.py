"""Example DAG demonstrating sequence of tasks."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='14_sequence_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    pre_processing = BashOperator(
        task_id='pre_processing',
        bash_command='echo "Pre Processing started at `date`"',
    )

    from_source_1 = BashOperator(
        task_id='read_from_source_1',
        bash_command='echo "Data read at `date` from source 1"',
    )

    from_source_2 = BashOperator(
        task_id='read_from_source_2',
        bash_command='echo "Data read at `date` from source 2"',
    )

    post_processing = BashOperator(
        task_id='post_processing',
        bash_command='echo "Post Processing started at `date`"',
    )

    pre_processing >> from_source_1 >> from_source_2 >> post_processing


if __name__ == "__main__":
    dag.cli()
