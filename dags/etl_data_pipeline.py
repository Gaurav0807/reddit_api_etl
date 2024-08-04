from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

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
        'subreddit': ["bigdata"],
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

# def create_snowflake_schema_and_integration():
#     snowflake_hook = SnowflakeHook(
#         snowflake_conn_id='snowflake_reddit',
#         account=os.getenv('SNOWFLAKE_ACCOUNT'),
#         user=os.getenv('SNOWFLAKE_USER'),
#         password=os.getenv('SNOWFLAKE_PASSWORD'),
#         database=os.getenv('SNOWFLAKE_DATABASE'),
#         schema=os.getenv('SNOWFLAKE_SCHEMA'),
#         warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
#         role=os.getenv('SNOWFLAKE_ROLE')
#     )
#     conn = snowflake_hook.get_conn()
#     cursor = conn.cursor()
#     cursor.execute("SELECT 1")
#     print("Snowflake connection established.")

# snowflake_referesh_table = PythonOperator(
#     task_id='snowflake_referesh_table',
#     python_callable=create_snowflake_schema_and_integration,
#     dag=dag
# )



snowflake_referesh_table = SnowflakeOperator(
    task_id='snowflake_referesh_table',
    snowflake_conn_id="snowflake_reddit",
    sql="""alter external table snowflake_integration.ingestion_layer.reddit_data refresh;""",
    dag=dag,
    #parameters={'snowflake_db': snowflake_db_name, 'schema': schema, 'tablename': reddit_data}
)
# def create_snowflake_schema_and_integration():
    
#     snowflake_hook = SnowflakeHook(snowflake_conn_id='snowflake_reddit')
#     conn = snowflake_hook.get_conn()
#     cursor = conn.cursor()
#     cursor.execute("select 2")
#     print("Snowflake connection established.")

# snowflake_referesh_table = PythonOperator(
#     task_id='snowflake_referesh_table',
#     python_callable=create_snowflake_schema_and_integration,
#     dag=dag
# )


end_task = DummyOperator(task_id='end_task',dag=dag)



start_task >> extract >> upload_s3 >> snowflake_referesh_table >> end_task


