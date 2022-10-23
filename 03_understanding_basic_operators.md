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

Let us go through the details of defining tasks using SSH Operator.
* One of the common pattern with respect to running applications using Airflow is to run applications remotely.
* We can use **SSHOperator** to run applications on remote servers.
* We can run shell scripts as well as applications developed using programming languages such as Python.

Here are the high level steps of defining tasks using SSH Operator.
* Make sure to have SSH Provider is installed as part of Python environment.
* We need to have a remote server accessible via SSH.
* We can define connection either by using SSHHook as part of DAG Code or by creating connection as part of Airflow Environment and use it as part of the DAG Code.
* We need to ensure we have a shell script or valid command which can be run on remote server
* We can then define task as part of the DAG Code using `SSHOperator`.

## Installing Provider for SSH Operator

We can validate whether provider exists for SSH Operator or not and then install using `pip` if it does not exists.
* Here is the command to check if SSH Provider is installed or not.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  airflow providers list
```

* If it does not exist, we can install using following command.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  pip install apache-airflow-providers-ssh
```

* We can launch Python and then validate by running `from airflow.providers.ssh.operators.ssh import SSHOperator`.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  python
```

## Create Docker Container for SSH Operator

Let us go ahead and setup Docker Container with SSH so that we can define task using SSHOperator.
* Create docker container using SSH image with in the network **itvdelabnw**.
* Go to **dockers/sshdemo** and run following commands to create the container.

```shell
docker build -t pythonapp .

docker run \
  --name pythonapp \
  --hostname pythonapp \
  --network itvdelabnw \
  -p 8888:8888 \
  -d \
  pythonapp
```

## Validate SSH Connectivity between Airflow and Pythonapp

As the container is created with pythonapp, let us ensure that Airflow servers (containers) can talk to the new container or server.
* Connect to the Airflow Webserver via bash.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  bash
```

* Run SSH Command to confirm the connectivity to pythonapp.

```shell
ssh itversity@pythonapp

# exit and then run below command from Airflow container or server
ssh itversity@pythonapp "hostname -f"
```

## Airflow DAG with task using SSHOperator and SSHHook

Let us understand how to use combination of SSHOperator and SSHHook to develop the tasks to run applications or commands on remote server.
* Keep in mind that this is not the common way as we might have to hard code the password and other details.
```python
from datetime import timedelta

from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.utils.dates import days_ago
from airflow.providers.ssh.hooks.ssh import SSHHook

args = {
    'owner': 'airflow',
}


ssh_hook = SSHHook(
    remote_host='pythonapp',
    username='itversity',
    password='itversity'
)

with DAG(
    dag_id='05_command_ssh_hook',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = SSHOperator(
        task_id='ssh_command_task',
        ssh_hook=ssh_hook,
        command='hostname -f',
    )

    run_this


if __name__ == "__main__":
    dag.cli()

```
## Creating SSH Connection using Airflow Web UI

Let us go ahead and create SSH Connection using Airflow Web UI.
* Connection Id: ssh_pythonapp
* Host: pythonapp
* Login: itversity
* Password: itversity

Make sure to click on save to add the connection. You can try validating the connection details by clicking on Test.
* If the test fails, ignore and save.

## Airflow DAG with task using SSHOperator and connection id

Let us understand how to use combination of SSHOperator and Connection added using Airflow Web UI to develop the tasks to run applications or commands on remote server.

```python
from datetime import timedelta

from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='06_command_ssh_connection',
    default_args=args,
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    dagrun_timeout=timedelta(minutes=60),
) as dag:
    run_this = SSHOperator(
        task_id='ssh_command_task',
        ssh_conn_id='ssh_pythonapp',
        command='hostname -f',
    )

    run_this


if __name__ == "__main__":
    dag.cli()

```

## Overview of Airflow Tasks and Operators to run Queries

Let us get an overview of Airflow Tasks and Operators to run Queries.
* There are providers for most of the common databases such as Postgres, MySQL, etc.
* The providers of respective databases provide operators to connect to the database and run queries.
* We need to pass database connectivity information to these operators while defining the tasks. We can leverage connections to pass the connectivity information.
* If you setup Airflow using Docker, most of the providers for common databases are already installed.
* We can review the providers using Airflow Web UI by going to providers as part of Admin drop down menu.
* To connect to most of the databases we need following information:
  * Host IP or DNS Alias on which Database Server is running
  * Port number on which Database Server is running
  * Schema (Oracle) or Database Name (Postgres, MySQL, etc) in which the tables that are in the scope of requirements are available.
  * Username - the user should have relevant permissions on the tables against which we would like to perform operations.
  * Password
* Here are the high level steps that are involved in defining task using Operator to connect to the database.
  * Make sure relevant provider is installed.
  * Make sure there is a database server with right database or schema exists. Also, we need to ensure that there is a user who have access to the underlying tables.
  * Validate connectivity between the Airflow servers and the server on which database is running.
  * Create connection object using appropriate connection type and relevant information.
  * Develop the DAG with task using relevant operator to run queries against underlying database.
* We will take care of demo using Postgres as the target database.

## Setup Provider for PostgresOperator

Go to the Airflow Web UI and confirm whether Provider for Postgres is installed or not.
* If the provider is not installed, use below `pip` command to setup provider to interact with Postgres Databases.

```shell
python3 -m pip install apache-airflow-providers-postgres
```

* You can also validate by running this Python code to confirm whether it can be used as part of developing DAGs.

```python
from airflow.providers.postgres.operators.postgres import PostgresOperator
```

## Setup Retail data set

We need to have a Postgres Database as part of Postgres Database Server with tables and data. Make sure to clone this repository so that we can setup required databases and tables later.

```shell
# use /home/ubuntu/environment

git clone https://github.com/dgadiraju/retail_db
rm -rf retail_db/.git
```

## Setup Postgres Database Server

Let us go ahead and setup Postgres Database Server as part of itvdelabnw network. We will eventually create **retail_db** database along with tables using the repository cloned as part of last lecture.

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

As the Postgres Database Server is up and running using Docker, let us go ahead and setup the following:
* Database: **retail_db**
* User: **retail_user**
* Grant all permissions on **retail_db** database to **retail_user**.
* Make sure to create tables in the database and also load the data into the tables using provided scripts.

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

## Develop Airflow DAG using PostgresOperator

```python
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

```
