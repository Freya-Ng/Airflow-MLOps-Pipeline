# Architecture Overview

## System Architecture

The Airflow ML Orchestration system follows a microservices architecture with the following components:

### Components

1. **Airflow Webserver**: Web UI for monitoring and managing workflows
2. **Airflow Scheduler**: Schedules and triggers DAG runs
3. **Airflow Worker(s)**: Executes tasks using CeleryExecutor
4. **PostgreSQL**: Metadata database for Airflow
5. **Redis**: Message broker for Celery
6. **Flower**: Monitoring UI for Celery workers

### Data Flow

```
External Source → Crawl → Raw Data → ETL → Processed Data → Model Training → Validation
                                                                                  ↓
                                                                            (Branch Logic)
                                                                                  ↓
                                                                  ┌───────────────┴───────────┐
                                                                  ↓                           ↓
                                                             Deploy Model              Retrain Alert
                                                                  ↓                           ↓
                                                              Monitor                        End
                                                                  ↓
                                                            Success Email
                                                                  ↓
                                                                 End
```

## ML Pipeline Stages

### 1. Data Crawling
- Fetches data from external sources
- Configurable via Airflow Variables
- Stores raw data in `data/raw/`

### 2. ETL Processing
- Cleans and transforms data
- Handles missing values
- Feature engineering
- Outputs to `data/processed/`

### 3. Model Training
- Loads processed data
- Trains ML model (configurable algorithm)
- Saves model artifacts
- Records training metrics

### 4. Validation
- Evaluates model performance
- Compares against threshold
- **Branch Decision**:
  - If accuracy >= threshold → Deploy
  - If accuracy < threshold → Alert

### 5. Deployment
- Deploys model to production endpoint
- Updates model registry
- Triggers monitoring

### 6. Monitoring
- Tracks model performance
- System health checks
- Logs metrics

### 7. Notification
- Sends success/failure emails
- Updates dashboards
- Alerts stakeholders

## Technology Stack

- **Orchestration**: Apache Airflow 3.1.3
- **Executor**: CeleryExecutor
- **Message Broker**: Redis
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Language**: Python 3.8+
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy

## Scalability Considerations

- Horizontal scaling via additional Celery workers
- Task parallelism through Airflow pools
- Resource isolation with Docker
- Separate queues for different task types
