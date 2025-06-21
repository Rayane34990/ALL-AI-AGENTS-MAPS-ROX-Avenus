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
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Agent Discovery API",
    description="🤖 The ultimate open-source AI discovery platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database and test connection on startup."""
    try:
        logger.info("🚀 Starting AI Agent Discovery API...")
        logger.info(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
        
        # Test database connection
        db_url = os.environ.get('DATABASE_URL')
        if db_url:
            logger.info(f"Database URL configured: {db_url[:50]}...")
        else:
            logger.warning("No DATABASE_URL configured!")
        
        # Initialize database tables
        init_db()
        logger.info("✅ Database initialized successfully")
        
        # Test connection with a simple query
        from db.models import SessionLocal, Agent
        db = SessionLocal()
        try:
            agent_count = db.query(Agent).count()
            logger.info(f"✅ Database connection test passed. Total agents: {agent_count}")
        except Exception as e:
            logger.error(f"❌ Database connection test failed: {e}")
            raise e
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        # Don't crash the app, but log the error
        # raise e  # Uncomment to crash on startup errors

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
    "https://*.onrender.com",  # Render services
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

@app.get("/test-db")
async def test_database():
    """Test database connection endpoint for debugging."""
    try:
        from db.connection import test_database_connection
        result = test_database_connection()
        return result
    except ImportError:
        # Fallback test if connection utility is not available
        try:
            from db.models import SessionLocal, Agent
            db = SessionLocal()
            agent_count = db.query(Agent).count()
            db.close()
            return {
                "status": "success",
                "message": "Database connection successful (fallback test)",
                "total_agents": agent_count
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Database connection failed: {e}"
            }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port, reload=False)
