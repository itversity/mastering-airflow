"""Example DAG demonstrating the usage of the DockerOperator to run python hello world application leveraging docker custom image"""

from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='09_custom_python_docker_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = DockerOperator(
        task_id='run_docker_custom_python_docker',
        image='mypython:latest',
        auto_remove=True,
        environment={
            'APP_ENV': 'dev'
        }
    )

    run_this


if __name__ == "__main__":
    dag.cli()
