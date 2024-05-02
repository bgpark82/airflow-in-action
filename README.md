# Airflow In Action

https://airflow.apache.org/docs/apache-airflow/stable/start.html

## Installation

1. Set home directory
   `~/airflow` by default
```bash
export AIRFLOW_HOME=${PWD}/airflow
```
2. Install Airflow
```bash
sh airflow-install.sh
```

3. run Airflow
- initialize the database
- create the default user
- start the web server
```bash
airflow standalone
```

4. access the web server
http://localhost:8080

## Configuration
1. airflow.cfg: [Configuration reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
2. Admin -> Configuration

## Production
- [Production Deployment](https://airflow.apache.org/docs/apache-airflow/stable/production-deployment.html)
```bash
airflow db migrate

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

airflow webserver --port 8080

airflow scheduler
```


## Commands
```bash
# run your first task instance
airflow tasks test example_bash_operator runme_0 2015-01-01
```
```bash
# run a backfill over 2 days
airflow dags backfill example_bash_operator \
    --start-date 2015-01-01 \
    --end-date 2015-01-02
```