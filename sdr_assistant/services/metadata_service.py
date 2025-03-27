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
        prompt = f"""Return the following information about {company_name} in STRICTLY VALID JSON format only:

{{
  "headquarters": "Where company is headquartered (city, state/province, country)",
  "employees": "Number of employees (use + if approximate)",
  "founded": "Year founded",
  "market_cap": "Market cap (use T for trillion, B for billion)",
  "description": "2-3 sentences on what company does",
  "financial_performance": "Comprehensive overview including Revenue, growth rate, funding rounds, and market valuation",
  "performance_trend": "positive/neutral/negative",
  "product_portfolio": "Main revenue-generating products/services",
  "portfolio_header": "5-7 word title for product strategy",
  "portfolio_status": "innovation/growth/transition/established",
  "industry_trends": "Key industry trends affecting company",
  "industry_header": "5-7 word title for main industry trend",
  "industry_impact": "positive/challenging/disruptive/competitive",
  "executive_insights": "Comprehensive overview of leadership priorities, recent executive quotes, and strategic focus areas",
  "executive_header": "5-7 word title for leadership approach",
  "leadership_style": "visionary/analytical/transformative/operational"
}}

Format your response as EXACTLY one valid JSON object. If any information is unknown, use "Unknown" as the value. Do NOT include any text outside the JSON object. Do NOT include markdown code formatting, just return the raw JSON.
        """
        
        try:
            # Make the API request
            response_text = self._make_perplexity_request(prompt)
            
            if not response_text:
                return self._get_default_metadata()
                
            # Try to extract JSON from the response
            try:
                # First, try direct JSON loading (in case it's already valid JSON)
                try:
                    data = json.loads(response_text)
                    print("Successfully parsed direct JSON response")
                    
                    # Ensure all required fields exist
                    required_fields = ["headquarters", "employees", "founded", "market_cap", "description"]
                    for field in required_fields:
                        if field not in data:
                            data[field] = "Unknown"
                            
                    return data
                except json.JSONDecodeError as e:
                    # If direct loading fails, try to extract JSON using regex
                    print(f"Direct JSON parsing failed: {str(e)}, trying regex extraction")
                
                # Try to find JSON within the response using regex
                json_match = re.search(r'\{[\s\S]*?\}', response_text)
                if json_match:
                    json_str = json_match.group(0)
                    
                    # Print the extracted JSON for debugging
                    print(f"Extracted JSON string (first 100 chars): {json_str[:100]}...")
                    
                    try:
                        # Advanced JSON cleaning
                        # 1. Fix missing commas between key-value pairs
                        json_str = re.sub(r'("[^"]+":\s*"[^"]+")\s*("[^"]+":)', r'\1,\2', json_str)
                        
                        # 2. Fix missing quotes around keys
                        json_str = re.sub(r'([{,])\s*([\w_]+):', r'\1"\2":', json_str)
                        
                        # 3. Fix missing quotes around string values
                        json_str = re.sub(r':\s*([^\s",{}\[\]0-9][^,}]*?)([,}])', r':"\1"\2', json_str)
                        
                        # 4. Replace any single quotes with double quotes
                        json_str = json_str.replace("'", "\"")
                        
                        print(f"Cleaned JSON (first 100 chars): {json_str[:100]}...")
                        
                        # Try to parse the cleaned JSON
                        data = json.loads(json_str)
                        print("Successfully parsed JSON after cleanup")
                        
                        # Ensure all required fields exist
                        required_fields = ["headquarters", "employees", "founded", "market_cap", "description"]
                        for field in required_fields:
                            if field not in data:
                                data[field] = "Unknown"
                                
                        return data
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON after cleanup: {str(e)}")
                        print(f"Problematic JSON position: {e.pos}, line: {e.lineno}, col: {e.colno}")
                        print(f"JSON substring at error: {json_str[max(0, e.pos-20):min(len(json_str), e.pos+20)]}")
                        
                        # Last resort: Try to manually fix common issues
                        try:
                            print("Attempting manual JSON repair...")
                            json_lines = json_str.split('\n')
                            
                            # Get more debugging info
                            if len(json_lines) >= 6:
                                print(f"Line 5: {json_lines[5]}")
                                if len(json_lines) > 6:
                                    print(f"Line 6: {json_lines[6]}")
                            
                            # Apply multiple fixes
                            if e.lineno == 6 and e.colno <= 10:
                                if len(json_lines) >= 6:
                                    # Fix 1: Add missing comma at the end of line 5
                                    json_lines[5] = json_lines[5].rstrip() + ','
                                    print(f"Fixed line 5, adding comma: {json_lines[5]}")
                                    
                                    # Fix 2: Ensure line 6 has proper property name format
                                    if len(json_lines) > 6 and json_lines[6].strip() and not json_lines[6].strip().startswith('"'):
                                        # Extract property name and add quotes
                                        line6_parts = json_lines[6].strip().split(':',1)
                                        if len(line6_parts) > 0:
                                            property_name = line6_parts[0].strip()
                                            remaining = ':' + line6_parts[1] if len(line6_parts) > 1 else ''
                                            # Add quotes around property name
                                            json_lines[6] = json_lines[6].replace(property_name, f'"{property_name}"', 1)
                                            print(f"Fixed line 6, adding quotes: {json_lines[6]}")
                                    
                                    # Apply fixes and try parsing
                                    fixed_json = '\n'.join(json_lines)
                                    try:
                                        data = json.loads(fixed_json)
                                        print("Successfully parsed JSON after manual fixes")
                                        
                                        # Ensure all required fields exist
                                        for field in required_fields:
                                            if field not in data:
                                                data[field] = "Unknown"
                                                
                                        return data
                                    except json.JSONDecodeError as nested_error:
                                        print(f"First manual fix failed: {str(nested_error)}")
                                        
                                        # More aggressive fix - create valid JSON with cleaned fields
                                        print("Attempting more aggressive JSON repair...")
                                        # Try to create clean JSON manually
                                        clean_json = "{"
                                        for line in json_lines[1:]:  # Skip first line opening brace
                                            line = line.strip()
                                            if line and not line.startswith('{') and not line.endswith('}'):
                                                # Extract property and value
                                                parts = line.split(':', 1)
                                                if len(parts) == 2:
                                                    prop = parts[0].strip().strip('"').strip()
                                                    val = parts[1].strip().rstrip(',').strip()
                                                    # Format as proper JSON
                                                    clean_json += f'"{prop}": {val},'
                                        # Remove last comma and close
                                        clean_json = clean_json.rstrip(',') + "}"
                                        print(f"Created clean JSON: {clean_json[:100]}...")
                                        
                                        try:
                                            data = json.loads(clean_json)
                                            print("Successfully parsed clean JSON")
                                            return data
                                        except Exception as e2:
                                            print(f"Clean JSON failed: {str(e2)}")
                        except Exception as manual_fix_error:
                            print(f"Manual JSON fix failed: {str(manual_fix_error)}")
                            
                        # Ultimate fallback - use regex to extract fields one by one
                        print("Using field-by-field extraction as last resort")
                        # Create a default object with all required fields
                        data = {
                            "headquarters": "Unknown",
                            "employees": "Unknown",
                            "founded": "Unknown",
                            "market_cap": "Unknown",
                            "description": "Unknown",
                            "financial_performance": "Unknown",
                            "performance_trend": "neutral",
                            "product_portfolio": "Unknown",
                            "portfolio_header": "Diverse product and service offerings",
                            "portfolio_status": "established",
                            "industry_trends": "Unknown",
                            "industry_header": "Evolving industry landscape and trends",
                            "industry_impact": "challenging",
                            "executive_insights": "Unknown",
                            "executive_header": "Strategic leadership and vision", 
                            "leadership_style": "visionary"
                        }
                        
                        # Try to extract each field from the response text
                        field_patterns = {
                            "headquarters": r'"headquarters"\s*:\s*"([^"]+)"',
                            "employees": r'"employees"\s*:\s*"([^"]+)"',
                            "founded": r'"founded"\s*:\s*"([^"]+)"',
                            "market_cap": r'"market[_\s]cap"\s*:\s*"([^"]+)"',
                            "description": r'"description"\s*:\s*"([^"]+)"',
                            "financial_performance": r'"financial[_\s]performance"\s*:\s*"([^"]+)"',
                            "performance_trend": r'"performance[_\s]trend"\s*:\s*"([^"]+)"',
                            "product_portfolio": r'"product[_\s]portfolio"\s*:\s*"([^"]+)"',
                            "portfolio_header": r'"portfolio[_\s]header"\s*:\s*"([^"]+)"',
                            "portfolio_status": r'"portfolio[_\s]status"\s*:\s*"([^"]+)"',
                            "industry_trends": r'"industry[_\s]trends"\s*:\s*"([^"]+)"',
                            "industry_header": r'"industry[_\s]header"\s*:\s*"([^"]+)"',
                            "industry_impact": r'"industry[_\s]impact"\s*:\s*"([^"]+)"',
                            "executive_insights": r'"executive[_\s]insights"\s*:\s*"([^"]+)"',
                            "executive_header": r'"executive[_\s]header"\s*:\s*"([^"]+)"',
                            "leadership_style": r'"leadership[_\s]style"\s*:\s*"([^"]+)"'
                        }
                        
                        # For each field, try to find it in the response
                        for field, pattern in field_patterns.items():
                            match = re.search(pattern, response_text)
                            if match:
                                data[field] = match.group(1)
                                print(f"Extracted {field}: {data[field][:30]}...")
                        
                        print("Field-by-field extraction complete")
                        return data
            except Exception as e:
                print(f"Error processing Perplexity response: {str(e)}")
                    
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
                {"role": "system", "content": "You are a helpful assistant that provides EXACTLY formatted JSON. Always structure your ENTIRE response as a VALID JSON object. NEVER add explanations or markdown formatting. Use double quotes for ALL keys and string values. Include commas between ALL key-value pairs, but NO trailing commas. Proper JSON formatting is CRITICAL."},
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
            print(f"DEBUG: API response structure: {list(response_data.keys())}")
            
            # Extract the content from the response
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"DEBUG: Raw API content (first 150 chars): {content[:150]}...")
            
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
