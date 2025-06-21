# Production Deployment Guide

## Overview

This guide covers enterprise-grade deployment of the AI Knowledge Graph Engine across multiple cloud platforms with production reliability, monitoring, and scalability.

## Architecture Options

### Option 1: Microservices Architecture (Recommended)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Ingestion │    │     API     │    │  Frontend   │
│   Services  │    │   Gateway   │    │    (SPA)    │
│             │    │             │    │             │
│ • Kubernetes│    │ • FastAPI   │    │ • React     │
│ • Celery    │    │ • Load Bal. │    │ • CDN       │
│ • Redis     │    │ • Auth      │    │ • Caching   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                  ┌─────────────┐
                  │ PostgreSQL  │
                  │   Cluster   │
                  │             │
                  │ • Primary   │
                  │ • Replicas  │
                  │ • Backups   │
                  └─────────────┘
```

### Option 2: Serverless Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Functions  │    │   API GW    │    │  Static Web │
│             │    │             │    │             │
│ • AWS Lambda│    │ • Kong/NGINX│    │ • Vercel    │
│ • Cloud Run │    │ • Cloudflare│    │ • Netlify   │
│ • Scheduled │    │ • Rate Limit│    │ • S3+CloudF │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Cloud Platform Configurations

### AWS Production Setup

#### Prerequisites
- AWS CLI configured
- Docker installed
- Terraform 1.5+

#### Infrastructure as Code
```hcl
# terraform/main.tf
provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "ai-knowledge-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = true
}

module "rds" {
  source = "terraform-aws-modules/rds/aws"
  
  identifier = "ai-knowledge-db"
  engine     = "postgres"
  engine_version = "14.9"
  instance_class = "db.t3.large"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true
  
  db_name  = "ai_knowledge"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [module.security_group.security_group_id]
  subnet_ids            = module.vpc.database_subnets
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"
  
  monitoring_interval = 60
  performance_insights_enabled = true
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "ai-knowledge-cluster"
  cluster_version = "1.27"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  node_groups = {
    main = {
      desired_capacity = 2
      max_capacity     = 10
      min_capacity     = 1
      
      instance_types = ["t3.large"]
      
      k8s_labels = {
        Environment = "production"
        Application = "ai-knowledge"
      }
    }
  }
}
```

#### Kubernetes Deployment
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ai-knowledge
  labels:
    name: ai-knowledge

---
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ai-knowledge-config
  namespace: ai-knowledge
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  API_VERSION: "v1"

---
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ai-knowledge-secrets
  namespace: ai-knowledge
type: Opaque
data:
  DATABASE_URL: <base64-encoded-connection-string>
  JWT_SECRET: <base64-encoded-jwt-secret>

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-knowledge-api
  namespace: ai-knowledge
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-knowledge-api
  template:
    metadata:
      labels:
        app: ai-knowledge-api
    spec:
      containers:
      - name: api
        image: ai-knowledge:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-knowledge-secrets
              key: DATABASE_URL
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ai-knowledge-api-service
  namespace: ai-knowledge
spec:
  selector:
    app: ai-knowledge-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ai-knowledge-ingress
  namespace: ai-knowledge
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - api.ai-knowledge.dev
    secretName: ai-knowledge-tls
  rules:
  - host: api.ai-knowledge.dev
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ai-knowledge-api-service
            port:
              number: 80
```

### Google Cloud Platform (GCP)

#### Cloud Run Deployment
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ai-knowledge:$BUILD_ID', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/ai-knowledge:$BUILD_ID']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'ai-knowledge-api'
      - '--image=gcr.io/$PROJECT_ID/ai-knowledge:$BUILD_ID'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=2Gi'
      - '--cpu=2'
      - '--max-instances=100'
      - '--concurrency=1000'
```

#### Cloud SQL Setup
```bash
# Create Cloud SQL instance
gcloud sql instances create ai-knowledge-db \
  --database-version=POSTGRES_14 \
  --tier=db-standard-2 \
  --region=us-central1 \
  --storage-size=100GB \
  --storage-type=SSD \
  --backup-start-time=03:00 \
  --enable-bin-log \
  --deletion-protection

# Create database
gcloud sql databases create ai_knowledge --instance=ai-knowledge-db

# Create user
gcloud sql users create app_user --instance=ai-knowledge-db --password=<secure-password>
```

### Azure Container Apps

#### Infrastructure Template
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "containerAppName": {
      "type": "string",
      "defaultValue": "ai-knowledge-api"
    },
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.App/containerApps",
      "apiVersion": "2022-03-01",
      "name": "[parameters('containerAppName')]",
      "location": "[parameters('location')]",
      "properties": {
        "configuration": {
          "ingress": {
            "external": true,
            "targetPort": 8000
          },
          "secrets": [
            {
              "name": "database-url",
              "value": "[parameters('databaseUrl')]"
            }
          ]
        },
        "template": {
          "containers": [
            {
              "name": "ai-knowledge",
              "image": "ai-knowledge:latest",
              "resources": {
                "cpu": 1.0,
                "memory": "2Gi"
              },
              "env": [
                {
                  "name": "DATABASE_URL",
                  "secretRef": "database-url"
                }
              ]
            }
          ],
          "scale": {
            "minReplicas": 1,
            "maxReplicas": 10
          }
        }
      }
    }
  ]
}
```

## Monitoring and Observability

### Prometheus + Grafana Stack
```yaml
# monitoring/prometheus.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ai-knowledge-metrics
spec:
  selector:
    matchLabels:
      app: ai-knowledge-api
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Application Metrics
```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Metrics
REQUEST_COUNT = Counter('ai_knowledge_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('ai_knowledge_request_duration_seconds', 'Request latency')
ACTIVE_CONNECTIONS = Gauge('ai_knowledge_active_connections', 'Active DB connections')
INGESTION_RATE = Counter('ai_knowledge_artifacts_ingested_total', 'Artifacts ingested')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    REQUEST_LATENCY.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Logging Configuration
```python
# logging_config.py
import logging
import structlog
from pythonjsonlogger import jsonlogger

def configure_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter())
    
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
```

## Security Configuration

### Authentication & Authorization
```python
# security/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### Network Security
```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ai-knowledge-network-policy
  namespace: ai-knowledge
spec:
  podSelector:
    matchLabels:
      app: ai-knowledge-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 80
```

## Performance Optimization

### Database Configuration
```sql
-- postgresql.conf optimizations
shared_buffers = '256MB'
effective_cache_size = '1GB'
maintenance_work_mem = '64MB'
checkpoint_completion_target = 0.9
wal_buffers = '16MB'
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = '4MB'
min_wal_size = '1GB'
max_wal_size = '4GB'

-- Indexes for performance
CREATE INDEX CONCURRENTLY idx_agents_name_trgm ON agents USING gin(name gin_trgm_ops);
CREATE INDEX CONCURRENTLY idx_agents_description_trgm ON agents USING gin(description gin_trgm_ops);
CREATE INDEX CONCURRENTLY idx_agents_created_at ON agents(created_at);
CREATE INDEX CONCURRENTLY idx_agents_source_platform ON agents(source, platform);
```

### Application-Level Caching
```python
# caching/redis_config.py
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

async def init_cache():
    redis_client = redis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="ai-knowledge-cache")

@app.get("/api/v1/search")
@cache(expire=300)  # 5-minute cache
async def search_agents(q: str, limit: int = 20):
    # Search implementation
    pass
```

## Disaster Recovery

### Database Backup Strategy
```bash
#!/bin/bash
# backup/backup.sh

# Full backup (daily)
pg_dump $DATABASE_URL > "backups/full_$(date +%Y%m%d_%H%M%S).sql"

# Upload to S3
aws s3 cp "backups/full_$(date +%Y%m%d_%H%M%S).sql" s3://ai-knowledge-backups/

# Point-in-time recovery setup
pg_basebackup -D /backup/base -Ft -z -P -U postgres -h $DB_HOST
```

### Automated Failover
```yaml
# k8s/postgres-ha.yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: postgres-cluster
spec:
  instances: 3
  
  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "256MB"
      effective_cache_size: "1GB"
      
  bootstrap:
    initdb:
      database: ai_knowledge
      owner: app_user
      
  storage:
    size: 100Gi
    storageClass: fast-ssd
    
  monitoring:
    enabled: true
```

## Cost Optimization

### Resource Right-Sizing
```python
# monitoring/cost_optimization.py
import psutil
import asyncio
from prometheus_client import Gauge

CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage percentage')

async def monitor_resources():
    while True:
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.virtual_memory().percent)
        await asyncio.sleep(60)
```

### Auto-scaling Configuration
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-knowledge-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-knowledge-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Deployment Checklist

### Pre-Production
- [ ] Load testing completed (target: 1000 RPS)
- [ ] Security audit passed
- [ ] Backup/restore procedures tested
- [ ] Monitoring dashboards configured
- [ ] Documentation updated
- [ ] Team training completed

### Production Launch
- [ ] DNS configured with health checks
- [ ] SSL certificates installed and auto-renewal setup
- [ ] CDN configured for static assets
- [ ] Rate limiting configured
- [ ] Error tracking enabled (Sentry/DataDog)
- [ ] Log aggregation configured
- [ ] Alert rules configured
- [ ] On-call rotation established

### Post-Launch
- [ ] Performance monitoring for 48 hours
- [ ] User feedback collection
- [ ] Cost monitoring enabled
- [ ] Capacity planning updated
- [ ] Incident response procedures tested

## Support and Maintenance

### Regular Maintenance Tasks
```bash
# maintenance/weekly.sh
#!/bin/bash

# Database maintenance
psql $DATABASE_URL -c "VACUUM ANALYZE;"
psql $DATABASE_URL -c "REINDEX DATABASE ai_knowledge;"

# Log rotation
find /var/log/ai-knowledge -name "*.log" -mtime +7 -delete

# Security updates
apt update && apt upgrade -y

# Certificate renewal check
certbot renew --dry-run
```

### Performance Tuning
- Monitor query performance with `pg_stat_statements`
- Analyze slow queries weekly
- Update database statistics monthly
- Review and optimize indexes quarterly

### Security Updates
- Automated dependency updates via Dependabot
- Monthly security scanning with Trivy
- Quarterly penetration testing
- Annual security audit

---

For questions about production deployment, contact: devops@ai-knowledge.dev

## 🔧 Monitoring
- Backend health: `https://your-app.onrender.com/health`
- Frontend: `https://your-app.vercel.app`
- GitHub Actions: Check the Actions tab

Your AI discovery platform is now **LIVE** and **SUSTAINABLE**! 🎉
