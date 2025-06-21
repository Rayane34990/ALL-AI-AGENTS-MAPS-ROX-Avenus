#!/usr/bin/env python3
"""
DNS resolution debugging tool for Render + Supabase.
Run this script to diagnose DNS and connection issues.
"""
import os
import socket
import sys
from urllib.parse import urlparse

def debug_dns_resolution():
    """Debug DNS resolution for database host."""
    
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not set")
        return
    
    print(f"🔍 Debugging DNS for: {db_url[:50]}...")
    
    try:
        parsed = urlparse(db_url)
        host = parsed.hostname
        port = parsed.port or 5432
        
        print(f"🌐 Host: {host}")
        print(f"🔌 Port: {port}")
        
        # Test IPv4 resolution
        try:
            ipv4_results = socket.getaddrinfo(host, port, socket.AF_INET)
            print(f"✅ IPv4 addresses:")
            for result in ipv4_results:
                print(f"   {result[4][0]}:{result[4][1]}")
        except Exception as e:
            print(f"❌ IPv4 resolution failed: {e}")
        
        # Test IPv6 resolution
        try:
            ipv6_results = socket.getaddrinfo(host, port, socket.AF_INET6)
            print(f"✅ IPv6 addresses:")
            for result in ipv6_results:
                print(f"   [{result[4][0]}]:{result[4][1]}")
        except Exception as e:
            print(f"❌ IPv6 resolution failed: {e}")
        
        # Test default resolution
        try:
            default_results = socket.getaddrinfo(host, port)
            print(f"✅ Default resolution (all families):")
            for result in default_results:
                family = "IPv4" if result[0] == socket.AF_INET else "IPv6"
                print(f"   {family}: {result[4][0]}:{result[4][1]}")
        except Exception as e:
            print(f"❌ Default resolution failed: {e}")
            
        # Test socket connection to IPv4
        try:
            ipv4_host = socket.getaddrinfo(host, port, socket.AF_INET)[0][4][0]
            print(f"🔌 Testing socket connection to IPv4 {ipv4_host}:{port}...")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((ipv4_host, port))
            sock.close()
            
            if result == 0:
                print("✅ IPv4 socket connection successful!")
            else:
                print(f"❌ IPv4 socket connection failed with code: {result}")
                
        except Exception as e:
            print(f"❌ IPv4 socket test failed: {e}")
            
    except Exception as e:
        print(f"❌ DNS debugging failed: {e}")

def check_environment():
    """Check environment variables and system info."""
    print("🔍 Environment Information:")
    print(f"   RENDER: {os.environ.get('RENDER', 'Not set')}")
    print(f"   PORT: {os.environ.get('PORT', 'Not set')}")
    print(f"   DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
    
    print(f"🐍 Python: {sys.version}")
    print(f"📦 Platform: {sys.platform}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 DNS Resolution Debugger")
    print("=" * 60)
    
    check_environment()
    print()
    debug_dns_resolution()
