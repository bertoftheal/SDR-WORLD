#!/usr/bin/env python
"""
Simple test to check if environment variables are being loaded correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdr_assistant.config.settings import settings

def check_environment():
    """Check if environment variables are loaded correctly."""
    print("Checking environment variables...")
    
    # Check Supabase variables directly from settings
    print("\nFrom settings object:")
    print(f"SUPABASE_URL: {settings.SUPABASE_URL}")
    print(f"SUPABASE_KEY: {'✓ (set)' if settings.SUPABASE_KEY else '✗ (not set)'}")
    
    # Check if the is_supabase_configured method is correct
    print(f"\nIs Supabase configured according to settings: {settings.is_supabase_configured()}")
    
    # Manual check for Supabase variables
    print("\nManual check for env variables:")
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'sdr_assistant', 'venv (backend)', '.env')
    print(f"Looking for .env at: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    if os.path.exists(env_path):
        # Load directly and check
        load_dotenv(env_path, override=True)
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        print(f"\nDirect from env file:")
        print(f"SUPABASE_URL: {supabase_url}")
        print(f"SUPABASE_KEY: {'✓ (set)' if supabase_key else '✗ (not set)'}")

if __name__ == "__main__":
    check_environment()
