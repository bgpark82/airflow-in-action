from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def print_ds(date, **kwargs):
    print(f"{date = }")
    print(f"{kwargs['abc'] =}")

def custom_macros(date):
    return date


dag = DAG(
    'create_kubernetes_cronjob',
    description='Create Kubernetes CronJob',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    user_defined_macros={
        "custom_macros_var": datetime.now(),
        "custom_macros_fun": custom_macros
    },
    catchup=False)

task = PythonOperator(
    task_id='print_ds',
    python_callable=print_ds,
    op_args=['{{ ds }}'],
    op_kwargs={'abc': '111'},
    dag=dag
)

bash = BashOperator(
    task_id='bash_op',
    # bash_command="echo 'execution date: {{ execution_date }}, random: {{ macros.random() }}'",
    bash_command="echo 'run duration : {{ custom_macros_fun(custom_macros_var) }}'",
    dag=dag
)

task >> bash
