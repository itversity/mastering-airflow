# Intertask Communication using XCom

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
