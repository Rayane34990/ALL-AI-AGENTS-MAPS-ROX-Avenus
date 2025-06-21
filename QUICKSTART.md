# Quick Start Guide

## Prerequisites

- **Python**: 3.9 or higher
- **PostgreSQL**: 13+ (local or cloud instance)
- **Node.js**: 16+ (for frontend development)
- **Git**: Latest version

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/riteshroshann/ALL-AI-AGENTS-MAPS-ROX-Avenus.git
cd ALL-AI-AGENTS-MAPS-ROX-Avenus
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your PostgreSQL credentials
# Example:
# DATABASE_URL=postgresql://username:password@localhost:5432/ai_knowledge
```

### 4. Database Initialization
```bash
# Initialize database schema
python init_db.py

# Verify connection
python -c "from db.models import get_session; print('✓ Database connected successfully')"
```

## Running the Application

### Development Mode

#### Backend API
```bash
# Start FastAPI development server
python main.py

# Alternative with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Optional)
```bash
# Install frontend dependencies
cd web
npm install

# Start React development server
npm start
```

### Production Mode
```bash
# Using Gunicorn (recommended for production)
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t ai-knowledge .
docker run -p 8000:8000 -e DATABASE_URL="your_db_url" ai-knowledge
```

## Data Ingestion

### Single Source Ingestion
```bash
# Hugging Face models
python -m ingest.hf_ingest

# arXiv papers
python -m ingest.arxiv_ingest

# GitHub repositories
python -m ingest.github_ingest

# TensorFlow Hub models
python -m ingest.tfhub_ingest

# ONNX models
python -m ingest.onnx_ingest
```

### Batch Ingestion
```bash
# Run all ingestion scripts
python scripts/run_all_ingestion.py

# With progress monitoring
python scripts/run_all_ingestion.py --verbose --batch-size 1000
```

### Automated Ingestion
```bash
# Setup scheduled ingestion (using cron)
# Add to crontab: 0 */6 * * * /path/to/venv/bin/python /path/to/project/scripts/run_all_ingestion.py

# Or use the built-in scheduler
python scripts/scheduled_ingestion.py --interval 6h
```

## Data Processing

### Deduplication
```bash
# Run deduplication algorithm
python -m dedup.dedup

# With custom similarity threshold
python -m dedup.dedup --threshold 0.85

# Advanced deduplication with clustering
python -m dedup.dedup --method clustering --min-cluster-size 2
```

### Data Validation
```bash
# Validate data integrity
python scripts/validate_data.py

# Generate data quality report
python scripts/data_quality_report.py --output reports/quality_$(date +%Y%m%d).html
```

## API Usage

### Basic Queries
```bash
# Search for AI models
curl "http://localhost:8000/api/v1/search?q=transformer&limit=10"

# Get model details
curl "http://localhost:8000/api/v1/models/123"

# Browse by category
curl "http://localhost:8000/api/v1/categories/nlp"
```

### Advanced Queries
```bash
# Search with filters
curl "http://localhost:8000/api/v1/search?q=vision&platform=huggingface&min_stars=100"

# Aggregated statistics
curl "http://localhost:8000/api/v1/analytics/trends?timeframe=30d"

# Export data
curl "http://localhost:8000/api/v1/export?format=csv&category=computer-vision" -o models.csv
```

### Authentication (Production)
```bash
# Get API token
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token for authenticated requests
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/v1/search?q=gpt"
```

## Monitoring and Maintenance

### Health Checks
```bash
# API health check
curl "http://localhost:8000/health"

# Database health check
curl "http://localhost:8000/health/db"

# Detailed system status
curl "http://localhost:8000/status"
```

### Performance Monitoring
```bash
# View application metrics
curl "http://localhost:8000/metrics"

# Database performance
python scripts/db_performance_check.py

# Generate performance report
python scripts/performance_report.py --output reports/perf_$(date +%Y%m%d).json
```

### Backup and Recovery
```bash
# Create database backup
pg_dump $DATABASE_URL > backups/backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql $DATABASE_URL < backups/backup_20250621_120000.sql

# Automated backup script
python scripts/automated_backup.py --destination s3://your-backup-bucket/
```

## Development Workflow

### Code Quality
```bash
# Run linting
flake8 src/ tests/
black src/ tests/
mypy src/

# Run tests
pytest tests/ -v --cov=src/

# Security scan
bandit -r src/
```

### Database Migrations
```bash
# Create new migration
python scripts/create_migration.py "add_new_field_to_agents"

# Apply migrations
python scripts/migrate.py

# Rollback migration
python scripts/migrate.py --rollback
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Test database connectivity
python -c "
import psycopg2
from urllib.parse import urlparse
try:
    conn = psycopg2.connect('$DATABASE_URL')
    print('✓ Database connection successful')
    conn.close()
except Exception as e:
    print(f'✗ Database connection failed: {e}')
"
```

#### Memory Issues
```bash
# Monitor memory usage during ingestion
python -m memory_profiler scripts/run_all_ingestion.py

# Optimize for large datasets
python -m ingest.hf_ingest --batch-size 500 --memory-limit 2GB
```

#### Performance Issues
```bash
# Analyze slow queries
python scripts/analyze_slow_queries.py

# Rebuild database indexes
python scripts/rebuild_indexes.py

# Update statistics
python scripts/update_db_stats.py
```

### Getting Help

- **Documentation**: Check `/docs` folder for detailed guides
- **API Documentation**: Visit `http://localhost:8000/docs` when running
- **Issues**: Create GitHub issue with error logs and system info
- **Community**: Join discussions in GitHub Discussions

### Configuration Examples

#### High-Performance Setup
```bash
# .env for high-performance deployment
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_knowledge?pool_size=20&max_overflow=30
REDIS_URL=redis://localhost:6379/0
WORKERS=8
BATCH_SIZE=2000
CACHE_TTL=3600
```

#### Development Setup
```bash
# .env for development
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_knowledge_dev
DEBUG=True
LOG_LEVEL=DEBUG
RELOAD=True
```

---

**Next Steps**: After completing the quickstart, see [DEPLOY.md](DEPLOY.md) for production deployment or [CONTRIBUTING.md](CONTRIBUTING.md) to contribute to the project.
