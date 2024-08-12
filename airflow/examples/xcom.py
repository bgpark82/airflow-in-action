from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

# https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html#xcoms
dag = DAG(dag_id="xcom",
          start_date=datetime(2023, 8, 1),
          schedule_interval='0 23 * * *',
          catchup=False)

# 1. xcom basic
def push_function(**context):
    value_to_push = f"hello {datetime.now()}"
    curr_task_instance = context['ti']
    print(f"context={curr_task_instance}") # ti: acronym of task instance
    curr_task_instance.xcom_push(key='keyword', value=value_to_push)

def pull_function(**context):
    curr_task_instance = context['ti']
    # key = "return_value" by default
    pulled_value = curr_task_instance.xcom_pull(key='keyword', task_ids='push_task')
    print(f"recieved value: {pulled_value}")

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_function,
    provide_context=True,
    dag=dag
)

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_function,
    provide_context=True,
    dag=dag
)

def print_jinja_template(kwargs):
    print(f"jinja_template={kwargs}")

jinja_task = PythonOperator(
    task_id='print_jinja_template',
    python_callable=print_jinja_template,
    op_args=['{{ ds }}'], #pass the execution date using jinja template
    dag = dag
)

# 3. xcom with do_xcom_push
# data is pushed to xcom with key as "return_value" by default
def do_xcom_push_function():
    return f"do_xcom_push {datetime.now()}"

# xcom_pull uses key as "return_value" by default
def do_xcom_pull_function(**context):
    result = context['ti'].xcom_pull(task_ids='do_xcom_push_task')
    print(f"{result = }")

do_xcom_push_task = PythonOperator(
    task_id='do_xcom_push_task',
    python_callable=do_xcom_push_function,
    do_xcom_push=True,
    dag=dag
)

do_xcom_pull_task = PythonOperator(
    task_id='do_xcom_pull_task',
    python_callable=do_xcom_pull_function,
    dag=dag
)

# 3. xcom with jinja template
def jinja_push_function():
    return f'jinja hello {datetime.now()}'

# key = return_value by default
def jinja_pull_function(**context):
    result = context['templates_dict'].get("path")
    print(result)
    # result = context['ti'].xcom_pull(key="return_value", task_ids='jinja_push_task')
    # print(f"jinja pull={result}")

jinja_push_task = PythonOperator(
    task_id='jinja_push_task',
    python_callable=jinja_push_function,
    do_xcom_push=True,
    dag=dag
)

# 'path': '{{ task_instance.xcom_pull(task_ids="jinja_push_task", key="return_value") }}'
# path will contain data that jinja_push_task pushed to
jinja_pull_task = PythonOperator(
    task_id='jinja_pull_task',
    python_callable=jinja_pull_function,
    templates_dict={
        'path': '{{ task_instance.xcom_pull(task_ids="jinja_push_task", key="return_value") }}'
    },
    dag=dag
)

push_task >> pull_task >> jinja_task
do_xcom_push_task >> do_xcom_pull_task
jinja_push_task >> jinja_pull_task