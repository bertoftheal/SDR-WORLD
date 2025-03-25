"""
API routes for account management functionality.
"""
from flask import Blueprint, jsonify, request
from typing import Dict, Any
import requests
import os

from ..core.auth import auth_manager
from ..core.accounts import account_manager
from ..config import settings


accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts", methods=["GET"])
@accounts_bp.route("/accounts/list", methods=["GET"])
def get_accounts():
    """
    API Route: Retrieve accounts
    
    Fetches accounts from Supabase (with Airtable as fallback) or returns mock account data.
    
    Returns:
        JSON array of accounts with 'id' and 'name' properties
    """
    accounts = account_manager.get_accounts()
    
    # Convert to simple format with just id and name
    account_list = [{"id": account.id, "name": account.name} for account in accounts]
    
    return jsonify(account_list)


@accounts_bp.route("/accounts/details", methods=["GET"])
def get_account_details():
    """
    API Route: Get detailed account information
    
    Returns accounts with additional details like industry, employees, and location.
    
    Returns:
        JSON array of account objects with detailed information
    """
    accounts = account_manager.get_accounts()
    
    # Convert to detailed format
    account_details = [account.to_dict() for account in accounts]
    
    return jsonify(account_details)


@accounts_bp.route("/accounts/search", methods=["GET"])
def search_accounts():
    """
    API Route: Search for accounts by name
    
    Searches existing accounts and returns matches. If no exact match is found,
    generates company information using Perplexity API and gets a logo URL from Clearbit.
    If all else fails, creates a basic placeholder account entry.
    
    Query parameters:
        name: Company name to search for
    
    Returns:
        JSON object with account information
    """
    search_term = request.args.get("name", "")
    
    if not search_term:
        return jsonify({"success": False, "message": "Search term is required"}), 400
    
    # First check if we have this account in our database
    accounts = account_manager.get_accounts()
    
    # Try to find a case-insensitive match
    for account in accounts:
        if account.name.lower() == search_term.lower():
            return jsonify({
                "success": True, 
                "account": account.to_dict(),
                "source": "database"
            })
    
    # For new companies, get information from Perplexity API (primary source for research)
    perplexity_info = fetch_company_info_perplexity(search_term)
    
    # Always try to get a logo from Clearbit (regardless of Perplexity success)
    logo_url = get_company_logo(search_term)
    
    if perplexity_info and perplexity_info.get("success"):
        # We have AI-generated company information, add logo to it
        company_info = perplexity_info.get("company")
        company_info["logo_url"] = logo_url
        
        return jsonify({
            "success": True,
            "account": company_info,
            "source": "perplexity"
        })
    
    # If Perplexity fails, create a basic account with just the name and logo
    basic_account = {
        "id": "",  # Will be assigned if saved
        "name": search_term,
        "industry": "Unknown",
        "headquarters": "Unknown",
        "employees": "Unknown",
        "logo_url": logo_url,  # Using the Clearbit logo if available
        "description": f"Information for {search_term} not available.",
        "market_cap": "Unknown",
        "founded": "Unknown"
    }
    
    return jsonify({
        "success": True,
        "account": basic_account,
        "source": "generated"
    })


def get_company_logo(company_name: str) -> str:
    """
    Get a company logo URL from Clearbit's Logo API
    
    This function uses Clearbit's free logo API to retrieve a company logo
    based on the company name. This service only requires the company name
    and does not need an API key.
    
    Args:
        company_name: Name of the company to get a logo for
    
    Returns:
        Logo URL as a string, or empty string if unavailable
    """
    try:
        # Clean the company name for use in a domain-like format
        clean_name = company_name.lower().replace(' ', '').replace(',', '').replace('.', '')
        
        # Use Clearbit's logo API - this doesn't require an API key
        logo_url = f"https://logo.clearbit.com/{clean_name}.com"
        
        # Test if the logo exists by sending a HEAD request
        response = requests.head(logo_url, timeout=2)
        
        if response.status_code == 200:
            return logo_url
        else:
            # Try an alternative format (some companies use .co, .io, etc.)
            alt_formats = ['.co', '.io', '.org', '.net']
            for format in alt_formats:
                alt_url = f"https://logo.clearbit.com/{clean_name}{format}"
                alt_response = requests.head(alt_url, timeout=1)
                if alt_response.status_code == 200:
                    return alt_url
            
            # If all else fails, return an empty string
            return ""
    
    except Exception as e:
        print(f"Error fetching logo: {e}")
        return ""


def fetch_company_info_perplexity(company_name: str) -> Dict[str, Any]:
    """
    Fetch company information using Perplexity AI API
    
    This function uses the Perplexity API to generate structured company information
    when traditional data sources like Clearbit fail to provide information.
    
    Args:
        company_name: Name of the company to search for
    
    Returns:
        Dictionary with AI-generated company information or error details
    """
    perplexity_api_key = settings.PERPLEXITY_API_KEY
    
    if not perplexity_api_key:
        return {"success": False, "message": "Perplexity API key not configured"}
    
    try:
        # Construct a prompt that requests structured company information
        prompt = f"""Please provide detailed information about {company_name} in JSON format with the following fields:
        - name: The full legal name of the company
        - industry: The primary industry the company operates in
        - headquarters: City and country where the company is headquartered
        - employees: Approximate number of employees (just the number, no text)
        - description: A 1-2 sentence description of what the company does
        - market_cap: Approximate market capitalization if publicly traded
        - founded: Year the company was founded
        - logo_url: Leave blank
        
        Only respond with valid JSON. Don't include markdown formatting or any other text.
        """
        
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {perplexity_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mixtral-8x7b-instruct",  # Using Mixtral model for structured output
            "messages": [{
                "role": "system",
                "content": "You are a helpful assistant that provides accurate, structured information about companies. Respond only with JSON data."
            }, {
                "role": "user",
                "content": prompt
            }],
            "max_tokens": 1024
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        
        # Try to extract JSON from the response
        # The model might sometimes wrap the JSON in markdown or add extra text
        import json
        import re
        
        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', ai_response)
        if json_match:
            ai_response = json_match.group(0)
        
        # Parse the JSON response
        try:
            company_data = json.loads(ai_response)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a basic structure with the error
            return {"success": False, "message": f"Failed to parse AI response as JSON"}
        
        # Ensure we have all expected fields
        company = {
            "id": "",  # Will be assigned if saved
            "name": company_data.get("name", company_name),
            "industry": company_data.get("industry", "Unknown"),
            "headquarters": company_data.get("headquarters", "Unknown"),
            "employees": company_data.get("employees", "Unknown"),
            "logo_url": "",  # We'll leave this blank or use a placeholder
            "description": company_data.get("description", f"Information for {company_name} not fully available."),
            "market_cap": company_data.get("market_cap", "Unknown"),
            "founded": company_data.get("founded", "Unknown")
        }
        
        # Set empty logo URL - logos are handled separately by get_company_logo
        company["logo_url"] = ""
        
        return {"success": True, "company": company}
    
    except Exception as e:
        return {"success": False, "message": f"Error getting AI-generated company data: {str(e)}"}
