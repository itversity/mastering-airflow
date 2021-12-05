from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.models.baseoperator import chain
from archive.file_converter_sleep import convert

args = {
    'owner': 'airflow'
}

json_schemas_file_path = Variable.get('JSON_SCHEMAS_FILE_PATH')
source_base_dir = Variable.get('SOURCE_BASE_DIR')
target_base_dir = Variable.get('TARGET_BASE_DIR')
data_set_dirs = Variable.get('DATA_SET_DIRS').split(',')

with DAG(
    dag_id='34_file_converter_parallelism_dag',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(30),
    dagrun_timeout=timedelta(minutes=10),
    max_active_runs=1,
    concurrency=2
) as dag:
    convert_tasks = [
        PythonOperator(
            task_id=f'convert_{data_set_dir}',
            python_callable=convert,
            op_kwargs={
                'json_schemas_file_path': json_schemas_file_path,
                'source_base_dir': source_base_dir,
                'data_set_dir': data_set_dir,
                'target_base_dir': target_base_dir
            })
        for data_set_dir in data_set_dirs
    ]

    chain(convert_tasks)
