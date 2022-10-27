from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.ssh.operators.ssh import SSHOperator


args = {
    'owner': 'itversity'
}


with DAG(
    dag_id='spark_sql_using_ssh',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    task_current_date = SSHOperator(
        task_id='task_current_date',
        ssh_conn_id='ssh_spark_gateway',
        command='spark-sql -e "SELECT current_date" '
    )