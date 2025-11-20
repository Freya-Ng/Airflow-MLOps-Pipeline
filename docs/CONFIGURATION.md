# Configuration Guide

## Environment Variables

### Core Airflow Settings

```bash
AIRFLOW_UID=50000                    # User ID for Airflow containers
AIRFLOW_PROJ_DIR=.                   # Project directory path
```

### Database Configuration

```bash
POSTGRES_USER=airflow                # PostgreSQL username
POSTGRES_PASSWORD=airflow            # PostgreSQL password
POSTGRES_DB=airflow                  # PostgreSQL database name
```

### Redis Configuration

```bash
REDIS_PASSWORD=redispass             # Redis password
```

## Airflow Variables

Configure these in the Airflow UI (Admin → Variables) or via CLI:

### ML Model Configuration

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `ml_model_type` | ML algorithm to use | `random_forest` |
| `training_data_path` | Path to training data | `/opt/airflow/data/processed/training_data.csv` |
| `model_save_path` | Where to save trained models | `/opt/airflow/data/models/` |
| `test_size` | Train/test split ratio | `0.2` |
| `random_state` | Random seed | `42` |

### Pipeline Configuration

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `accuracy_threshold` | Minimum accuracy for deployment | `0.8` |
| `crawl_url` | Data source URL | `https://example.com/data` |
| `notification_email` | Email for alerts | `your-email@example.com` |

## Email Configuration (Optional)

For production email notifications, configure SMTP settings:

```bash
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT=587
AIRFLOW__SMTP__SMTP_USER=your-email@gmail.com
AIRFLOW__SMTP__SMTP_PASSWORD=your-app-password
AIRFLOW__SMTP__SMTP_MAIL_FROM=your-email@gmail.com
```

### Gmail Setup

1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in `SMTP_PASSWORD`

## Airflow Connections

### Database Connection

```python
conn_id='ml_database'
conn_type='postgres'
host='postgres'
login='ml_user'
password='ml_password'
port=5432
schema='ml_pipeline'
```

### API Connection

```python
conn_id='ml_api'
conn_type='http'
host='https://api.mlservice.com'
login='api_user'
password='api_password'
```

## Advanced Configuration

### Executor Configuration

Edit `config/airflow.cfg` to modify:

- Parallelism settings
- Task concurrency
- DAG concurrency
- Worker settings

### Resource Limits

Edit `docker-compose.yaml` to adjust:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

## Security Best Practices

1. **Never commit `.env` files** with real credentials
2. Use **strong passwords** for production
3. Enable **Airflow authentication** (LDAP/OAuth)
4. Use **secrets backend** (AWS Secrets Manager, Vault)
5. Rotate credentials regularly
6. Use **HTTPS** in production
7. Enable **audit logging**

## Troubleshooting Configuration

### Check Current Configuration

```bash
# View all Airflow configuration
docker-compose exec airflow-webserver airflow config list

# Check specific setting
docker-compose exec airflow-webserver airflow config get-value core executor
```

### Validate Variables

```bash
# List all variables
docker-compose exec airflow-webserver airflow variables list

# Get specific variable
docker-compose exec airflow-webserver airflow variables get ml_model_type
```

### Test Connections

```bash
# List all connections
docker-compose exec airflow-webserver airflow connections list

# Test connection
docker-compose exec airflow-webserver airflow connections get ml_database
```
