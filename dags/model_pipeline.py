from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.email import send_email
from datetime import datetime, timedelta
import os
import logging
import sys

from src.model_development.model_development_evalution import run_model_development

# Airflow root directory (where the project is mounted)
AIRFLOW_ROOT = "/opt/airflow"

# Add src to Python path
SRC_PATH = os.path.join(AIRFLOW_ROOT, "src")
sys.path.append(SRC_PATH)

default_args = {
    'owner': 'MLopsProjectGroup14',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}


dag_2 = DAG(
    'ModelDevelopmentPipeline',
    default_args=default_args,
    description='DAG for running model development with MLflow',
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
)

def run_model_development_task(**kwargs):

    TRAIN_PATH = "train_data.csv"
    TEST_PATH = "test_data.csv"
    
    final_metrics = run_model_development(TRAIN_PATH, TEST_PATH, max_attempts=3)
    
    logging.info(f"Final model metrics: {final_metrics}")
    kwargs['ti'].xcom_push(key='final_metrics', value=final_metrics)
    
    if all(metric >= 0.7 for metric in final_metrics.values()):
        logging.info("Model development successful: All metrics are above 0.7")
    else:
        logging.warning("Model development completed, but not all metrics are above 0.7")

model_development_task = PythonOperator(
    task_id='run_model_development',
    python_callable=run_model_development_task,
    provide_context=True,
    dag=dag_2,
)

model_development_task