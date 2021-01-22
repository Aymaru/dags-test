from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'smartnow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
    'postgresql_example',
    default_args=default_args,
    description='A simple dag example using postgresql',
    schedule_interval=timedelta(days=1), #Set to run everyday
    start_date=days_ago(2),
    tags=['example']
)


def access_database():
    request = "SELECT * FROM public.company;" #"SELECT schema_name FROM information_schema.schemata;"
    pg_hook  = PostgresHook(postgre_conn_id="mypsql",schema="prueba")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    sources = cursor.fetchall()
    for source in sources:
        print(source)
    return sources

hooktask = PythonOperator(
    task_id='hookpostgresql',
    python_callable=access_database,
    dag=dag
    )
