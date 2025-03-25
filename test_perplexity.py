"""
Test script to check if the Perplexity API key is working correctly.
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/albertperez.codeium/Desktop/CascadeProjects/SDR-WORLD/.env')

# Get API key from environment
api_key = os.environ.get('PERPLEXITY_API_KEY')

print(f"API Key found: {'Yes' if api_key else 'No'}")

if not api_key:
    print("No Perplexity API key found in environment variables.")
    exit(1)

# Attempt to make a simple request to the Perplexity API
url = "https://api.perplexity.ai/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "sonar",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Give me a brief overview of Apple Inc."}
    ]
}

print("Making API request to Perplexity...")

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("API call successful!")
        response_data = response.json()
        print("\nResponse content:")
        print(json.dumps(response_data, indent=2))
    else:
        print(f"API call failed with status code: {response.status_code}")
        print("Response content:")
        print(response.text)
except Exception as e:
    print(f"Error making API request: {str(e)}")
