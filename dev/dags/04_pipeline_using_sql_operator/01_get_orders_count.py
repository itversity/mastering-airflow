from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.postgres.operators.postgres import PostgresOperator


args = {
    'owner': 'itversity'
}

with DAG(
    dag_id='01_get_orders_count',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    get_orders_count_task = PostgresOperator(
        task_id='get_table_count_task',
        postgres_conn_id='retail_db',
        sql='SELECT count(*) FROM orders'
    )

    get_orders_count_task


if __name__ == '__main__':
    dag.cli()
