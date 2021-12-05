from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

args = {
    'owner': 'itversity'
}


def hello_world(arg):
    print(f'Hello World from {arg}')


with DAG(
        dag_id='01_hello_world_python',
        default_args=args,
        schedule_interval='0 0 * * *',
        start_date=days_ago(2)
) as dag:
    hello_world_task = PythonOperator(
        task_id='hello_world_task',
        python_callable=hello_world,
        op_kwargs={
            'arg': 'itversity'
        }
    )

    hello_world_task

if __name__ == "__main__":
    dag.cli()
