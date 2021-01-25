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
    tags=["example","insert","etl"] ) 

    #total_inserts = randrange(5,20)
    #insert_task = InsertSalesOperator(postgres_conn_id='mypsql',database='postgres',inserts=total_inserts)

def insert_values_sales():

    names = ['Paul', 'Andres', 'Aymaru','Julio','Stward']
    total_inserts = randrange(5,20)

    src = PostgresHook(postgres_conn_id='mypsql',schema='postgres')
    src_conn = src.get_conn()
    cursor = src_conn.cursor()    

    for i in range(0,total_inserts):
        rand_name = randrange(0,len(names))
        rand_amount = randrange(10000,500000)

        cursor.execute ("INSERT INTO sales(name,amount) VALUES ( %(name)s, %(amount)s )", {'name':names[rand_name],'amount':rand_amount})
 
    cursor.close()
    src_conn.commit()

hook_task = PythonOperator(
    task_id='insertIntoSales',
    python_callable=insert_values_sales,
    dag=dag
)