#!/usr/bin/env python3
"""
Database connection utility with IPv4 fallback for Render deployment.
"""

import os
import socket
import psycopg2
from urllib.parse import urlparse

def force_ipv4_connection():
    """Force IPv4 connections for psycopg2 to avoid Render IPv6 issues."""
    # Patch socket.getaddrinfo to prefer IPv4
    original_getaddrinfo = socket.getaddrinfo
    
    def getaddrinfo_ipv4_first(*args, **kwargs):
        try:
            # Try IPv4 first
            kwargs['family'] = socket.AF_INET
            return original_getaddrinfo(*args, **kwargs)
        except Exception:
            # Fallback to original if IPv4 fails
            return original_getaddrinfo(*args, **kwargs)
    
    socket.getaddrinfo = getaddrinfo_ipv4_first

def get_connection_params(database_url):
    """Parse database URL and return connection parameters."""
    parsed = urlparse(database_url)
    return {
        'host': parsed.hostname,
        'port': parsed.port,
        'database': parsed.path[1:],  # Remove leading '/'
        'user': parsed.username,
        'password': parsed.password,
        'sslmode': 'require'
    }

def test_connection():
    """Test database connection."""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        return False, "DATABASE_URL not set"
    
    try:
        # Apply IPv4 patch
        force_ipv4_connection()
        
        # Get connection parameters
        params = get_connection_params(database_url)
        
        # Test connection
        conn = psycopg2.connect(**params)
        conn.close()
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    success, message = test_connection()
    print(f"Database connection: {message}")
    exit(0 if success else 1)
