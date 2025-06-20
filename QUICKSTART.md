# Quick Start Guide

## 1. Setup Environment
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

## 2. Install Dependencies
```bash
pip install -r requirements.txt
cd web && npm install
```

## 3. Initialize Database
```bash
# Set your DATABASE_URL first
export DATABASE_URL="postgresql://user:password@localhost:5432/ai_agents"
python init_db.py
```

## 4. Run the Application
```bash
# Start API server
python main.py
# or
uvicorn main:app --reload

# Start frontend (in new terminal)
cd web && npm start
```

## 5. Access the Application
- API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## 6. Ingest Data
```bash
# Run ingestion scripts
python -m ingest.github_ingest
python -m ingest.arxiv_ingest
python -m ingest.hf_ingest
```

## 7. Deduplicate (Optional)
```bash
python -m dedup.dedup
```
