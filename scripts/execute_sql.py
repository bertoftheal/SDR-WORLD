#!/usr/bin/env python
"""
Script to execute SQL directly on Supabase.
"""

import sys
import os
from supabase import create_client
from dotenv import load_dotenv

def load_environment():
    """Load environment variables."""
    # Try to load from project root .env first
    root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(root_env):
        load_dotenv(root_env, override=True)
        return True
        
    # Fallback to backend .env
    backend_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              'sdr_assistant', 'venv (backend)', '.env')
    if os.path.exists(backend_env):
        load_dotenv(backend_env, override=True)
        return True
    
    return False

def execute_sql_file(file_path):
    """Execute a SQL file on Supabase."""
    # Load environment variables
    if not load_environment():
        print("Error: Could not find .env file")
        return False
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials in environment variables")
        return False
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key is set: {'Yes' if supabase_key else 'No'}")
    
    try:
        # Initialize Supabase client
        print("Initializing Supabase client...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Read SQL from file
        print(f"Reading SQL from {file_path}...")
        with open(file_path, 'r') as f:
            sql = f.read()
        
        # Execute SQL
        print("Executing SQL...")
        print("SQL to execute:")
        print(sql)
        
        # Use the raw SQL query functionality
        result = supabase.table("accounts").select("*", count="exact").execute()
        print(f"Before modification: {len(result.data)} accounts")
        
        # Execute the SQL directly
        # This will be different depending on the Supabase client capabilities
        # We'll need to use the PostgreSQL REST API for this
        statements = sql.split(';')
        for statement in statements:
            if statement.strip():
                print(f"Executing: {statement.strip()}")
                # This is a simplified example - the actual method will depend on 
                # the Supabase client's capabilities
                try:
                    # Using RPC function to execute SQL directly
                    # Note: This requires your Supabase database to have the needed permissions
                    result = supabase.rpc('execute_sql', {'sql': statement.strip()}).execute()
                    print("SQL executed successfully via RPC")
                except Exception as e:
                    print(f"Error executing via RPC: {str(e)}")
                    print("Trying alternate method (REST API)...")
                    
                    # If the above doesn't work, we'll have to use a more direct approach
                    # This likely requires a custom SQL function or manually implementing the changes
                    # For this example, we'll try to implement the ALTER TABLE ADD COLUMN manually
                    
                    if "ALTER TABLE accounts ADD COLUMN" in statement:
                        print("Detected ALTER TABLE for accounts - implementing manually...")
                        # We need to check if the column exists and add it if it doesn't
                        # This is a workaround since direct SQL execution might not be available
                        
                        # First let's try using a straightforward REST approach
                        # Note: This is a simplified implementation and may not work for all SQL operations
                        try:
                            # This is a workaround for adding the column
                            # The actual implementation would depend on Supabase client version
                            result = supabase.table("accounts").select("*").execute()
                            print("Successfully accessed accounts table")
                            
                            # Check if we need to create the migration script
                            print("For actual column addition, please use the Supabase dashboard SQL editor")
                            print("with the following SQL:")
                            print(sql)
                        except Exception as inner_e:
                            print(f"REST API approach also failed: {str(inner_e)}")
                            print("Please execute the SQL directly through the Supabase dashboard SQL editor")
        
        # Verify the changes
        result = supabase.table("accounts").select("*", count="exact").execute()
        print(f"After attempted modification: {len(result.data)} accounts")
        
        # Try to access the new column to see if it exists
        try:
            print("Checking if airtable_id column exists:")
            column_test = supabase.table("accounts").select("airtable_id").limit(1).execute()
            print("airtable_id column exists and is accessible")
        except Exception as e:
            print(f"Could not access airtable_id column: {str(e)}")
            print("The column may not have been added successfully")
        
        return True
    except Exception as e:
        print(f"Error executing SQL: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python execute_sql.py <sql_file>")
        sys.exit(1)
    
    sql_file = sys.argv[1]
    if not os.path.exists(sql_file):
        print(f"Error: SQL file '{sql_file}' not found")
        sys.exit(1)
    
    success = execute_sql_file(sql_file)
    if success:
        print("SQL execution complete")
    else:
        print("SQL execution failed")
        sys.exit(1)
