# Understanding Basic Operators

## Running Shell Commands using BashOperator

Let us see how we can run shell commands as tasks with in a DAG using BashOperator.

```python
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.bash import BashOperator

args = {
  'owner': 'itversity'
}


with DAG(
  dag_id='01_shell_command.py',
  default_args=args,
  schedule_interval='0 0 * * *',
  start_date=days_ago(2)
) as dag:
    shell_command_task = BashOperator(
      task_id='shell_command_task',
      bash_command='echo "Hello World"'
    )
    shell_command_task

if __name__ == '__main__':
    dag.cli()
```
* Once the development is done, we should be able to deploy and validate.

## Triggering Shell Scripts using BashOperator

Let us see how we can trigger shell scripts using BashOperator. First, let us go through the high level steps.

* Develop a shell script to get number of files in a given folder (**retail_db**).
* We would like to pass the folder as a variable to the DAG. 
  * Let us go ahead and create variable by name `BASE_DIR` with value `/opt/airflow/data/retail_db`
* Develop a DAG with a task to trigger the shell script. Make sure to read the variable as part of the DAG logic.

* Here is the script to check if the **retail_db** folder contains files or not.

```shell
# get_file_count.sh
DIR_PATH=${1} # Fully qualified path have to be passed as argument.

find $DIR_PATH -type f|wc -l
```

* Here is the DAG with task to invoke shell script using **BashOperator**.

```python
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.bash import BashOperator
from airflow.models import Variable

args = {
  'owner': 'itversity'
}


base_dir = Variable.get('BASE_DIR')

with DAG(
  dag_id='01_shell_command.py',
  default_args=args,
  schedule_interval='0 0 * * *',
  start_date=days_ago(2)
) as dag:
    shell_command_task = BashOperator(
      task_id='shell_command_task',
      bash_command=f'source /opt/airflow/scripts/get_file_count.sh {base_dir} '
    )
    shell_command_task

if __name__ == '__main__':
    dag.cli()
```

## Running Python Applications using PythonOperator

## Separating DAGs and Python Applications

## Overview of Operators from External Providers

## Installing Provider for SSH Operator

## Create Docker Container for SSH Operator

## Running Applications remotely using SSHHook

## Creating SSH Connection using Airflow Web UI

## Managing Connections using Airflow CLI

## Running Applications remotely using SSH Connection

## Setup Retail data set

```shell
# use /home/ubuntu/environment

git clone https://github.com/dgadiraju/retail_db
rm -rf retail_db/.git
```

## Setup Postgres Database Server

```shell
docker run \
  --name retail_pg \
  --hostname retail_pg \
  -d \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=itversity \
  -v `pwd`/retail_db:/retail_db \
  --network itvdelabnw \
  postgres:13
```


## Setup Retail Database using Postgres

```shell
docker exec -i -t retail_pg psql -U postgres
```

```sql
CREATE DATABASE retail_db;
CREATE USER retail_user WITH ENCRYPTED PASSWORD 'itversity';

GRANT ALL ON DATABASE retail_db TO retail_user;
\q
```

```shell
docker exec -i -t retail_pg psql -U retail_user -d retail_db

# quit from Postgres
docker exec -i -t retail_pg \
  psql -U retail_user \
  -d retail_db \
  -f /retail_db/create_db_tables_pg.sql

docker exec -i -t retail_pg \
  psql -U retail_user \
  -d retail_db \
  -f /retail_db/load_db_tables_pg.sql

docker exec -i -t retail_pg \
  psql -U retail_user \
  -d retail_db \
  -c "SELECT count(*) FROM orders"
```

## Create Connection using Airflow

Let us go ahead and create connection using Airflow Web UI.
* We need following information to create connection.
  * Connection Id - Name of your choice. In my case, I am using **retail_db**.
  * Connection Type - **Postgres**
  * Host: **retail_pg**
  * Schema: **retail_db**
  * Login: **retail_user**
  * Password: **itversity**
  * Port: **5432**
* Before saving, we can test to confirm whether the information is correct or not.

## Managing Connections using Airflow CLI

## Getting Started with SQL Operator

