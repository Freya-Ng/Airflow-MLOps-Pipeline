from airflow.models import Variable, Connection
from airflow import settings
import os

def setup_ml_variables():
    """Thiết lập variables cho ML pipeline"""

    variables = {
        'ml_model_type': 'random_forest',
        'training_data_path': '/opt/airflow/data/processed/training_data.csv',
        'model_save_path': '/opt/airflow/data/models/',
        'test_size': '0.2',
        'random_state': '42',
        'accuracy_threshold': '0.8',
        'crawl_url': 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
        'notification_email': 'your-email-for-notification'
    }

    for key, value in variables.items():
        Variable.set(key, value)
        print(f"Variable {key} set to {value}")

def setup_ml_connections():
    """Thiết lập connections cho ML pipeline"""

    session = settings.Session()

    # Database connection for storing results
    db_conn = Connection(
        conn_id='ml_database',
        conn_type='postgres',
        host='localhost',
        login='ml_user',
        password='ml_password',
        port=5432,
        schema='ml_pipeline'
    )

    # API connection for model deployment
    api_conn = Connection(
        conn_id='ml_api',
        conn_type='http',
        host='https://api.mlservice.com',
        login='api_user',
        password='api_password'
    )

    try:
        session.add(db_conn)
        session.add(api_conn)
        session.commit()
        print("Connections created successfully")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("--- Bat dau setup ---")
    setup_ml_variables()
    setup_ml_connections()
    print("--- Hoan tat ---")