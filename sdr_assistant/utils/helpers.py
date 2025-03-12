"""
Helper utility functions for the SDR Assistant application.
Contains reusable functions that don't fit elsewhere in the architecture.
"""
import re
import json
import datetime
from typing import Dict, Any, Optional, Union

def sanitize_string(text: str) -> str:
    """
    Sanitize a string by removing special characters and extra whitespace.
    
    Args:
        text: The string to sanitize
        
    Returns:
        Sanitized string
    """
    if not text:
        return ""
    
    # Remove special characters except spaces, alphanumerics, and common punctuation
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def json_serialize(obj: Any) -> Any:
    """
    Custom JSON serializer for handling datetime objects and other non-serializable types.
    
    Args:
        obj: The object to serialize
        
    Returns:
        JSON-serializable representation of the object
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    
    # Add other custom serializations as needed
    return str(obj)

def to_json(data: Any) -> str:
    """
    Convert data to a JSON string with custom serialization.
    
    Args:
        data: Data to convert to JSON
        
    Returns:
        JSON string
    """
    return json.dumps(data, default=json_serialize, indent=2)

def from_json(json_str: str) -> Any:
    """
    Parse a JSON string to a Python object.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed Python object
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None

def format_response(success: bool, data: Any = None, message: str = "", status_code: int = 200) -> Dict[str, Any]:
    """
    Format a standardized API response.
    
    Args:
        success: Whether the operation was successful
        data: Optional data to include in the response
        message: Optional message to include in the response
        status_code: HTTP status code
        
    Returns:
        Formatted response dictionary
    """
    response = {
        "success": success,
        "status_code": status_code
    }
    
    if data is not None:
        response["data"] = data
        
    if message:
        response["message"] = message
        
    return response

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Optional[str]:
    """
    Validate that all required fields are present in the data.
    
    Args:
        data: Data dictionary to validate
        required_fields: List of required field names
        
    Returns:
        Error message if validation fails, None otherwise
    """
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}"
    
    return None