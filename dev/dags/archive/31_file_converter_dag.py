from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from archive.file_converter import convert

args = {
    'owner': 'airflow'
}


with DAG(
    dag_id='31_file_converter_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=10)
) as dag:
    convert_orders = PythonOperator(
        task_id='convert_orders',
        python_callable=convert,
        op_kwargs={
            'json_schemas_file_path': '/opt/airflow/apps/file_converter_schemas.json',
            'source_base_dir': '/opt/airflow/data/retail_db',
            'data_set_dir': 'orders',
            'target_base_dir': '/opt/airflow/data/retail_db_json'
        }
    )

    convert_orders
