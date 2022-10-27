# Setup Airflow Environment using Docker

## Clone the repository

Make sure to clone the **mastering-airflow** repository. Here is the command for your reference.

```shell
git clone https://github.com/itversity/mastering-airflow.git
```

It will create a folder by name **mastering-airflow**. Make sure it contain folder by name **airflow-docker**.

## Review Docker Compose File

Let us review the changes that are made on top of original **docker-compose.yaml**.
* We have added network so that we can integrate other docker based components with airflow for our learning purpose.
* We have updated the mount folders so that data is available as part of the docker containers in which airflow components are running.
* We have added **PYTHONPATH** as part of environment variables so that dags and python applications are decoupled. 
  * This will facilitate us to develop Python applications separately from DAGs.
  * Also we will be able to import Python modules that are available under **PYTHONPATH** as part of Python programs which contain DAG logic.

## Setup Data Set

Let us make sure that we copy **data** folder with **retail_db** to **airflow-docker**.
* This will expose **data** folder as part of docker containers.
* We can validate by running below command once Airflow is started using docker.

```shell
docker-compose exec airflow-webserver ls -ltr data
docker-compose exec airflow-webserver find data
```

## Setup Development Folders

Let us ensure that we have setup development folders properly to develop application code.
* As part of project directory **mastering-airflow**, make sure to create a folder by name **dev**.
* In that make sure to create folders by name **apps** and **dags**.
* **apps** have actual application with business logic where as **dags** will contain the logic related to Airflow DAGs.
* Also make sure **dags** and **apps** folders exists as part of **airflow-docker** folder.
```shell
# Run this command as part of airflow-docker folder
mkdir -p ./dags ./plugins ./logs ./apps
```
* These will be mounted on to the docker containers on which Airflow components are going to run.

## Setup Python Virtual Environment

Let us go ahead and setup local Python Virtual Environment to take care of developing applications as well DAGs.

```shell
# Make sure to run this command as part of mastering-airflow folder
python3 -m venv af-venv

# Activate Virtual Environment
source af-venv/bin/activate
pip install --upgrade pip

# Install OS Modules related to psycopg2
sudo apt-get install libpq-dev

# Setup Airflow
export AIRFLOW_VERSION=2.2.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Install additional dependencies
pip install -r requirements.txt
```

## Create Docker Network

Let us create external docker network before launching Airflow using Docker.
* You can run `docker network ls` command to review existing docker networks.
* You can run `docker network create itvdelabnw` to create custom network on which all the docker containers related to learning airflow are goint to run.

## Start Airflow using Docker

Let us start Airflow using Docker over the network created as part of previous lecture.
* Make sure to add **AIRFLOW_UID** to **.env** file.

```shell
echo -e "AIRFLOW_UID=$(id -u)" > airflow-docker/.env
```

* We will run `docker-compose up` command from the project directory **mastering-airflow** in detach mode.

```shell
docker-compose -f airflow-docker/docker-compose.yaml up -d --build
```

* Make sure to confirm whether all the processes are up and healthy or not using the below command.

```shell
docker-compose -f airflow-docker/docker-compose.yaml ps
```

* You can also validate whether all the folders are mounted or not using below commands.

```shell
docker-compose -f airflow-docker/docker-compose.yaml exec airflow-webserver ls -ltr data
docker-compose -f airflow-docker/docker-compose.yaml exec airflow-webserver find data
```

## Validate Web UI

Let us go through the Web UI and make sure that we can login.


## Develop First DAG

Let us go ahead and deploy our first DAG using Python Operator.

```python
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
```

## Deploy and Validate First DAG.
Let us deploy and validate the DAG developed using Python Operator.
* Make sure to copy the Python script to **dags** folder with in **airflow-docker** folder.
* Restart Airflow Webserver as well as Scheduler to see the DAG immediately.
```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  restart airflow-webserver airflow-scheduler

docker-compose -f airflow-docker/docker-compose.yaml ps
```
* Enable DAG and see if it will run successfully or not.


