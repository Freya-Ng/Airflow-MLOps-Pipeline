# Quick Start Guide

Get up and running with Airflow ML Orchestration in 5 minutes!

## Prerequisites Check

```bash
# Check Docker
docker --version
# Should show: Docker version 20.x or higher

# Check Docker Compose
docker-compose --version
# Should show: Docker Compose version 2.x or higher
```

If not installed, visit:
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## Step-by-Step Setup

### 1️⃣ Clone & Navigate

```bash
git clone https://github.com/yourusername/airflow-ml-orchestration.git
cd airflow-ml-orchestration
```

### 2️⃣ Configure Environment

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
echo "AIRFLOW_UID=50000" >> .env
```

**Linux/Mac:**
```bash
cp .env.example .env
echo "AIRFLOW_UID=$(id -u)" >> .env
```

### 3️⃣ Initialize Directories

```bash
python scripts/init.py
```

This creates all necessary directories and checks dependencies.

### 4️⃣ Start Airflow

```bash
# Initialize the database (first time only)
docker-compose up airflow-init

# Start all services
docker-compose up -d

# Check if services are running
docker-compose ps
```

You should see all services in "Up" state.

### 5️⃣ Access Airflow Web UI

1. Open browser: http://localhost:8080
2. Login with:
   - **Username**: `airflow`
   - **Password**: `airflow`

### 6️⃣ Configure Pipeline

**Option A: Automatic Setup**
```bash
docker-compose exec airflow-webserver python /opt/airflow/dags/setup_ml_pipeline.py
```

**Option B: Manual Setup**
1. Go to Admin → Variables in Airflow UI
2. Add these variables:

| Key | Value |
|-----|-------|
| `ml_model_type` | `random_forest` |
| `accuracy_threshold` | `0.8` |
| `notification_email` | `your-email@example.com` |

### 7️⃣ Run Your First Pipeline

1. In Airflow UI, find `mlpipeline_complete` DAG
2. Toggle it **ON** (switch on the left)
3. Click the **▶ Play** button → "Trigger DAG"
4. Watch it run! 🎉

## Verify Everything Works

### Check Services

```bash
# View all services
docker-compose ps

# Should show:
# - airflow-webserver (port 8080)
# - airflow-scheduler
# - airflow-worker
# - postgres (port 5432)
# - redis (port 6379)
# - flower (port 5555)
```

### Check Logs

```bash
# View scheduler logs
docker-compose logs airflow-scheduler

# View worker logs
docker-compose logs airflow-worker

# Follow logs in real-time
docker-compose logs -f
```

### Check DAG

```bash
# List all DAGs
docker-compose exec airflow-webserver airflow dags list

# Should show: mlpipeline_complete
```

## Common First-Time Issues

### Issue: Port 8080 already in use
**Solution:**
```bash
# Check what's using port 8080
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Mac/Linux

# Either stop that service or change port in docker-compose.yaml
```

### Issue: Services won't start
**Solution:**
```bash
# Stop all services
docker-compose down

# Remove volumes and start fresh
docker-compose down -v
docker-compose up airflow-init
docker-compose up -d
```

### Issue: DAG not appearing
**Solution:**
```bash
# Check DAG for errors
docker-compose exec airflow-webserver airflow dags list-import-errors

# Restart scheduler
docker-compose restart airflow-scheduler
```

## What's Next?

### Explore the UI

- 📊 **DAGs**: View and manage your pipelines
- 📈 **Graph View**: Visualize task dependencies
- 📝 **Logs**: Debug task execution
- ⚙️ **Admin**: Configure variables and connections
- 🌸 **Flower**: Monitor Celery workers (http://localhost:5555)

### Customize Your Pipeline

1. Edit `dags/ml_pipeline_dag.py`
2. Add your own tasks
3. Configure variables for your data source
4. Deploy your models

### Learn More

- 📖 [Architecture Guide](docs/ARCHITECTURE.md)
- ⚙️ [Configuration Guide](docs/CONFIGURATION.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT.md)
- 🤝 [Contributing Guide](CONTRIBUTING.md)

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove all data (careful!)
docker-compose down -v
```

## Need Help?

- 📖 Check the [full README](README.md)
- 🐛 Report issues on GitHub
- 💬 Ask questions in Discussions
- 📧 Contact: your-email@example.com

## Success Checklist

- [ ] Docker and Docker Compose installed
- [ ] Repository cloned
- [ ] Environment configured
- [ ] Services started successfully
- [ ] Airflow UI accessible at http://localhost:8080
- [ ] Variables configured
- [ ] First DAG run completed successfully

**Congratulations! You're ready to build ML pipelines! 🎉**
