"""Configuration settings for SDR Assistant application.
Loads environment variables and provides a centralized place to manage configurations.
"""
import os
from dotenv import load_dotenv

class Settings:
    """Singleton class to manage application settings and configuration."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._load_environment()
        return cls._instance
    
    def _load_environment(self):
        """Load environment variables from .env files with proper fallback mechanism."""
        loaded = False
        
        # Try to load environment variables from virtual environment .env file first
        venv_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'venv (backend)', '.env')
        if os.path.exists(venv_env_path):
            print(f"Loading environment from: {venv_env_path}")
            load_dotenv(venv_env_path, override=True)  # Use the venv .env file with priority
            loaded = True
            
        # Fall back to project-level .env file
        project_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        if os.path.exists(project_env_path):
            print(f"Loading environment from: {project_env_path}")
            load_dotenv(project_env_path, override=True)
            loaded = True
            
        # As a last resort, just try to load from any .env in the current directory
        if not loaded:
            print("Attempting to load .env from current directory")
            load_dotenv(override=True)
        
        # Configure API keys
        self.AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
        self.AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
        self.AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME', 'Companies')
        self.PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.CLEARBIT_API_KEY = os.getenv('CLEARBIT_API_KEY')
        
        # Supabase configuration
        self.SUPABASE_URL = os.getenv('SUPABASE_URL')
        self.SUPABASE_KEY = os.getenv('SUPABASE_KEY')
        
        # JWT settings
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-secret-key-replace-in-production')
        self.JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', '86400'))  # Default: 24 hours
        
        # App settings
        self.DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
        self.PORT = int(os.getenv('PORT', '5001'))
        self.VERSION = '1.0.3'  # App version

    def is_airtable_configured(self):
        """Check if Airtable credentials are properly configured."""
        return (
            self.AIRTABLE_API_KEY is not None and 
            self.AIRTABLE_BASE_ID is not None and 
            self.AIRTABLE_TABLE_NAME is not None
        )
        
    def is_supabase_configured(self):
        """Check if Supabase credentials are properly configured."""
        url_configured = self.SUPABASE_URL is not None and self.SUPABASE_URL != ''
        key_configured = self.SUPABASE_KEY is not None and self.SUPABASE_KEY != ''
        
        # For debugging
        if not url_configured:
            print("SUPABASE_URL is not configured")
        if not key_configured:
            print("SUPABASE_KEY is not configured")
            
        return url_configured and key_configured

# Create a singleton instance for easy import
settings = Settings()
