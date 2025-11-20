# Deployment Guide

## Production Deployment Checklist

### Pre-Deployment

- [ ] Review and update all configurations
- [ ] Set strong passwords for all services
- [ ] Configure production database
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerting
- [ ] Review security settings
- [ ] Test all DAGs in staging environment

### Deployment Steps

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/yourusername/airflow-ml-orchestration.git
cd airflow-ml-orchestration

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Create directories
mkdir -p ./logs ./plugins ./config ./data/{raw,processed,model}
```

#### 3. Security Configuration

```bash
# Generate secure passwords
openssl rand -base64 32  # For database
openssl rand -base64 32  # For Redis
openssl rand -base64 32  # For Airflow secret key

# Update .env with generated passwords
```

#### 4. Start Services

```bash
# Initialize database
docker-compose up airflow-init

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

#### 5. Post-Deployment

```bash
# Create admin user
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Set up Airflow Variables
docker-compose exec airflow-webserver python /opt/airflow/dags/setup_ml_pipeline.py

# Test DAG
docker-compose exec airflow-webserver airflow dags test mlpipeline_complete
```

## Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

## Monitoring Setup

### Prometheus (Optional)

```yaml
# Add to docker-compose.yaml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### Grafana (Optional)

```yaml
grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Backup Strategy

### Database Backup

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T postgres pg_dump -U airflow airflow > backup_$DATE.sql
gzip backup_$DATE.sql
# Upload to S3 or other storage
EOF

chmod +x backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### Data Backup

```bash
# Backup data directory
tar -czf data_backup_$(date +%Y%m%d).tar.gz ./data
```

## Scaling

### Horizontal Scaling (Add Workers)

```yaml
# In docker-compose.yaml, add more workers
airflow-worker-2:
  <<: *airflow-common
  command: celery worker
  environment:
    <<: *airflow-common-env
    WORKER_NAME: worker-2
```

### Vertical Scaling (Resource Limits)

```yaml
services:
  airflow-worker:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

## Troubleshooting

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs airflow-webserver

# Follow logs
docker-compose logs -f airflow-scheduler
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart airflow-scheduler
```

### Clean Up

```bash
# Stop all services
docker-compose down

# Remove volumes (careful!)
docker-compose down -v
```

## Health Checks

```bash
# Check Airflow health
curl http://localhost:8080/health

# Check database connection
docker-compose exec postgres pg_isready

# Check Redis
docker-compose exec redis redis-cli ping
```

## Maintenance

### Regular Tasks

- Review logs daily
- Monitor disk usage
- Check DAG run history
- Update dependencies monthly
- Review security settings quarterly
- Test backups regularly

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose build

# Restart services
docker-compose up -d
```
