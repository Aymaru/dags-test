
from datetime import timedelta
from random import randrange
from time import sleep

# Import the DAG object, used to instantiate a dag
from airflow import DAG

# Import the Operators, needed to operate
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Default arguments that will get passed on to each operator
# These arguments can be override on each operator initialization
default_args = {
    'owner': 'smartnow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# DAG initialization
dag = DAG(
    'python_example',
    default_args=default_args,
    description='A simple dag example using python operator and bash operator',
    schedule_interval=timedelta(days=1), #Set to run everyday
    start_date=days_ago(2),
    tags=['example']
)

# Function executed by the PythonOperator on First Task
def generate_value():
    rand_num = randrange(10)
    return rand_num

# Task declaration using PythonOperator
first_task = PythonOperator(
    task_id='generate_value',
    python_callable=generate_value,
    dag=dag # task assign to dag
)

# Task declaration using BashOperator
last_task = BashOperator(
    task_id = 'print_date',
    bash_command='date', # this is the bash command executed
    dag=dag
)

#Function executed by PythonOperator, just sleep for a few seconds each
def sleep_function(sleep_time: int):
    print('Sleeping for',sleep_time,' seconds')
    sleep(sleep_time)
    return True

# Declaring multiple tasks
for i in range(0,3):
    sleep_time = randrange(1,8)
    task = PythonOperator(
        task_id='sleep_'+str(i), #dynamic generating the task id
        python_callable=sleep_function,
        op_kwargs={'sleep_time':sleep_time}, # Passing parameters on to the python function
        dag=dag
    )

    first_task >> task >> last_task #Setting the tasks dependencies.

