from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.bash import BashOperator


args = {
    'owner': 'itversity'
}


with DAG(
    dag_id='01_hello_world',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Hello World from task1"'
    )
    task2 = BashOperator(
        task_id='task2',
        bash_command='echo "Hello World from task2"'
    )
    task1 >> task2


if __name__ == '__main__':
    dag.cli()