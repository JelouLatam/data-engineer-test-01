import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.pipeline.orchestrator import main

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='airbnb_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id='run_pipeline',
        python_callable=main,
    )
