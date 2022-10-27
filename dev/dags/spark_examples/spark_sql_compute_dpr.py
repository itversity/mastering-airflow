from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.providers.ssh.operators.ssh import SSHOperator


args = {
    'owner': 'itversity'
}


with DAG(
    dag_id='dag_spark_daily_product_revenue',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    task_cleanup = SSHOperator(
        task_id='task_cleanup',
        ssh_conn_id='ssh_spark_gateway',
        command='spark-sql -f /home/itversity/data-engineering-on-gcp/scripts/daily_product_revenue/cleanup.sql '
    )

    task_convert_orders = SSHOperator(
        task_id='task_convert_orders',
        ssh_conn_id='ssh_spark_gateway',
        command='spark-sql -f /home/itversity/data-engineering-on-gcp/scripts/daily_product_revenue/file_format_converter.sql -d bucket_name=gs://airetail -d table_name=orders '
    )

    task_convert_order_items = SSHOperator(
        task_id='task_convert_order_items',
        ssh_conn_id='ssh_spark_gateway',
        command='spark-sql -f /home/itversity/data-engineering-on-gcp/scripts/daily_product_revenue/file_format_converter.sql -d bucket_name=gs://airetail -d table_name=order_items '
    )

    task_compute_daily_product_revenue = SSHOperator(
        task_id='task_compute_daily_product_revenue',
        ssh_conn_id='ssh_spark_gateway',
        command='spark-sql -f /home/itversity/data-engineering-on-gcp/scripts/daily_product_revenue/compute_daily_product_revenue.sql -d bucket_name=gs://airetail '
    )

    task_cleanup >> task_convert_orders
    task_cleanup >> task_convert_order_items

    task_convert_orders >> task_compute_daily_product_revenue
    task_convert_order_items >> task_compute_daily_product_revenue