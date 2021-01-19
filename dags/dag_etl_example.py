import json
from datetime import timedelta

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

# Default args for each task, args can be override on each task declaration
default_args = {
    'owner': 'smartnow',
    'depends_on_past': False,
    'email':['aymaru@smartnow.la'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'execution_time_out': timedelta(seconds=300)
}

# Using dag decorator to instantiate a DAG object, using the name function as unique id
@dag(default_args=default_args, schedule_interval=timedelta(days=1), start_date=days_ago(2))
def test_taskflow_api_etl():
    """
    ### TaskFlow API Example
    """

    # Using task decorator to instantiate a task, the operator is the function defined
    @task()
    def extract():
        """
        #### Extract task
        """
        data = '{"val_1": 231.52, "val_2": 675.52, "val_3": 347.98}'

        data_dict = json.loads(data)
        return data_dict

    # Using task decorator to instantiate a task, passing multiple_outputs params that were not define in default args
    @task(multiple_outputs=True)
    def transform(data_dict: dict):
        """
        #### Transform task
        """
        total_order_value = 0
        total_orders = 0


        for values in data_dict.values():
            total_order_value += values
            total_orders+=1

        return {"total_orders": total_orders, "total_order_value": total_order_value}

    @task()
    def load(total_orders: int, total_order_value: float):
        """
        #### Load task
        """

        print("Total orders processed: ", total_orders)
        print("Total order value is: ", total_order_value)

    data = extract()

    summary = transform(data)

    load(summary["total_orders"],summary["total_order_value"])

#test_etl_dag = test_taskflow_api_etl()
