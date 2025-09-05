# Deployment Guide

## Overview

This guide covers deployment options for the Hotel AI Suite, from local development to production environments.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git
- 4GB+ RAM available
- 10GB+ disk space

## Local Development

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd Client_Churn_analyzer

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f hotel-ai-app
```

### Access Points
- **Application**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434
- **Redis**: localhost:6379
- **PostgreSQL**: localhost:5432

## Production Deployment

### Environment Variables

Create `.env` file:
```bash
# Application
APP_TITLE=Hotel AI Suite
APP_VERSION=1.0.0
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/hotel_ai
REDIS_URL=redis://redis:6379

# AI Services
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3
VECTOR_DB_PATH=/app/data/rag_db

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# External Services
OPENAI_API_KEY=your-openai-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

### Docker Compose Production

```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale hotel-ai-app=3
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hotel-ai-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hotel-ai-app
  template:
    metadata:
      labels:
        app: hotel-ai-app
    spec:
      containers:
      - name: hotel-ai-app
        image: ghcr.io/your-org/hotel-ai-suite:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: hotel-ai-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### AWS Deployment

#### ECS with Fargate
```bash
# Build and push image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker build -t hotel-ai-suite .
docker tag hotel-ai-suite:latest <account>.dkr.ecr.us-east-1.amazonaws.com/hotel-ai-suite:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/hotel-ai-suite:latest

# Deploy with ECS
aws ecs create-service \
  --cluster hotel-ai-cluster \
  --service-name hotel-ai-service \
  --task-definition hotel-ai-task:1 \
  --desired-count 3
```

#### Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB
eb init hotel-ai-suite

# Create environment
eb create production

# Deploy
eb deploy
```

### Google Cloud Platform

#### Cloud Run
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/hotel-ai-suite

# Deploy
gcloud run deploy hotel-ai-suite \
  --image gcr.io/PROJECT-ID/hotel-ai-suite \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment

#### Container Instances
```bash
# Build and push
az acr build --registry myregistry --image hotel-ai-suite .

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name hotel-ai-suite \
  --image myregistry.azurecr.io/hotel-ai-suite:latest \
  --ports 8000 \
  --environment-variables \
    DATABASE_URL=your-database-url \
    REDIS_URL=your-redis-url
```

## Monitoring and Observability

### Health Checks
```bash
# Application health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# AI service health
curl http://localhost:8000/health/ai
```

### Metrics Collection

#### Prometheus + Grafana
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'hotel-ai-app'
    static_configs:
      - targets: ['hotel-ai-app:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

#### Application Metrics
- Request count and duration
- AI processing time
- Database query performance
- Memory and CPU usage
- Error rates

### Logging

#### Structured Logging
```python
import structlog

logger = structlog.get_logger()

# Usage
logger.info("User request processed", 
           user_id=user_id, 
           processing_time=1.2,
           endpoint="/api/churn/predict")
```

#### Log Aggregation
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Fluentd**: Log collection and forwarding
- **CloudWatch**: AWS native logging

## Security Considerations

### SSL/TLS
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://hotel-ai-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Network Security
- Firewall configuration
- VPC setup for cloud deployments
- Security groups and network ACLs
- DDoS protection

### Data Protection
- Database encryption at rest
- API key management
- Secrets management (AWS Secrets Manager, Azure Key Vault)
- GDPR compliance measures

## Performance Optimization

### Caching Strategy
```python
# Redis caching
from redis import Redis
import json

redis_client = Redis(host='redis', port=6379, db=0)

def cache_churn_prediction(customer_id, prediction):
    key = f"churn:{customer_id}"
    redis_client.setex(key, 3600, json.dumps(prediction))

def get_cached_prediction(customer_id):
    key = f"churn:{customer_id}"
    cached = redis_client.get(key)
    return json.loads(cached) if cached else None
```

### Database Optimization
- Connection pooling
- Query optimization
- Indexing strategy
- Read replicas for analytics

### AI Model Optimization
- Model quantization
- Batch processing
- GPU acceleration
- Model caching

## Backup and Recovery

### Database Backups
```bash
# PostgreSQL backup
pg_dump -h postgres -U hotel_user hotel_ai > backup_$(date +%Y%m%d).sql

# Restore
psql -h postgres -U hotel_user hotel_ai < backup_20240115.sql
```

### Application Data
- Vector database backups
- Model artifacts
- Configuration files
- Log archives

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check logs
docker-compose logs hotel-ai-app

# Check resource usage
docker stats

# Restart services
docker-compose restart
```

#### Database Connection Issues
```bash
# Test connection
docker-compose exec hotel-ai-app python -c "
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@postgres:5432/hotel_ai')
print('Connection successful')
"
```

#### AI Service Issues
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama
docker-compose restart ollama
```

### Performance Issues
- Monitor resource usage
- Check database query performance
- Analyze AI processing times
- Review network latency

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Session management
- Database scaling
- Cache distribution

### Vertical Scaling
- Resource allocation
- Memory optimization
- CPU optimization
- Storage optimization

## Maintenance

### Regular Tasks
- Security updates
- Dependency updates
- Performance monitoring
- Backup verification
- Log rotation

### Update Procedures
```bash
# Rolling update
docker-compose pull
docker-compose up -d --no-deps hotel-ai-app

# Blue-green deployment
# 1. Deploy new version to staging
# 2. Test thoroughly
# 3. Switch traffic to new version
# 4. Monitor and rollback if needed
```
