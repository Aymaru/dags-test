import pandas as pd
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

dag = DAG( 'postgresql_etl_example', 
    default_args=default_args, 
    description='A simple dag example using postgresql to insert into a table', 
    schedule_interval=timedelta(days=1), 
    start_date=days_ago(2), 
    tags=["example","etl"] ) 


def generate_report(**kwargs):
    #request = "SELECT COUNT(id) as count,SUM(amount) as total FROM sales;"
    request = "SELECT * FROM sales;"
    pg_hook  = PostgresHook(postgres_conn_id="mypsql",schema="postgres")
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    result = cursor.fetchall()
    print('generate and push report')
    print (result)
    #kwards['ti'].xcom_push(key='sales_report',value=result)
    #return {'count': result[0], 'total':result[1], 'date':datetime.now()}
    return result

def transform(**kwargs):
    ti = kwargs['ti']
    result = ti.xcom_pull(task_ids='generate_sales_report')
    df = pd.DataFrame(result)
    cantidad = df[0].count()
    monto = df[1].sum()
    print(df)
    print(cantidad)
    print(monto)
    return result



def log_report(**kwargs):
    ti = kwargs['ti']
    #report = ti.xcom_pull(task_ids='generate_sales_report')
    result = ti.xcom_pull(task_ids='transform_sales_report')
    report = {'count': result[0], 'total':result[1], 'date':datetime.now()}
    
    #request = "INSERT INTO reports(count,total,date) VALUES ( %(count)s, %(total)s, %(date)s );"
    #pg_hook  = PostgresHook(postgres_conn_id="mypsql",schema="postgres")
    #connection = pg_hook.get_conn()
    #cursor = connection.cursor()
    #cursor.execute(request, report)
    #connection.commit()

    print('pull and log report')
    print(report)
    return

task_generate_report = PythonOperator(
    task_id = 'generate_sales_report',
    python_callable=generate_report,
    provide_context=True,
    dag=dag
)

task_transform = PythonOperator(
    task_id = 'transform_sales_report',
    python_callable=transform,
    provide_context=True,
    dag=dag
)

task_log_report = PythonOperator(
    task_id = 'log_report',
    python_callable=log_report,
    provide_context=True,
    dag=dag
)

task_generate_report >> task_transform >> task_log_report