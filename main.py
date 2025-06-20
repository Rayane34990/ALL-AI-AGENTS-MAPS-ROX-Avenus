#!/usr/bin/env python3
"""
Main FastAPI application entry point.
Cloud-native AI Agent Discovery API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from db.models import init_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database tables on startup
init_db()

app = FastAPI(
    title="AI Agent Discovery API",
    description="🤖 The ultimate open-source AI discovery platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for cloud deployment
allowed_origins = [
    "http://localhost:3000",  # Development
    "https://your-app.vercel.app",  # Production frontend
    "https://*.vercel.app",  # Vercel previews
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "🤖 AI Agent Discovery API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "environment": os.environ.get("ENVIRONMENT", "development")
    }

@app.get("/health")
async def health_check():
    """Detailed health check for cloud monitoring."""
    try:
        from db.models import SessionLocal, Agent
        db = SessionLocal()
        agent_count = db.query(Agent).count()
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_agents": agent_count,
            "environment": os.environ.get("ENVIRONMENT", "development"),
            "database_url": "configured" if os.environ.get('DATABASE_URL') else "missing"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "environment": os.environ.get("ENVIRONMENT", "development")
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=False)
