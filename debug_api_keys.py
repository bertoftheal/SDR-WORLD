#!/usr/bin/env python3
"""
Debug script to check API key configuration and API connectivity.
"""
import os
import sys
from sdr_assistant.config.settings import settings
from sdr_assistant.services.openai_service import OpenAIService
from sdr_assistant.services.perplexity_service import PerplexityService

def debug_settings():
    """Debug environment variables and settings"""
    print("\n===== SETTINGS DEBUG =====")
    print(f"Environment loaded from: {os.path.dirname(os.path.dirname(__file__))}/.env")
    
    # Check for API keys without printing the actual keys
    perplexity_key = settings.PERPLEXITY_API_KEY
    openai_key = settings.OPENAI_API_KEY
    
    print(f"Perplexity API Key configured: {bool(perplexity_key)}")
    if perplexity_key:
        print(f"  Key begins with: {perplexity_key[:4]}{'*' * 12}")
        print(f"  Key length: {len(perplexity_key)} characters")
    
    print(f"OpenAI API Key configured: {bool(openai_key)}")
    if openai_key:
        print(f"  Key begins with: {openai_key[:4]}{'*' * 12}")
        print(f"  Key length: {len(openai_key)} characters")

def test_perplexity_api():
    """Test Perplexity API connectivity with a simple request"""
    print("\n===== PERPLEXITY API TEST =====")
    perplexity_service = PerplexityService()
    
    # Simple test prompt
    test_prompt = "What are the latest trends in software development?"
    print("Sending test request to Perplexity API...")
    
    try:
        result = perplexity_service._make_perplexity_request(test_prompt)
        if result:
            print("\nAPI RESPONSE SUCCESS! First 100 characters:")
            print(result[:100] + "...")
        else:
            print("\nAPI request failed. Check the error messages above.")
    except Exception as e:
        print(f"Exception when testing Perplexity API: {str(e)}")

def test_openai_api():
    """Test OpenAI API connectivity with a simple request"""
    print("\n===== OPENAI API TEST =====")
    openai_service = OpenAIService()
    
    # Mock data for the test
    account_name = "Example Company"
    insights = {
        "industry_insights": "Technology industry is growing rapidly.",
        "company_insights": "Example Company is expanding into new markets.",
        "vision_insights": "Future opportunities in AI and cloud computing."
    }
    
    print("Sending test request to OpenAI API...")
    try:
        result = openai_service.generate_talk_track(account_name, insights)
        if result and "# Personalized Talk Track" not in result:
            print("\nAPI RESPONSE SUCCESS! First 100 characters:")
            print(result[:100] + "...")
        else:
            print("\nAPI request failed or returned fallback response. Check error messages above.")
    except Exception as e:
        print(f"Exception when testing OpenAI API: {str(e)}")

if __name__ == "__main__":
    debug_settings()
    test_perplexity_api()
    test_openai_api()
    print("\nDebug complete.")
