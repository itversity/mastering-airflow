"""Example DAG demonstrating the usage of the KubernetesPodOperator to run python hello world application leveraging Kubernetes"""

from datetime import timedelta

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='12_data_copier_kubepod_operator',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = KubernetesPodOperator(
        task_id='run_data_copier_using_kube',
        namespace='default',
        config_file='/Users/itversity/.kube/config',
        pod_template_file='/k8s/07-data-copier-kubepod.yaml',
        in_cluster=False,
        is_delete_operator_pod=True,
        get_logs=True
    )

    run_this


if __name__ == "__main__":
    dag.cli()
