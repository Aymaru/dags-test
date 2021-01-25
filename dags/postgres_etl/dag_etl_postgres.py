from datetime import datetime, timedelta
from random import randrange
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'smartnow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=30)
}

dag = DAG( 'postgresql_insert_example', 
    default_args=default_args, 
    description='A simple dag example using postgresql to insert into a table', 
    schedule_interval=timedelta(days=1), 
    start_date=days_ago(2), 
    tags=["example","etl"] ) 


def generate_report():
    request = "SELECT COUNT(id),SUM(amount) FROM sales;"
    pg_hook  = PostgresHook(postgres_conn_id="mypsql",schema="postgres")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    sources = cursor.fetchall()
    for source in sources:
        print (source)
    return

# def log_report():
#     return

task_generate_report = PythonOperator(
    task_id = 'generate_sales_report'
    python_callable=generate_report,
    provide_context=True,
    dag=dag
)


# task_log_report = PythonOperator(
#     task_id = 'log_report',
#     python_callable=log_report,
#     provide_context=True,
#     dag=dag
# )