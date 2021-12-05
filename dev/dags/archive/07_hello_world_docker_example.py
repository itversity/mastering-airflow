"""Example DAG demonstrating the usage of the DockerOperator to run hello world application leveraging docker"""

from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='07_hello_world_docker_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = DockerOperator(
        task_id='run_hello_world_using_docker',
        image='hello-world',
        auto_remove=True
    )

    run_this


if __name__ == "__main__":
    dag.cli()
