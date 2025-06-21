#!/usr/bin/env python3
"""
Simple script to test database connection for Render deployment
"""
import os
import sys
import socket
from urllib.parse import urlparse

def test_connection():
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL environment variable not set")
        return False
    
    print(f"🔍 Testing connection to: {db_url[:50]}...")
    
    try:
        # Parse the database URL
        parsed = urlparse(db_url)
        host = parsed.hostname
        port = parsed.port or 5432
        
        print(f"🌐 Host: {host}")
        print(f"🔌 Port: {port}")
        
        # Test DNS resolution
        try:
            ipv4_addresses = socket.getaddrinfo(host, None, socket.AF_INET)
            ipv6_addresses = socket.getaddrinfo(host, None, socket.AF_INET6)
            
            print(f"📍 IPv4 addresses: {[addr[4][0] for addr in ipv4_addresses]}")
            print(f"📍 IPv6 addresses: {[addr[4][0] for addr in ipv6_addresses]}")
            
        except Exception as e:
            print(f"⚠️  DNS resolution error: {e}")
        
        # Test database connection
        from sqlalchemy import create_engine, text
        
        # Try with IPv4 resolution first
        try:
            ipv4_host = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
            db_url_ipv4 = db_url.replace(host, ipv4_host)
            
            engine = create_engine(
                db_url_ipv4,
                pool_pre_ping=True,
                connect_args={"sslmode": "require"}
            )
            
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).fetchone()
                print("✅ Database connection successful with IPv4!")
                return True
                
        except Exception as ipv4_error:
            print(f"❌ IPv4 connection failed: {ipv4_error}")
            
            # Fallback to original URL
            try:
                engine = create_engine(
                    db_url,
                    pool_pre_ping=True,
                    connect_args={"sslmode": "require"}
                )
                
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT 1")).fetchone()
                    print("✅ Database connection successful with original URL!")
                    return True
                    
            except Exception as original_error:
                print(f"❌ Original URL connection failed: {original_error}")
                return False
                
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
