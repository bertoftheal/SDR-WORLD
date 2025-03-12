"""
SDR Research Assistant Application
-----------------------------------
This application serves as a research tool for sales development representatives at Codeium.
It uses the Perplexity API to generate insights about companies and industries, and the OpenAI API 
to create a recommended talk track. The data can be stored in and retrieved from Airtable.

APIs Used:
- Perplexity API: For generating industry, company, and forward-thinking insights
- OpenAI API: For generating the recommended talk track
- Airtable API: For storing and retrieving account data and research

Main Functionality:
1. Retrieve accounts from Airtable (or use mock data if not configured)
2. Generate insights for selected accounts using AI
3. Save generated insights back to Airtable
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import logging
import os

# Import application configuration
from sdr_assistant.config.settings import settings

# Import route registrar
from sdr_assistant.api.routes import register_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask application instance
    """
    # Create Flask app - ensure static folder is correctly set
    app = Flask(__name__, static_folder='static')
    
    # Configure CORS
    CORS(app)
    
    # Register routes (API and static file routes)
    register_routes(app)
    
    # Application version - match the original version
    app.config['VERSION'] = '1.0.3'
    
    # Log configuration status
    logger.info(f"Airtable configured: {settings.is_airtable_configured()}")
    logger.info(f"Perplexity API configured: {'Yes' if settings.PERPLEXITY_API_KEY else 'No'}")
    logger.info(f"OpenAI API configured: {'Yes' if settings.OPENAI_API_KEY else 'No'}")
    
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
