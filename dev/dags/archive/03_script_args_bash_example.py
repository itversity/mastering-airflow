"""Example DAG demonstrating the usage of the BashOperator to run bash command to invoke script with arguments."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='03_script_args_bash_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    username = Variable.get('USERNAME')
    run_this = BashOperator(
        task_id='run_shell_script_with_args_using_bash',
        bash_command=f'source /Users/itversity/Projects/Internal/bootcamp/itversity-material/mastering-airflow/scripts/03_run_script_with_args.sh {username} ',
    )

    run_this


if __name__ == "__main__":
    dag.cli()
