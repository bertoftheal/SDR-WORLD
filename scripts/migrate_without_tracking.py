#!/usr/bin/env python
"""
Migrate data from Airtable to Supabase without using airtable_id tracking.
"""

import os
import sys
import json
from pyairtable import Table
from supabase import create_client
from dotenv import load_dotenv
import uuid

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_environment():
    """Load environment variables from both possible locations."""
    # Try project root .env first
    root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(root_env):
        load_dotenv(root_env, override=True)
        
    # Also try backend .env
    backend_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              'sdr_assistant', 'venv (backend)', '.env')
    if os.path.exists(backend_env):
        load_dotenv(backend_env, override=True)

def migrate_airtable_to_supabase():
    """Migrate data from Airtable to Supabase."""
    print("Starting migration from Airtable to Supabase...")
    
    # Load environment variables
    load_environment()
    
    # Get environment variables
    airtable_api_key = os.getenv('AIRTABLE_API_KEY')
    airtable_base_id = os.getenv('AIRTABLE_BASE_ID')
    airtable_table_name = os.getenv('AIRTABLE_TABLE_NAME')
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    # Verify environment variables
    if not all([airtable_api_key, airtable_base_id, airtable_table_name, supabase_url, supabase_key]):
        missing = []
        if not airtable_api_key: missing.append("AIRTABLE_API_KEY")
        if not airtable_base_id: missing.append("AIRTABLE_BASE_ID")
        if not airtable_table_name: missing.append("AIRTABLE_TABLE_NAME")
        if not supabase_url: missing.append("SUPABASE_URL")
        if not supabase_key: missing.append("SUPABASE_KEY")
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        return False
    
    try:
        # Initialize Airtable
        airtable = Table(airtable_api_key, airtable_base_id, airtable_table_name)
        
        # Initialize Supabase
        print("Initializing Supabase client...")
        supabase = create_client(supabase_url, supabase_key)
        print("Supabase client initialized successfully")
        
        # Clear existing accounts in Supabase (optional)
        print("Clearing existing Supabase accounts for fresh migration...")
        try:
            result = supabase.table("accounts").delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
            print(f"Deleted existing accounts")
        except Exception as e:
            print(f"Error clearing accounts: {str(e)}")
        
        # Get all accounts from Airtable
        print("Starting account migration...")
        airtable_accounts = airtable.all()
        print(f"Found {len(airtable_accounts)} accounts in Airtable.")
        
        # Map for successful migrations
        account_map = {}  # Maps Airtable ID to Supabase ID
        
        # Migrate each account
        for account in airtable_accounts:
            airtable_id = account['id']
            record = account['fields']
            name = record.get('Name', 'Unnamed Account')
            
            try:
                # Create account object for Supabase
                account_data = {
                    'id': str(uuid.uuid4()),
                    'name': name,
                    'industry': record.get('Industry', ''),
                    'location': record.get('Location', ''),
                    'headquarters': record.get('Headquarters', ''),
                    'employees': record.get('Employees', ''),
                    'employee_count': record.get('Employee Count', 0),
                    'revenue': record.get('Revenue', ''),
                    'market_cap': record.get('Market Cap', ''),
                    'website': record.get('Website', ''),
                    'logo_url': record.get('Logo', ''),
                    'description': record.get('Description', ''),
                    'status': record.get('Status', 'Active'),
                }
                
                # Insert into Supabase
                result = supabase.table("accounts").insert(account_data).execute()
                
                if result and hasattr(result, 'data') and result.data:
                    account_map[airtable_id] = account_data['id']
                    print(f"Successfully migrated account {name}")
                else:
                    print(f"Error migrating account {name}: No data returned")
                    
            except Exception as e:
                print(f"Error migrating account {name}: {str(e)}")
        
        print(f"Account migration complete. Migrated {len(account_map)} of {len(airtable_accounts)} accounts.")
        
        # Migrate research if available
        try:
            print("Starting research migration...")
            # Check if research table exists in Airtable
            research_base_id = os.getenv('AIRTABLE_RESEARCH_BASE_ID', airtable_base_id)
            research_table_name = os.getenv('AIRTABLE_RESEARCH_TABLE_NAME', 'Research')
            
            # Try to get research table
            research_table = Table(airtable_api_key, research_base_id, research_table_name)
            research_records = research_table.all()
            
            print(f"Found {len(research_records)} research records in Airtable")
            
            # Clear existing research in Supabase (optional)
            try:
                result = supabase.table("research").delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
                print(f"Deleted existing research")
            except Exception as e:
                print(f"Error clearing research: {str(e)}")
            
            # Migrate each research record
            research_count = 0
            for research in research_records:
                record = research['fields']
                account_name = record.get('Company', '')
                
                # Look for matching account by name
                try:
                    # Query Supabase for the account
                    account_result = supabase.table("accounts").select("id").eq("name", account_name).execute()
                    
                    if account_result and account_result.data:
                        account_id = account_result.data[0]['id']
                        
                        # Create research record
                        research_data = {
                            'id': str(uuid.uuid4()),
                            'account_id': account_id,
                            'account_name': account_name,
                            'industry_insights': record.get('Industry Insights', ''),
                            'company_insights': record.get('Company Insights', ''),
                            'vision_insights': record.get('Vision Insights', ''),
                            'talk_track': record.get('Talk Track', '')
                        }
                        
                        # Insert into Supabase
                        result = supabase.table("research").insert(research_data).execute()
                        
                        if result and hasattr(result, 'data') and result.data:
                            research_count += 1
                            print(f"Successfully migrated research for {account_name}")
                        else:
                            print(f"Error migrating research for {account_name}: No data returned")
                    else:
                        print(f"Couldn't find matching account for research: {account_name}")
                        
                except Exception as e:
                    print(f"Error migrating research for {account_name}: {str(e)}")
            
            print(f"Research migration complete. Migrated {research_count} of {len(research_records)} research records.")
            
        except Exception as e:
            print(f"Error during research migration: {str(e)}")
        
        print("Migration complete!")
        return True
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        return False

if __name__ == "__main__":
    migrate_airtable_to_supabase()
