import os
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)

# Print environment variables
print(f"AIRTABLE_API_KEY: {os.getenv('AIRTABLE_API_KEY')}")
print(f"AIRTABLE_BASE_ID: {os.getenv('AIRTABLE_BASE_ID')}")
print(f"AIRTABLE_TABLE_NAME: {os.getenv('AIRTABLE_TABLE_NAME')}")
