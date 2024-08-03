from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past' :False,
    'start_date': datetime(2024,6,14),
    'retries':1,
    'retries_delay': timedelta(minutes=5),
}

dag = DAG(
    'Basic_Dag',
    default_args=default_args,
    description="Airflow DAG Trigger with Lambda Function",
    schedule_interval=timedelta(days=1)
)

start_task = DummyOperator(task_id ="start_task",dag=dag)

def hello():
    print("Hello Airflow DAG")


python_task = PythonOperator(
    task_id = 'python_task',
    python_callable=hello,
    dag=dag,
)




end_task = DummyOperator(task_id='end_task',dag=dag)

start_task >> python_task >> end_task