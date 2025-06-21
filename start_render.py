#!/usr/bin/env python3
"""
Render deployment startup script.
Handles IPv6 issues and provides better error reporting for Render deployments.
"""
import os
import sys
import logging
import time

# Apply IPv6 patch early for Render
try:
    from db.ipv6_patch import apply_ipv4_patch
    apply_ipv4_patch()
except ImportError:
    pass

# Configure logging for Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_environment():
    """Test environment setup before starting the app."""
    logger.info("🔍 Testing environment setup...")
    
    # Check required environment variables
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        logger.error("❌ DATABASE_URL environment variable not set!")
        return False
    
    logger.info(f"✅ DATABASE_URL configured: {db_url[:50]}...")
    
    # Check Python version
    python_version = sys.version
    logger.info(f"🐍 Python version: {python_version}")
    
    return True

def test_database():
    """Test database connection."""
    logger.info("🗄️  Testing database connection...")
    
    try:
        # Test with the connection utility first
        try:
            from db.connection import test_database_connection
            result = test_database_connection()
            
            if result["status"] == "success":
                logger.info("✅ Database connection test passed!")
                return True
            else:
                logger.error(f"❌ Database connection test failed: {result['message']}")
                return False
                
        except ImportError:
            logger.info("Connection utility not available, using fallback test...")
            
            # Fallback test
            from db.models import SessionLocal, Agent, init_db
            
            # Initialize database
            init_db()
            logger.info("✅ Database initialized")
            
            # Test connection
            db = SessionLocal()
            try:
                agent_count = db.query(Agent).count()
                logger.info(f"✅ Database connection successful! Total agents: {agent_count}")
                return True
            finally:
                db.close()
                
    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        return False

def start_app():
    """Start the FastAPI application."""
    logger.info("🚀 Starting AI Agent Discovery API...")
    
    import uvicorn
    from main import app
    
    # Get configuration from environment
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"🌐 Starting server on {host}:{port}")
    
    # Start the application
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        access_log=True,
        log_level="info"
    )

def main():
    """Main startup function."""
    logger.info("=" * 60)
    logger.info("🤖 AI Agent Discovery API - Render Deployment")
    logger.info("=" * 60)
    
    # Test environment
    if not test_environment():
        logger.error("❌ Environment test failed!")
        sys.exit(1)
    
    # Test database connection
    if not test_database():
        logger.error("❌ Database test failed!")
        # Don't exit on database failure in case it's a temporary issue
        logger.warning("⚠️  Continuing startup despite database test failure...")
        time.sleep(5)  # Wait a bit before starting
    
    # Start the application
    try:
        start_app()
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
