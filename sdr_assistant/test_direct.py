from pyairtable import Table

# Directly use the credentials you provided
api_key = "pat0uCiScQYOaAiX4.7525722c0c3e3536e7e51796fb3cf4d098cfc175091d61cf22889e99f9df634d"
base_id = "appGsSyYTq8rksZS3"
table_name = "tblIqwYXcxHVmez3n"

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
