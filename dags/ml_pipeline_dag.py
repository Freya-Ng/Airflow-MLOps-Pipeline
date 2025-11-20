from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable
import pandas as pd
import requests
import json
import os
import random

default_args = {
    'owner': 'ml_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# 1. CRAWL DATA FUNCTION (Giả lập)
def crawl_iris_data(**context):
    print("Starting data crawling...")
    # Lấy URL từ Variable (đã cài ở file setup)
    try:
        crawl_url = Variable.get("crawl_url")
    except:
        crawl_url = "http://example.com/data"
    
    print(f"Crawling data from: {crawl_url}")
    
    # Giả lập lưu file
    raw_path = "/opt/airflow/data/raw/iris_raw.csv"
    os.makedirs(os.path.dirname(raw_path), exist_ok=True)
    with open(raw_path, "w") as f:
        f.write("sepal_length,sepal_width,petal_length,petal_width,species\n")
        f.write("5.1,3.5,1.4,0.2,Iris-setosa\n")
    
    print(f"Data saved to {raw_path}")
    context['ti'].xcom_push(key='raw_data_path', value=raw_path)

# 2. ETL FUNCTION (Giả lập)
def process_etl(**context):
    print("Starting ETL process...")
    raw_path = context['ti'].xcom_pull(task_ids='crawl_data_task', key='raw_data_path')
    processed_path = "/opt/airflow/data/processed/iris_processed.csv"
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    
    # Copy data giả lập
    with open(raw_path, 'r') as f_in, open(processed_path, 'w') as f_out:
        content = f_in.read()
        f_out.write(content)
        
    print(f"ETL finished. Path: {processed_path}")
    context['ti'].xcom_push(key='processed_data_path', value=processed_path)

# 3. TRAINING FUNCTION (Giả lập)
def train_ml_model(**context):
    print("Training model...")
    # Lấy tham số từ Variable
    try:
        model_type = Variable.get("ml_model_type")
    except:
        model_type = "random_forest"
        
    print(f"Training with model type: {model_type}")
    
    # Giả lập độ chính xác ngẫu nhiên cao để pass
    accuracy = 0.95 
    print(f"Model Accuracy: {accuracy}")
    
    context['ti'].xcom_push(key='model_accuracy', value=accuracy)

# 4. VALIDATION FUNCTION
def validate_model(**context):
    print("Validating model...")
    accuracy = context['ti'].xcom_pull(task_ids='training_task', key='model_accuracy')
    
    try:
        threshold = float(Variable.get("accuracy_threshold"))
    except:
        threshold = 0.8
        
    if accuracy >= threshold:
        return 'deploy_task'
    else:
        return 'retrain_alert_task'

# 5. DEPLOY FUNCTION
def deploy_model(**context):
    print("Deploying model to API...")
    return "deployed_success"

# 6. MONITOR FUNCTION
def monitor_pipeline(**context):
    print("Monitoring system status: OK")

# 7. ALERT FUNCTION
def send_retrain_alert(**context):
    print("ALERT: Model accuracy is too low! Retraining needed.")

# 8. SUCCESS NOTIFICATION (Giả lập gửi mail)
def print_success_msg(**context):
    try:
        email = Variable.get("notification_email")
    except:
        email = "unknown@example.com"
        
    print(f"--------------------------------------------------")
    print(f"GIA LAP: Dang gui email thong bao thanh cong den: {email}")
    print(f"--------------------------------------------------")

# ĐỊNH NGHĨA DAG
with DAG(
    'mlpipeline_complete', 
    default_args=default_args,
    description='Complete ML Pipeline',
    schedule='@daily',  # <--- SỬA DÒNG NÀY (Dùng 'schedule' thay vì 'schedule_interval')
    catchup=False,
    tags=['ml', 'pipeline'],
) as dag:

    start = EmptyOperator(task_id='start')

    crawl_data_task = PythonOperator(
        task_id='crawl_data_task',
        python_callable=crawl_iris_data,
    )

    etl_task = PythonOperator(
        task_id='etl_task',
        python_callable=process_etl,
    )

    training_task = PythonOperator(
        task_id='training_task',
        python_callable=train_ml_model,
    )

    validate_task = BranchPythonOperator(
        task_id='validate_task',
        python_callable=validate_model,
    )

    deploy_task = PythonOperator(
        task_id='deploy_task',
        python_callable=deploy_model,
    )

    retrain_alert_task = PythonOperator(
        task_id='retrain_alert_task',
        python_callable=send_retrain_alert,
    )

    monitor_task = PythonOperator(
        task_id='monitor_task',
        python_callable=monitor_pipeline,
    )

    # Bước 8: Giả lập gửi mail bằng PythonOperator thay vì EmailOperator (để tránh lỗi SMTP)
    success_email = PythonOperator(
        task_id='success_email',
        python_callable=print_success_msg
    )

    end = EmptyOperator(task_id='end')

    # Định nghĩa luồng chạy (Workflow)
    start >> crawl_data_task >> etl_task >> training_task >> validate_task
    
    # Rẽ nhánh
    validate_task >> [deploy_task, retrain_alert_task]
    
    # Nhánh thành công
    deploy_task >> monitor_task >> success_email >> end
    
    # Nhánh thất bại (cần retrain)
    retrain_alert_task >> end