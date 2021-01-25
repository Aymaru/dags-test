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
    tags=["example","insert"] ) 

def insert_values_sales():

    names = ['Paul', 'Andres', 'Aymaru','Julio','Stward']
    total_inserts = randrange(5,20)
    request = "INSERT INTO sales(name,amount) VALUES ( %(name)s, %(amount)s )"

    src = PostgresHook(postgres_conn_id='mypsql',schema='postgres')
    src_conn = src.get_conn()
    cursor = src_conn.cursor()    

    for i in range(0,total_inserts):
        rand_name = names[randrange(0,len(names))]
        rand_amount = randrange(10000,500000)
        print('Inserting into sales: name=%s,amount=%d' % (rand_name,rand_amount))

        cursor.execute (request, {'name':rand_name,'amount':rand_amount})
 
    cursor.close()
    src_conn.commit()

hook_task = PythonOperator(
    task_id='insertIntoSales',
    python_callable=insert_values_sales,
    dag=dag
)