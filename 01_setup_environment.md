# Setup Environment

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

# Install OS Modules related to psycopg2
sudo apt-get install libpq-dev

# Install dependencies
pip install -r requirements.txt
```

## Create Docker Network

Let us create external docker network before launching Airflow using Docker.
* You can run `docker network ls` command to review existing docker networks.
* You can run `docker network create itvdelabnw` to create custom network on which all the docker containers related to learning airflow are goint to run.

## Start Airflow using Docker

Let us start Airflow using Docker over the network created as part of previous lecture.
* We will run `docker-compose up` command from the project directory **mastering-airflow** in detach mode.

```shell
docker-compose -f airflow-docker/docker-compose.yaml up -d --build
```

* Make sure to confirm whether all the processes are up and healthy or not using the below command.

```shell
echo -e "AIRFLOW_UID=$(id -u)" > airflow-docker/.env
docker-compose -f airflow-docker/docker-compose.yaml up ps
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

```

## Deploy and Validate First DAG.



