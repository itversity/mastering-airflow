"""Example DAG demonstrating the usage of the BashOperator to run bash command."""

from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='02_script_bash_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:

    run_this = BashOperator(
        task_id='run_shell_script_using_bash',
        bash_command='source /Users/itversity/Projects/Internal/bootcamp/itversity-material/mastering-airflow/scripts/02_run_script.sh ',
    )

    run_this


if __name__ == "__main__":
    dag.cli()
