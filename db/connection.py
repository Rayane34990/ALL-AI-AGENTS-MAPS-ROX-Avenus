"""
Database connection utilities for cloud deployment.
Handles IPv6 issues with Render + Supabase specifically.
"""
import os
import socket
import logging
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Apply IPv6 patch if on Render
try:
    from .ipv6_patch import apply_ipv4_patch
    if os.environ.get('RENDER'):
        apply_ipv4_patch()
except ImportError:
    pass

logger = logging.getLogger(__name__)

def create_cloud_engine(database_url=None):
    """
    Create a SQLAlchemy engine optimized for cloud deployment.
    Handles IPv6 issues with Render + Supabase.
    """
    db_url = database_url or os.environ.get('DATABASE_URL')
    
    if not db_url:
        raise ValueError("No DATABASE_URL provided")
    
    # For Supabase connections, try to resolve IPv6 issues
    if 'supabase.co' in db_url:
        return _create_supabase_engine(db_url)
    else:
        return _create_generic_engine(db_url)

def _create_supabase_engine(db_url):
    """Create engine specifically for Supabase with IPv4 fallback."""
    
    # Strategy 1: Try with IPv4 resolution
    try:
        logger.info("Attempting Supabase connection with IPv4 resolution...")
        
        parsed = urlparse(db_url)
        host = parsed.hostname
        
        # Get IPv4 address
        ipv4_addresses = socket.getaddrinfo(host, None, socket.AF_INET)
        if ipv4_addresses:
            ipv4_host = ipv4_addresses[0][4][0]
            db_url_ipv4 = db_url.replace(host, ipv4_host)
            
            engine = create_engine(
                db_url_ipv4,
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=5,
                max_overflow=10,
                connect_args={
                    "sslmode": "require",
                    "options": "-c timezone=utc"
                }
            )
            
            # Test the connection
            with engine.connect() as conn:
                conn.execute("SELECT 1")
                logger.info("✅ Supabase connection successful with IPv4!")
                return engine
                
    except Exception as e:
        logger.warning(f"IPv4 connection attempt failed: {e}")
    
    # Strategy 2: Try with original URL and different connection args
    try:
        logger.info("Attempting Supabase connection with original URL...")
        
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args={
                "sslmode": "require",
                "connect_timeout": 30
            }
        )
        
        # Test the connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            logger.info("✅ Supabase connection successful with original URL!")
            return engine
            
    except Exception as e:
        logger.error(f"Original URL connection failed: {e}")
        raise e

def _create_generic_engine(db_url):
    """Create engine for non-Supabase databases."""
    
    if db_url.startswith('sqlite'):
        return create_engine(
            db_url,
            connect_args={"check_same_thread": False}
        )
    else:
        return create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300
        )

def test_database_connection(engine=None):
    """Test database connection and return detailed info."""
    
    if not engine:
        engine = create_cloud_engine()
    
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1").fetchone()
            return {
                "status": "success",
                "message": "Database connection successful",
                "result": result[0] if result else None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {e}",
            "error": str(e)
        }
