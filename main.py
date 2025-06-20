#!/usr/bin/env python3
"""
Main FastAPI application entry point.
Starts the AI Agent Discovery API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from db.models import init_db
import os

# Initialize database tables on startup
init_db()

app = FastAPI(
    title="AI Agent Discovery API",
    description="The ultimate open-source AI discovery platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://riteshroshann.github.io"],
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
        "message": "AI Agent Discovery API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Detailed health check."""
    try:
        from db.models import SessionLocal, Agent
        db = SessionLocal()
        agent_count = db.query(Agent).count()
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_agents": agent_count,
            "database_url": os.environ.get('DATABASE_URL', 'not set').split('@')[0] + "@***"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
