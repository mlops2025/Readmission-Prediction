from airflow import DAG
import os
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from src.data_download import ingest_data
from src.unzip import unzip_file
from src.duplicate_missing_values import duplicates
from src.duplicate_missing_values import missingVal
from src.data_mapping import process_data_mapping

ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
DATA_PATH = os.path.join(ROOT_DIR, "data", "diabetic_data.csv")

# Define default_args
default_args = {
    'owner': 'MLOps_Team14',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#INITIALIZE THE DAG INSTANCE
dag = DAG(
    'DataPipeline',
    default_args = default_args,
    description = 'MLOps Data pipeline',
    schedule_interval = None,  # Set the schedule interval or use None for manual triggering
    catchup = False,
)

ingest_data_task = PythonOperator(
    task_id='ingest_data_task',
    python_callable=ingest_data,
    op_args=["https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"],
    dag=dag,
)

unzip_file_task = PythonOperator(
    task_id='unzip_file_task',
    python_callable=unzip_file,
    op_args=[ingest_data_task.output],
    dag=dag,
)

remove_duplicates_task = PythonOperator(
    task_id='remove_duplicates_task',
    python_callable= duplicates,
    op_args=[DATA_PATH],
    dag=dag,
)

missing_value_task = PythonOperator(
    task_id='missing_value_task',
    python_callable= missingVal,
    op_args= [remove_duplicates_task.output],
    dag=dag,
)

data_mapping_task = PythonOperator(
    task_id='data_mapping_task',
    python_callable= process_data_mapping,
    op_args= [missing_value_task.output],
    dag=dag,
)

ingest_data_task >> unzip_file_task >> remove_duplicates_task >> missing_value_task >> data_mapping_task
