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
* Airflow Variables are not encrypted by default. It is a good practice to make sure they are encrypted. Airflow Administrator team can take care of it, if it is recommended by development team.
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
* We will see Airflow Variables as part of DAGs which we are going to develop in subsequent modules or sections.

## Managing Variables using Airflow CLI

Let us understand how to manage airflow variables using Airflow CLI.
* If you setup Airflow locally, you should be able to run `airflow` commands directly.
* In case of Airflow on Docker, make sure to connect to bash using the following command.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  bash
```

* Now run the command `airflow -h` to see list of Airflow components that can be managed by CLI.
* We can use `airflow variables -h` to see the permitted operations on Airflow Variables via CLI.
* Here are the examples for some standard operations.

```shell
airflow variables list
airflow variables get SOURCE_BASE_DIR
airflow variables delete SOURCE_BASE_DIR
airflow variables set SOURCE_BASE_DIR /opt/airflow/data/retail_db
```

## Overview of Airflow Connections

Let us get an overview of Airflow Connections.
* Airflow Connections are similar to Airflow Variables. However, we typically used to preserve connectivity information.
* Here are some of the common scenarios where we use connections.
  * Connect to remote server via SSH.
  * Connect to remote database by passing server, port, schema or database, username, password, etc
* Here are the high level steps we typically follow with respect to connections.
  * Create connection using Airflow Web UI or CLI. Each connection will have unique connection id.
  * Use relevant operator while defining the task with connection id.
  * Operators such as SSHOperator, PostgresOperator, etc can leverage these connections.

## Creating Airflow Connections using Web UI

Let us understand how to create airflow connections using Web UI.
* Go to Admin and then go to Web UI.
* Create connection of type SSH with some dummy names.
* We cannot test unless we have a server and valid details to connect to it.
* For now let us save with out testing it.
* Airflow Connection details should be encrypted. It will be taken care by Airflow Administrators when the Airflow is setup.
* We will see more appropriate examples in subsequent modules.

## Managing Airflow Connections using Airflow CLI

Let us understand how to manage airflow connections using Airflow CLI.

* If you setup Airflow locally, you should be able to run `airflow` commands directly.
* In case of Airflow on Docker, make sure to connect to bash using the following ommand.

```shell
docker-compose -f airflow-docker/docker-compose.yaml \
  exec airflow-webserver \
  bash
```

* Now run the command `airflow -h` to see list of Airflow components that can be managed by CLI.
* We can use `airflow connections -h` to see the permitted operations on Airflow Connections via CLI.
* Here are the examples for some standard operations.

```shell
airflow connections list
airflow connections get ssh_demo
airflow connections delete ssh_demo
```
* We can also add connections using CLI. You can review the help to see what all details needs to be passed.

```shell
airflow connections add ssh_demo \
  --conn-type ssh \
  --conn-host dummy \
  --conn-login dummy \
  --conn-password dummy
```
