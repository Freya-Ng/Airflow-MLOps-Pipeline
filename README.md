# Airflow ML Orchestration

A production-ready machine learning pipeline orchestration system built with Apache Airflow, demonstrating end-to-end MLOps practices including data collection, transformation, model training, validation, conditional deployment, and continuous monitoring.

## 🚀 Features

- **Automated Data Ingestion**: Scheduled data crawling from external sources
- **ETL Pipeline**: Data preprocessing and transformation workflows
- **ML Model Training**: Configurable model training with hyperparameter management
- **Intelligent Validation**: Branching logic with accuracy threshold checks
- **Conditional Deployment**: Automated deployment only when quality metrics are met
- **Monitoring & Alerting**: Real-time pipeline health checks and email notifications
- **Docker-Compose Setup**: Fully containerized with CeleryExecutor, Redis, and PostgreSQL
- **Variable Management**: Centralized configuration via Airflow Variables

## 🏗️ Architecture

### Pipeline Workflow Visualization

![ML Pipeline Architecture](images/ml_pipeline_dag.png)

The pipeline follows a complete ML lifecycle with intelligent branching logic:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Crawl     │────▶│     ETL     │────▶│   Training  │────▶│ Validation  │
│    Data     │     │  Processing │     │    Model    │     │   (Branch)  │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                     │
                                            ┌────────────────────────┴─────────┐
                                            │                                  │
                                            ▼                                  ▼
                                    ┌─────────────┐                  ┌─────────────┐
                                    │   Deploy    │                  │   Retrain   │
                                    │    Model    │                  │    Alert    │
                                    └──────┬──────┘                  └──────┬──────┘
                                           │                                │
                                           ▼                                │
                                    ┌─────────────┐                         │
                                    │  Monitoring │                         │
                                    └──────┬──────┘                         │
                                           │                                │
                                           ▼                                │
                                    ┌─────────────┐                         │
                                    │   Success   │                         │
                                    │    Email    │                         │
                                    └──────┬──────┘                         │
                                           │                                │
                                           └────────────┬───────────────────┘
                                                        ▼
                                                   ┌─────────┐
                                                   │   End   │
                                                   └─────────┘
```

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.8+
- 4GB+ RAM available for Docker

## 🔧 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/airflow-ml-orchestration.git
cd airflow-ml-orchestration
```

### 2. Set up environment variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configurations
```

### 3. Initialize Airflow

```bash
# Create necessary directories
mkdir -p ./logs ./plugins ./config

# Set the Airflow UID (Linux/Mac)
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Windows PowerShell
echo "AIRFLOW_UID=50000" >> .env
```

### 4. Start the services

```bash
# Initialize the database
docker-compose up airflow-init

# Start all services
docker-compose up -d
```

### 5. Access Airflow Web UI

- **URL**: http://localhost:8080
- **Username**: `airflow`
- **Password**: `airflow`

### 6. Configure Pipeline Variables

Run the setup script to initialize variables:

```bash
docker-compose exec airflow-webserver python /opt/airflow/dags/setup_ml_pipeline.py
```

Or manually set variables in the Airflow UI:
- Go to Admin → Variables
- Add the required variables (see Configuration section)

## ⚙️ Configuration

### Required Airflow Variables

| Variable Name | Description | Default Value |
|--------------|-------------|---------------|
| `ml_model_type` | Type of ML model | `random_forest` |
| `accuracy_threshold` | Minimum accuracy for deployment | `0.8` |
| `crawl_url` | Data source URL | - |
| `notification_email` | Email for alerts | - |

## 📁 Project Structure

```
.
├── dags/                          # Airflow DAG definitions
│   ├── ml_pipeline_dag.py        # Main ML pipeline DAG
│   └── setup_ml_pipeline.py      # Setup script for variables
├── plugins/                       # Custom Airflow plugins
├── data/                         # Data storage
│   ├── raw/                      # Raw data from crawling
│   ├── processed/                # Processed data after ETL
│   └── model/                    # Trained models
├── config/                       # Configuration files
│   └── airflow.cfg              # Airflow configuration
├── scripts/                      # Utility scripts
├── tests/                        # Unit tests
├── docs/                         # Documentation
├── docker-compose.yaml           # Docker orchestration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🔄 Pipeline Workflow

1. **Data Crawling**: Fetches data from configured source
2. **ETL Processing**: Cleans and transforms raw data
3. **Model Training**: Trains ML model with configured parameters
4. **Validation**: Checks if model meets accuracy threshold
5. **Deployment** (if passed): Deploys model to production
6. **Monitoring**: Tracks system health and performance
7. **Notification**: Sends success/failure alerts

## 🧪 Testing

Basic validation tests ensure the DAG loads without errors:

```bash
# Run DAG validation tests
docker-compose exec airflow-webserver pytest tests/ -v
```

The test suite validates:
- DAG can be loaded without import errors
- All tasks are present in the DAG structure  
- DAG metadata (tags, schedule) is correctly configured

## 📊 Monitoring

- **Airflow UI**: http://localhost:8080
- **Flower (Celery)**: http://localhost:5555
- **Logs**: `./logs/` directory

## 🛠️ Development

### Adding a new task

1. Create a Python function in `dags/ml_pipeline_dag.py`
2. Define a new operator in the DAG
3. Add task dependencies
4. Test locally before deploying

### Modifying the pipeline

```python
# Example: Add a new preprocessing step
preprocessing_task = PythonOperator(
    task_id='preprocessing_task',
    python_callable=preprocess_data,
)

# Update dependencies
etl_task >> preprocessing_task >> training_task
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use**
```bash
# Change ports in docker-compose.yaml or stop conflicting services
docker-compose down
```

**Permission denied on logs**
```bash
# Fix permissions
chmod -R 777 logs/
```

**DAG not appearing**
```bash
# Check DAG bag
docker-compose exec airflow-webserver airflow dags list
```

## 🙏 Acknowledgments

- Apache Airflow community
- Iris dataset from UCI Machine Learning Repository
- Docker & Docker Compose
