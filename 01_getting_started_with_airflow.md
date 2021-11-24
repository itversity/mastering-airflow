## Setup Python Virtual Environment

```
python3 -m venv af-venv
```

## Install Airflow using Pip

```
source af-venv/bin/activate
pip install --upgrade pip

mkdir airflow

export AIRFLOW_HOME=`pwd`/airflow

AIRFLOW_VERSION=2.1.4
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

## Initialize with default sqlite3 database

```
airflow db init
airflow db upgrade
```

## Create Airflow admin user

```
airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org
```

## Start and Validate Airflow Components

```
airflow webserver --port 8080 -D

airflow scheduler -D
```

## Review the log files

```
ls -ltr airflow
ls -ltr airflow/airflow-webserver.*
ls -ltr airflow/airflow-scheduler.*
```

## Disable Airflow Examples

* Update airflow.cfg file to disable examples.
* Restart airflow webserver

```
cat $AIRFLOW_HOME/airflow-webserver.pid | xargs kill -9
airflow webserver -p 8080 -D 
```
