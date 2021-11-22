"""Example DAG demonstrating fork parallel tasks and join them."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='15_fork_and_join_dag',
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
        bash_command='sleep 60; echo "Data read at `date` from source 1"',
    )

    from_source_2 = BashOperator(
        task_id='read_from_source_2',
        bash_command='sleep 30; echo "Data read at `date` from source 2"',
    )

    join_sources = BashOperator(
        task_id='join_source_1_and_2',
        bash_command='echo "Data from source 1 and 2 are joined at `date`"'
    )

    post_processing = BashOperator(
        task_id='post_processing',
        bash_command='echo "Post Processing started at `date`"',
    )

    pre_processing >> from_source_1 >> join_sources
    pre_processing >> from_source_2 >> join_sources
    join_sources >> post_processing


if __name__ == "__main__":
    dag.cli()
