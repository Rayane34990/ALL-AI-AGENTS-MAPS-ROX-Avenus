"""
IPv6 connection patch for Render + Supabase.
This module provides utilities to force IPv4 connections for PostgreSQL.
"""
import socket
import logging

logger = logging.getLogger(__name__)

# Store original socket.getaddrinfo
_original_getaddrinfo = socket.getaddrinfo

def ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """
    Custom getaddrinfo that prefers IPv4 for Supabase hosts.
    This helps fix IPv6 connection issues on Render.
    """
    if isinstance(host, str) and 'supabase.co' in host:
        # Force IPv4 for Supabase hosts
        try:
            logger.debug(f"Forcing IPv4 resolution for Supabase host: {host}")
            results = _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
            if results:
                logger.debug(f"IPv4 resolution successful for {host}: {results[0][4][0]}")
                return results
        except Exception as e:
            logger.warning(f"IPv4 resolution failed for {host}: {e}")
            # Fall back to original function
    
    # Use original function for non-Supabase hosts or if IPv4 fails
    return _original_getaddrinfo(host, port, family, type, proto, flags)

def apply_ipv4_patch():
    """Apply the IPv4-only patch to socket.getaddrinfo."""
    if socket.getaddrinfo is not ipv4_only_getaddrinfo:
        logger.info("Applying IPv4-only patch for Supabase connections...")
        socket.getaddrinfo = ipv4_only_getaddrinfo
    else:
        logger.debug("IPv4 patch already applied")

def remove_ipv4_patch():
    """Remove the IPv4-only patch."""
    if socket.getaddrinfo is ipv4_only_getaddrinfo:
        logger.info("Removing IPv4-only patch...")
        socket.getaddrinfo = _original_getaddrinfo
    else:
        logger.debug("IPv4 patch not currently applied")

# Auto-apply patch when module is imported if running on Render
import os
if os.environ.get('RENDER'):
    logger.info("Render environment detected, auto-applying IPv4 patch...")
    apply_ipv4_patch()
