"""Example DAG demonstrating the usage of the KubernetesPodOperator to run python hello world application leveraging Kubernetes"""

from datetime import timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='11_hello_python_kubepod_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = KubernetesPodOperator(
        task_id='run_hello_world_using_python_kube',
        namespace='default',
        config_file='/Users/itversity/.kube/config',
        image='python:3.7',
        name='hello-world-python',
        cmds=["python", "-c", "print('Hello World')"],
        in_cluster=False,
        is_delete_operator_pod=True,
        get_logs=True
    )

    run_this


if __name__ == "__main__":
    dag.cli()
