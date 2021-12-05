"""Example DAG demonstrating the usage of the BashOperator to run python command to invoke python application with arguments."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='04_python_app_bash_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    username = Variable.get('USERNAME')
    run_this = BashOperator(
        task_id='run_python_app_with_args_using_bash',
        bash_command=f'python /Users/itversity/Projects/Internal/bootcamp/itversity-material/mastering-airflow/apps/04_hello_world.py {username} ',
    )

    run_this


if __name__ == "__main__":
    dag.cli()
