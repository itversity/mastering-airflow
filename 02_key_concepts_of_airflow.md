# Key Concepts of Airflow

## Overview of Airflow Documentation

Let us get an overview of Airflow Documentation. It is available under https://airflow.apache.org.

## Airflow DAGs and Tasks
Let us get an overview of Airflow DAGs and Tasks.
* DAG stands for Directed Acyclic Graph. We define workflows using Python programs leveraing DAG API.
* A DAG consists of tasks in appropriate order depending upon the requirements.
* Here are some of the common patterns with respect to defining tasks as part of DAGs.
  * Serial tasks
  * Parallel and then join tasks
  * We can mix and match and develop complex workflows in the form of DAGs using tasks.
* Each task is defined using specific type of operator depending up on the requirements.

## Overview of Airflow Executors
As Airflow Executors is infrastructural concept, for now we will only get an overview of it.
* Let's review the architecture diagram and go through the details of Airflow Executors.
* When we setup Airflow locally, the default executor is **SequentialExecutor**.
* In production we typically use **CeleryExecutor** or **KubernetesExecutor**.
* When we setup Airflow using Docker, it uses **CeleryExecutor**. You can review the **docker-compose.yaml** to get more details.

## Overview of Airflow Scheduler
Let us get an overview of Airflow Scheduler.
* Cron based syntax - eg: `0 0 * * *`
* @ syntax - eg: `@daily`
* Custom Calendars

## Overview of Operators

Let us get an overview of Operators.
* Each task is defined using relevant Operator class. Here are some of the common operators.
  * BashOperator
  * PythonOperator
  * SSHOperator
  * SQLOperator
  * DockerOperator
  * and many more
* We can install appropriate plugins provided by relevant vendors to use 3rd party operators.
* We will go through the details of several important operators as part of the course.
* Depending up on the type of operator, the arguments change.

## Overview of Airflow CLI

We can manage most of the Airflow components using Airflow CLI.
* DAGs
* Variables
* Connections
* and more

To use Airflow CLI via Docker Compose, we can leverage this command. Also official Airflow provides shell script to interact with Airflow CLI via docker.

```shell
# Get help
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  airflow -h
 
# Get list of deployed dags
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  airflow dags list
```

## Managing DAGs using Airflow CLI

Let us understand how to manage DAGs using Airflow CLI.

## Airflow Variables

Let us get an overview of Airflow Variables.
* Airflow Variables are primarily used to define reusable application level settings across tasks with in a DAG or across multiple DAGs.
* We can define variables using Web UI or CLI.
* Let us define Airflow Variable using Airflow Web UI and understand how to access it using Airflow APIs.
  * Key: **SOURCE_BASE_DIR**
  * Value: **/opt/airflow/data/retail_db**
* Now let us launch Python CLI as part of Docker and validate by using below code snippet.

```python
# Luanch Python CLI - docker-compose -f airflow-docker/docker-compose.yaml exec airflow-webserver python
from airflow.models import Variable
Variable.get('SOURCE_BASE_DIR')
```

* We can also manage Airflow Variables using `Variable` from `airflow.models` module. It exposes functions such as `set`, `delete`, etc on top of `get`.
* We will see Airflow Variables as part of DAGs which we are going develop in subsequent modules or sections.

## Managing Variables using Airflow CLI

## Overview of Airflow Connections

## Intertask Communication using XCom - return value

## Overview of XCom pull and push
