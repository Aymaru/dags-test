from datetime import datetime, timedelta
from random import randrange
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from operators import SalesInsertOperator

default_args = {
    'owner': 'smartnow',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=30)
}

# with DAG( 'postgresql_insert_example', default_args=default_args, description='A simple dag example using postgresql to insert into a table', schedule_interval=timedelta(days=1), start_date=days_ago(2), tags=["example","insert","etl"] ) as dag :
#     src = PostgresHook(postgres_conn_id='mypsql',schema='postgres')
#     src_conn = src.get_conn()
#     cursor = src_conn.cursor()

#     names = ['Paul', 'Andres', 'Aymaru','Julio','Stward']
#     total_inserts = randrange(5,20)

#     for i in range(0,total_inserts):
#         rand_name = randrange(0,len(names))
#         rand_amount = randrange(10000,500000)

#         cursor.execute ("INSERT INTO sales(name,amount) VALUES ( %(name)s, %(amount)s )", {'name':names[rand_name],'amount':rand_amount})
with DAG( 'postgresql_insert_example', default_args=default_args, description='A simple dag example using postgresql to insert into a table', schedule_interval=timedelta(days=1), start_date=days_ago(2), tags=["example","insert","etl"] ) as dag :
    total_inserts = randrange(5,20)
    insert_task = InsertSalesOperator(postgres_conn_id='mypsql',database='postgres',inserts=total_inserts)
