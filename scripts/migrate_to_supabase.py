#!/usr/bin/env python
"""
Migration script to transfer data from Airtable to Supabase.
This script will migrate all account and research data from your Airtable
database to your new Supabase database.
"""

import os
import sys
import time
from datetime import datetime

# Add the parent directory to the path to import from the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdr_assistant.services.airtable_service import AirtableService
from sdr_assistant.services.supabase_service import SupabaseService
from sdr_assistant.config.settings import settings


def migrate_accounts():
    """Migrate accounts from Airtable to Supabase."""
    print("Starting account migration...")
    
    # Initialize services
    airtable = AirtableService()
    supabase = SupabaseService()
    
    # Get all accounts from Airtable
    airtable_accounts = airtable.get_accounts()
    
    if not airtable_accounts:
        print("No accounts found in Airtable.")
        return
    
    print(f"Found {len(airtable_accounts)} accounts in Airtable.")
    
    # For each account, create a record in Supabase
    migrated_count = 0
    for account in airtable_accounts:
        # Convert Airtable account to a format for Supabase
        supabase_account = {
            'name': account.name,
            'industry': account.industry,
            'location': account.location,
            'employees': str(account.employees) if account.employees else None,
            'revenue': account.revenue,
            'website': account.website,
            'description': account.description,
            'created_at': datetime.now().isoformat(),
            'airtable_id': account.id  # Store original Airtable ID for reference
        }
        
        try:
            # Insert account into Supabase
            result = supabase.client.from_('accounts').insert(supabase_account).execute()
            
            if result.data:
                migrated_count += 1
                print(f"Migrated account: {account.name}")
            else:
                print(f"Failed to migrate account: {account.name}")
                
            # Avoid rate limits
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error migrating account {account.name}: {str(e)}")
    
    print(f"Account migration complete. Migrated {migrated_count} of {len(airtable_accounts)} accounts.")


def migrate_research():
    """Migrate research data from Airtable to Supabase."""
    print("Starting research migration...")
    
    # Initialize services
    airtable = AirtableService()
    supabase = SupabaseService()
    
    # We need to map Airtable account IDs to Supabase account IDs
    # Get all accounts from Supabase with their Airtable IDs
    account_mapping = {}
    try:
        response = supabase.client.from_('accounts').select('id, airtable_id').execute()
        if response.data:
            for account in response.data:
                if 'airtable_id' in account and account['airtable_id']:
                    account_mapping[account['airtable_id']] = account['id']
    except Exception as e:
        print(f"Error fetching account mapping: {str(e)}")
        return
    
    if not account_mapping:
        print("No account mapping available. Make sure to migrate accounts first.")
        return
    
    # Get all research from Airtable
    airtable_research = airtable.get_all_research()
    
    if not airtable_research:
        print("No research found in Airtable.")
        return
    
    print(f"Found {len(airtable_research)} research records in Airtable.")
    
    # For each research, create a record in Supabase
    migrated_count = 0
    for research in airtable_research:
        # Skip if we don't have a mapping for this account
        if research.account_id not in account_mapping:
            print(f"Skipping research for unmapped account ID: {research.account_id}")
            continue
        
        # Convert Airtable research to a format for Supabase
        supabase_research = {
            'account_id': account_mapping[research.account_id],
            'account_name': research.account_name,
            'industry_insights': research.industry_insights,
            'company_insights': research.company_insights,
            'vision_insights': research.vision_insights,
            'talk_track': research.talk_track,
            'created_by': research.created_by,
            'created_at': research.created_at.isoformat() if research.created_at else datetime.now().isoformat(),
            'updated_at': research.updated_at.isoformat() if research.updated_at else datetime.now().isoformat(),
            'airtable_id': research.account_id  # Store original Airtable ID for reference
        }
        
        try:
            # Insert research into Supabase
            result = supabase.client.from_('research').insert(supabase_research).execute()
            
            if result.data:
                migrated_count += 1
                print(f"Migrated research for account: {research.account_name}")
            else:
                print(f"Failed to migrate research for account: {research.account_name}")
                
            # Avoid rate limits
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error migrating research for {research.account_name}: {str(e)}")
    
    print(f"Research migration complete. Migrated {migrated_count} of {len(airtable_research)} research records.")


def main():
    """Main function to run the migration."""
    # Check if Supabase is configured
    if not settings.is_supabase_configured():
        print("Error: Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
        return
    
    # Check if Airtable is configured
    if not settings.is_airtable_configured():
        print("Error: Airtable is not configured. Please set AIRTABLE_API_KEY and AIRTABLE_BASE_ID in your .env file.")
        return
    
    print("Starting migration from Airtable to Supabase...")
    
    # Migrate accounts first
    migrate_accounts()
    
    # Then migrate research
    migrate_research()
    
    print("Migration complete!")


if __name__ == "__main__":
    main()
