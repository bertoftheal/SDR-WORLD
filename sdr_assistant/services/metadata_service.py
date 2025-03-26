"""
Service for retrieving company metadata using the Perplexity API.
Provides structured company information for UI display.
"""
import json
import re
import requests
from typing import Dict, Any, Optional

from ..config.settings import settings

class MetadataService:
    """Service for retrieving structured company metadata."""
    
    def __init__(self):
        """Initialize the metadata service."""
        # Use the Perplexity API key from settings
        self.api_key = settings.PERPLEXITY_API_KEY
        
    def get_company_metadata(self, company_name: str) -> Dict[str, Any]:
        """
        Get structured company metadata using the Perplexity API.
        
        Args:
            company_name: Name of the company
            
        Returns:
            Dictionary with company metadata (headquarters, employees, founded, market_cap, description)
        """
        if not self.api_key or not company_name:
            return self._get_default_metadata()
        
        # Make Perplexity API request for structured metadata
        prompt = f"""Provide ONLY the following factual information about {company_name} in JSON format:
        - headquarters: Where is the company headquartered? (city, state/province, country)
        - employees: How many employees does the company have? (use + if approximate)
        - founded: What year was the company founded?
        - market_cap: What is the company's market cap? (for public companies, use T for trillion, B for billion)
        - description: In 2-3 sentences, what does the company do and what products/services does it offer?
        - financial_performance: In one clear sentence, summarize the current financial performance or outlook of the company.
        - performance_trend: Categorize the company's overall financial performance as one of: 'positive', 'neutral', or 'negative' based on recent financial results, stock performance, or financial outlook.
        - product_portfolio: In one clear paragraph, describe the main products/services that generate the most revenue for the company.
        - portfolio_header: Provide a concise 5-7 word title that summarizes the company's product portfolio strategy or focus.
        - portfolio_status: Categorize the company's product portfolio as one of: 'innovation' (new cutting-edge products), 'growth' (expanding existing product lines), 'transition' (shifting focus between products), or 'established' (stable, mature product lines) based on their current product strategy.
        - industry_trends: In one clear paragraph, describe the key industry trends that impact {company_name}'s business and market position.
        - industry_header: Provide a concise 5-7 word title that captures the most significant industry trend affecting the company.
        - industry_impact: Categorize the impact of current industry trends on the company as one of: 'positive' (beneficial), 'challenging' (requires adaptation), 'disruptive' (transformative), or 'competitive' (intensifying rivalry).
        
        Format your response as valid JSON only, with NO explanations, citations, or other text.
        Just return the JSON object with these 13 properties. If any information is unknown, use 'Unknown' as the value.
        """
        
        try:
            # Make the API request
            response_text = self._make_perplexity_request(prompt)
            
            if not response_text:
                return self._get_default_metadata()
                
            # Try to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*?\}', response_text)
            if json_match:
                json_str = json_match.group(0)
                try:
                    data = json.loads(json_str)
                    
                    # Ensure all required fields exist
                    required_fields = ["headquarters", "employees", "founded", "market_cap", "description"]
                    for field in required_fields:
                        if field not in data:
                            data[field] = "Unknown"
                            
                    return data
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON from Perplexity response")
                    
            # If we couldn't extract JSON, use regex to extract individual fields
            data = {}
            patterns = {
                "headquarters": r'headquarters["\':]\s*["\']*([^"\'\n\}]+)',
                "employees": r'employees["\':]\s*["\']*([^"\'\n\}]+)',
                "founded": r'founded["\':]\s*["\']*([^"\'\n\}]+)',
                "market_cap": r'market_cap["\':]\s*["\']*([^"\'\n\}]+)',
                "description": r'description["\':]\s*["\']*([^"\']+?)["\']*[,}]'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, response_text, re.IGNORECASE)
                if match:
                    data[key] = match.group(1).strip()
                else:
                    data[key] = "Unknown"
                    
            return data
        except Exception as e:
            print(f"Error getting company metadata: {str(e)}")
            return self._get_default_metadata()
    
    def _make_perplexity_request(self, prompt: str) -> Optional[str]:
        """Make a request to the Perplexity API."""
        if not self.api_key:
            print("WARNING: Perplexity API key is not configured or is empty")
            return None
            
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that provides accurate, structured data in JSON format."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            print(f"DEBUG: Making Perplexity API request for: {prompt[:50]}...")
            print(f"DEBUG: Using API key: {self.api_key[:5]}...{self.api_key[-5:] if self.api_key and len(self.api_key) > 10 else 'MISSING_KEY'}")
            
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json=data
            )
            
            print(f"DEBUG: API response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"ERROR: Perplexity API request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
            response_data = response.json()
            
            # Extract the content from the response
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Log a snippet of the content for debugging
            print(f"DEBUG: Retrieved content from API: {content[:200]}...")
            
            return content
        except Exception as e:
            print(f"ERROR making Perplexity API request: {str(e)}")
            return None
    
    def _get_default_metadata(self) -> Dict[str, str]:
        """Return default metadata when API is unavailable."""
        return {
            "headquarters": "Unknown",
            "employees": "Unknown",
            "founded": "Unknown",
            "market_cap": "Unknown",
            "description": "Unknown"
        }

# Singleton instance for easy import
metadata_service = MetadataService()
