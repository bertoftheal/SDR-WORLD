"""
Custom exceptions for the SDR Assistant application.
Provides well-defined error classes for different types of failures.
"""
from typing import Optional, Dict, Any

class SDRAssistantError(Exception):
    """Base exception for all SDR Assistant errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

# API errors
class APIError(SDRAssistantError):
    """Base class for API-related errors."""
    pass

class AirtableAPIError(APIError):
    """Exception raised for Airtable API errors."""
    pass

class OpenAIAPIError(APIError):
    """Exception raised for OpenAI API errors."""
    pass

class PerplexityAPIError(APIError):
    """Exception raised for Perplexity API errors."""
    pass

# Authentication errors
class AuthError(SDRAssistantError):
    """Base class for authentication-related errors."""
    pass

class InvalidCredentialsError(AuthError):
    """Exception raised for invalid user credentials."""
    pass

class TokenExpiredError(AuthError):
    """Exception raised for expired JWT tokens."""
    pass

# Data errors
class DataError(SDRAssistantError):
    """Base class for data-related errors."""
    pass

class ValidationError(DataError):
    """Exception raised for data validation failures."""
    pass

class NotFoundError(DataError):
    """Exception raised when a requested resource is not found."""
    pass

# Utility function for handling errors
def handle_error(error: Exception, log_func=None) -> Dict[str, Any]:
    """
    Handle an exception and return a standardized error response.
    
    Args:
        error: The exception to handle
        log_func: Optional function to log the error
        
    Returns:
        Standardized error response dictionary
    """
    if isinstance(error, SDRAssistantError):
        status_code = 400
        if isinstance(error, AuthError):
            status_code = 401
        elif isinstance(error, NotFoundError):
            status_code = 404
        
        error_response = {
            "success": False,
            "error": error.message,
            "details": error.details,
            "status_code": status_code
        }
    else:
        # Generic error handler
        error_response = {
            "success": False,
            "error": str(error),
            "details": {},
            "status_code": 500
        }
    
    # Log the error if a logging function is provided
    if log_func:
        log_func(f"Error: {error_response['error']} - Details: {error_response['details']}")
    
    return error_response
