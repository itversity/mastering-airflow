from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

from archive.file_converter import convert

args = {
    'owner': 'airflow'
}

json_schemas_file_path = Variable.get('JSON_SCHEMAS_FILE_PATH')
source_base_dir = Variable.get('SOURCE_BASE_DIR')
target_base_dir = Variable.get('TARGET_BASE_DIR')

with DAG(
    dag_id='32_file_converter_variables_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=10)
) as dag:
    convert_orders = PythonOperator(
        task_id='convert_orders',
        python_callable=convert,
        op_kwargs={
            'json_schemas_file_path': json_schemas_file_path,
            'source_base_dir': source_base_dir,
            'data_set_dir': 'orders',
            'target_base_dir': target_base_dir
        }
    )

    convert_orders
