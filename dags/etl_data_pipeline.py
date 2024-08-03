from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.etl_pipeline import etl_pipeline
from etl.aws_s3_pipeline import upload_s3_pipeline

output_name = datetime.now().strftime("%Y%m%d")

default_args = {
    'owner': 'Gaurav Rawat',
    'depends_on_past' :False,
    'start_date': datetime(2024,8,1),
    'retries':1,
    'retries_delay': timedelta(minutes=5),
}

dag = DAG(
    'Reddit_ETL_Pipeline',
    default_args=default_args,
    description="Reddit ETL Pipeline",
    schedule_interval=timedelta(days=1)
)

start_task = DummyOperator(task_id ="start_task",dag=dag)


extract = PythonOperator(
    task_id='reddit_extract',
    python_callable=etl_pipeline,
    op_kwargs={
        'output_name': f'{output_name}',
        'subreddit': ["bigdata","dataengineering","snowflake","databricks"],
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

upload_s3 = PythonOperator(
    task_id='s3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)


end_task = DummyOperator(task_id='end_task',dag=dag)

start_task >> extract >> upload_s3 >> end_task


