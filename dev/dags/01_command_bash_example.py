"""Example DAG demonstrating the usage of the BashOperator to run bash command."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='01_command_bash_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:

    run_this = BashOperator(
        task_id='run_bash_command',
        bash_command='echo "Hello World"',
    )

    run_this


if __name__ == "__main__":
    dag.cli()
