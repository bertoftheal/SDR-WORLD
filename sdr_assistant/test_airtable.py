from pyairtable import Table
import os
from dotenv import load_dotenv

# Load environment variables, make sure to reload
load_dotenv(override=True)

# Get Airtable credentials
api_key = os.getenv('AIRTABLE_API_KEY')
base_id = os.getenv('AIRTABLE_BASE_ID')
table_name = os.getenv('AIRTABLE_TABLE_NAME')

print(f"API Key: {api_key[:10]}... (truncated)")
print(f"Base ID: {base_id}")
print(f"Table Name: {table_name}")

# Connect to Airtable
try:
    print(f"Connecting to Airtable: {base_id}/{table_name}")
    table = Table(api_key, base_id, table_name)
    records = table.all()
    print(f"Found {len(records)} records")
    
    # Print first 5 records
    for i, record in enumerate(records[:5]):
        print(f"Record {i+1}: {record.get('fields', {}).get('Name', 'No name')}")
except Exception as e:
    print(f"Error connecting to Airtable: {str(e)}")
