"""Example DAG demonstrating the usage of the SSHOperator to run python application on remote server."""

from datetime import timedelta

from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='06_python_app_ssh_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = SSHOperator(
        task_id='run_python_app_with_args_using_ssh',
        ssh_conn_id='ssh_ec2_remote',
        command='/home/ec2-user/airflow-python-demo/apd-venv/bin/python /home/ec2-user/airflow-python-demo/file_converter.py ',
        environment={
            'SOURCE_BASE_DIR': '/home/ec2-user/data/retail_db',
            'dataset': 'order_items',
            'TARGET_BASE_DIR': '/home/ec2-user/data/retail_db_json'
        }
    )

    run_this


if __name__ == "__main__":
    dag.cli()
