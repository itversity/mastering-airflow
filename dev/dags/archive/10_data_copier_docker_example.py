"""Example DAG demonstrating the usage of the DockerOperator to run python data copier application leveraging docker custom image"""

from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount


args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='10_data_copier_docker_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = DockerOperator(
        task_id='run_data_copier_python_docker',
        docker_url='tcp://ec2-54-161-238-212.compute-1.amazonaws.com:2375',
        image='data-copier:latest',
        network_mode='container:retail',
        auto_remove=True,
        mounts=[
            Mount(
                source='/home/ec2-user/data/retail_db_json',
                target='/retail_db_json',
                type='bind'
            )
        ],
        command=['data_copier', 'orders,order_items'],
        environment={
            'BASE_DIR': '/retail_db_json',
            'DB_HOST': 'retail',
            'DB_PORT': '5432',
            'DB_NAME': 'retail_db',
            'DB_USER': 'retail_user',
            'DB_PASS': 'itversity'
        }
    )

    run_this


if __name__ == "__main__":
    dag.cli()
