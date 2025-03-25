#!/usr/bin/env python
"""
Test script to verify Supabase connection is working properly.
"""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path to import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdr_assistant.config.settings import settings
from sdr_assistant.services.supabase_service import SupabaseService

def test_connection():
    """Test the connection to Supabase."""
    print("Testing Supabase connection...")
    
    # Check if Supabase is configured in settings
    if not settings.is_supabase_configured():
        print("Error: Supabase is not configured. Please check your environment variables.")
        return False
    
    print(f"Supabase URL configured: {settings.SUPABASE_URL}")
    print(f"Supabase Key configured: {'✓' if settings.SUPABASE_KEY else '✗'}")
    
    # Initialize Supabase service
    supabase = SupabaseService()
    
    if not supabase.initialized:
        print("Error: Failed to initialize Supabase client.")
        return False
    
    # Try to get accounts from Supabase
    try:
        print("\nTrying to fetch accounts from Supabase...")
        accounts = supabase.get_accounts()
        print(f"Successfully retrieved {len(accounts)} accounts!")
        
        # Display a sample account
        if accounts:
            print("\nSample account data:")
            print(f"Name: {accounts[0].name}")
            print(f"Industry: {accounts[0].industry}")
            return True
        else:
            print("No accounts found in the database.")
            return True  # Connection successful, just no data
        
    except Exception as e:
        print(f"Error connecting to Supabase: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n✅ Supabase connection test passed!")
    else:
        print("\n❌ Supabase connection test failed.")
