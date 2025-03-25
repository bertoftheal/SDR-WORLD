#!/usr/bin/env python
"""
Direct test of Supabase connection without using the settings system.
This will help isolate if the issue is with settings or with Supabase itself.
"""

import os
import sys
from supabase import create_client

# Hard-coded credentials for testing
SUPABASE_URL = "https://mdyaumihbrjconickcdy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1keWF1bWloYnJqY29uaWNrY2R5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk3NzI3MzksImV4cCI6MjA1NTM0ODczOX0.ipnIPCiqGx61HJhhAaf_GBoGyIDVYZzrYN5AG9_c4t8"

def test_direct_connection():
    """Test connection directly to Supabase without using the settings system."""
    print("Testing direct Supabase connection...")
    print(f"Supabase URL: {SUPABASE_URL}")
    print(f"Supabase Key: {'✓ (set)' if SUPABASE_KEY else '✗ (not set)'}")
    
    try:
        # Create Supabase client directly
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Test a simple query to fetch accounts
        print("\nAttempting to query Supabase 'accounts' table...")
        response = client.from_('accounts').select('*').execute()
        
        # Check response
        if hasattr(response, 'data'):
            print(f"Success! Retrieved {len(response.data)} accounts from Supabase.")
            if response.data:
                print("\nSample account data:")
                print(f"ID: {response.data[0].get('id')}")
                print(f"Name: {response.data[0].get('name')}")
                print(f"Industry: {response.data[0].get('industry')}")
            return True
        else:
            print("Error: Unexpected response format")
            return False
            
    except Exception as e:
        print(f"Error connecting to Supabase: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_direct_connection()
    if success:
        print("\n✅ Direct Supabase connection test passed!")
    else:
        print("\n❌ Direct Supabase connection test failed.")
