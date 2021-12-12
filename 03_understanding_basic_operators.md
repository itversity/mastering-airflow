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
    dag_id='01_shell_command',
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
* Let us make sure we copy **retail_db** folder into **airflow-docker/data** folder.
* Develop a DAG with a task to trigger the shell script. Make sure to read the variable as part of the DAG logic.

Now let us go through the development and deployment of the DAG.
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
    dag_id='02_shell_script_with_args.py',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    shell_script_args_task = BashOperator(
        task_id='shell_script_args_task',
        bash_command=f'source /opt/airflow/scripts/03_understanding_basic_operators/get_file_count.sh {base_dir} '
    )

    shell_script_args_task


if __name__ == '__main__':
    dag.cli()
```

## Running Python Applications using PythonOperator

Let us get started with running Python Applications using Python Operator.
* **PythonOperator** is typically used to run Python applications which are supposed to be executed as part of Airflow Infrastructure.
* Here is the example code to get started with Python Operator. We can pass lambda function or invoke existing functions.

```python
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.python import PythonOperator


args = {
    'owner': 'itversity'
}

def call_me():
    print('Hello World from call_me function')

with DAG(
    dag_id='03_hello_world_python',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    hello_world_lambda_task = PythonOperator(
        task_id='hello_world_lambda_task',
        python_callable=lambda company: f'Hello World from {company} using lambda',
        op_kwargs={
            'company': 'ITVersity'
        }
    )
  
    call_me_task = PythonOperator(
        task_id='call_me_task',
        python_callable=call_me
    )
  
    hello_world_lambda_task >> call_me_task


if __name__ == '__main__':
    dag.cli()
```

## Separating DAGs and Python Applications

Let us understand how to separate Python programs with DAG code from the application logic.
* We will use **apps** folder to deploy Python code and we will continue to use **dags** folder to deploy DAG Code.
* We need to ensure that **apps** folder is added to **PYTHONPATH**.
* Once we add **apps** folder to **PYTHONPATH**, then we should be able to use Python modules in apps folder as part of our DAG code.

Let us go through the process of formal deployment of Python applications into the Airflow Environment.
* Develop Python code with name **hello_world.py** as part of **apps** folder under **dev**.

```python
def call_me_with_args(company):
    print(f'Hello World from {company} using call_me_with_args')
```

* Make sure to update **PYTHONPATH**. Also we need to ensure the **docker-compose.yaml** is udpated with **PYTHONPATH**.
* Develop the DAG Code to invoke **call_me_with_args** from the DAG.

```python
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.python import PythonOperator

from hello_world import call_me_with_args

args = {
    'owner': 'itversity'
}


with DAG(
    dag_id='04_hello_world_python_app',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2)
) as dag:
    hello_world_app_task = PythonOperator(
        task_id='hello_world_app_task',
        python_callable=call_me_with_args,
        op_kwargs={
            'company': 'ITVersity'
        }
    )
  
    hello_world_app_task


if __name__ == '__main__':
    dag.cli()
```

## Overview of Operators from External Providers

Let us get an overview of operators from external providers.
* As Airflow is setup using docker most of the commonly used external providers are already installed.
* We can use `airflow providers list` to see the list of providers.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  airflow providers list
```

* Providers typically expose operators which can be leveraged to create the tasks based on the requirements.
* Connect to Airflow bash using `docker-compose`.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  bash
```

* Launch Python and run this piece of code to understand how we can import operators such as SSHOperator, DockerOperator, etc.

```python
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.docker.operators.docker import DockerOperator                   
from airflow.providers.postgres.operators.postgres import PostgresOperator
```

## Overview of using SSH Operator

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

