from datetime import datetime
from pprint import pprint

from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(dag_id='callable', start_date=datetime(2024, 4, 10), schedule_interval="0 23 * * *", catchup=False)

# https://airflow.apache.org/docs/apache-airflow/1.10.3/howto/operator/python.html
"""
 'conn': None,
 'dag': <DAG: callable>,
 'dag_run': <DagRun callable @ 2024-08-12 22:46:57.767585+00:00: manual__2024-08-12T22:46:57.767585+00:00, state:running, queued_at: 2024-08-12 22:46:57.799023+00:00. externally triggered: True>,
 'data_interval_end': DateTime(2024, 8, 11, 23, 0, 0, tzinfo=Timezone('UTC')),
 'data_interval_start': DateTime(2024, 8, 10, 23, 0, 0, tzinfo=Timezone('UTC')),
 'ds_nodash': '20240812',
 'execution_date': <Proxy at 0xffffb4f38b80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'execution_date', DateTime(2024, 8, 12, 22, 46, 57, 767585, tzinfo=Timezone('UTC')))>,
 'expanded_ti_count': None,
 'inlets': [],
 'logical_date': DateTime(2024, 8, 12, 22, 46, 57, 767585, tzinfo=Timezone('UTC')),
 'macros': <module 'airflow.macros' from '/home/airflow/.local/lib/python3.9/site-packages/airflow/macros/__init__.py'>,
 'map_index_template': None,
 'next_ds': <Proxy at 0xffffb4f74b40 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'next_ds', '2024-08-12')>,
 'next_ds_nodash': <Proxy at 0xffffb4f78e80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'next_ds_nodash', '20240812')>,
 'next_execution_date': <Proxy at 0xffffb4f78a40 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'next_execution_date', DateTime(2024, 8, 12, 22, 46, 57, 767585, tzinfo=Timezone('UTC')))>,
 'outlets': [],
 'params': {},
 'prev_data_interval_end_success': None,
 'prev_data_interval_start_success': None,
 'prev_ds': <Proxy at 0xffffb4e85740 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'prev_ds', '2024-08-12')>,
 'prev_ds_nodash': <Proxy at 0xffffb4e858c0 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'prev_ds_nodash', '20240812')>,
 'prev_end_date_success': None,
 'prev_execution_date': <Proxy at 0xffffb4e859c0 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'prev_execution_date', DateTime(2024, 8, 12, 22, 46, 57, 767585, tzinfo=Timezone('UTC')))>,
 'prev_execution_date_success': <Proxy at 0xffffb4e85a80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'prev_execution_date_success', None)>,
 'prev_start_date_success': None,
 'run_id': 'manual__2024-08-12T22:46:57.767585+00:00',
 'task': <Task(PythonOperator): callable_task>,
 'task_instance': <TaskInstance: callable.callable_task manual__2024-08-12T22:46:57.767585+00:00 [running]>,
 'task_instance_key_str': 'callable__callable_task__20240812',
 'templates_dict': None,
 'test_mode': False,
 'ti': <TaskInstance: callable.callable_task manual__2024-08-12T22:46:57.767585+00:00 [running]>,
 'tomorrow_ds': <Proxy at 0xffffb4e85b40 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'tomorrow_ds', '2024-08-13')>,
 'tomorrow_ds_nodash': <Proxy at 0xffffb4e85c00 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'tomorrow_ds_nodash', '20240813')>,
 'triggering_dataset_events': {},
 'ts': '2024-08-12T22:46:57.767585+00:00',
 'ts_nodash': '20240812T224657',
 'ts_nodash_with_tz': '20240812T224657.767585+0000',
 'var': {'json': None, 'value': None},
 'yesterday_ds': <Proxy at 0xffffb4e85cc0 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'yesterday_ds', '2024-08-11')>,
 'yesterday_ds_nodash': <Proxy at 0xffffb4e85d80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0xffffb4f773a0>, 'yesterday_ds_nodash', '20240811')>}
"""
def callable_function(arg1, arg2, random, **kwargs):
    pprint(kwargs)
    print(f"{arg1 = }")
    print(f"{arg2 = }")
    pprint(f"{random = }")
    print(f"{kwargs['templates_dict']['execution_date']}")
    print(f"{kwargs['templates_dict']['custom_message']}")
    return 'whatever you return gets printed in the logs'

callable_task = PythonOperator(
    task_id='callable_task',
    provide_context=True, # pass airflow's execution context to python_callable, pass in addition set of keyword arguemnt w/ template_dict
    python_callable=callable_function,
    op_args=['pos arg1', 'pos arg2'], # positional argument
    op_kwargs={'random': 1}, # dictionary of argument
    templates_dict={
        'execution_date': '{{ ds }}',
        'custom_message': 'hello {{ ds }}'
    }, # pass extra keyword argument w/ provide_context option https://airflow.apache.org/docs/apache-airflow/1.10.3/macros.html
    dag=dag
)
