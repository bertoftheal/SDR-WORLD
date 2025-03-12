"""
Test script for the SDR Assistant application.
This script tests the main functionality of the application.
"""
import sys
import os
import logging

# Add the parent directory to the path so we can import the application
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdr_assistant.config.settings import settings
from sdr_assistant.core.accounts import account_manager
from sdr_assistant.core.research import research_manager
from sdr_assistant.core.auth import auth_manager


def setup_logging():
    """Setup logging for the test script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def test_settings():
    """Test settings configuration."""
    logger.info("Testing settings...")
    logger.info(f"Airtable configured: {settings.is_airtable_configured()}")
    logger.info(f"Perplexity API configured: {'Yes' if settings.PERPLEXITY_API_KEY else 'No'}")
    logger.info(f"OpenAI API configured: {'Yes' if settings.OPENAI_API_KEY else 'No'}")


def test_accounts():
    """Test account retrieval."""
    logger.info("Testing account retrieval...")
    accounts = account_manager.get_accounts()
    logger.info(f"Retrieved {len(accounts)} accounts")
    for account in accounts[:3]:  # Show first 3 accounts
        logger.info(f"Account: {account.id} - {account.name}")


def test_auth():
    """Test authentication."""
    logger.info("Testing authentication...")
    # Test with correct credentials
    user = auth_manager.authenticate_user("demo@codeium.com", "password123")
    if user:
        logger.info(f"Authentication successful for user: {user['name']}")
        token = auth_manager.generate_token(user['id'])
        logger.info(f"Generated token: {token[:20]}...")
        
        # Test token verification
        user_id = auth_manager.verify_token(token)
        logger.info(f"Verified token, user_id: {user_id}")
    else:
        logger.error("Authentication failed")
    
    # Test with incorrect credentials
    user = auth_manager.authenticate_user("demo@codeium.com", "wrongpassword")
    if user:
        logger.error("Authentication succeeded with incorrect password!")
    else:
        logger.info("Authentication correctly failed with wrong password")


def test_research_generation():
    """Test research generation."""
    logger.info("Testing research generation...")
    # Use a real company name for better results
    result = research_manager.generate_research("Microsoft")
    
    if result["success"]:
        logger.info("Research generation successful")
        logger.info(f"Industry insights sample: {result['industryInsights'][:100]}...")
        logger.info(f"Company insights sample: {result['companyInsights'][:100]}...")
        logger.info(f"Vision insights sample: {result['visionInsights'][:100]}...")
        logger.info(f"Talk track sample: {result['recommendedTalkTrack'][:100]}...")
    else:
        logger.error(f"Research generation failed: {result['message']}")


if __name__ == "__main__":
    logger = setup_logging()
    
    logger.info("Starting SDR Assistant tests...")
    
    # Run tests
    test_settings()
    test_accounts()
    test_auth()
    
    # Uncomment to test AI research generation (may incur API costs)
    # test_research_generation()
    
    logger.info("Tests completed")
