"""
Tests for the Research Manager core functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from sdr_assistant.core.research import ResearchManager

@pytest.fixture
def research_manager():
    """Fixture to create a ResearchManager instance for testing."""
    with patch('sdr_assistant.core.research.AirtableService'), \
         patch('sdr_assistant.core.research.PerplexityService'), \
         patch('sdr_assistant.core.research.OpenAIService'):
        yield ResearchManager()

@patch('sdr_assistant.core.research.account_manager')
def test_generate_research_account_not_found(mock_account_manager, research_manager):
    """Test generate_research when account is not found."""
    # Mock account_manager to return None (account not found)
    mock_account_manager.get_account_by_name.return_value = None
    
    # Test the method
    result = research_manager.generate_research("Non-existent Account")
    
    # Assert we get an error response
    assert result["success"] == False
    assert "not found" in result["message"]

@patch('sdr_assistant.core.research.account_manager')
def test_generate_research_success(mock_account_manager, research_manager):
    """Test successful research generation."""
    # Mock account_manager to return an account
    mock_account_manager.get_account_by_name.return_value = {
        "id": "test_id",
        "name": "Test Company"
    }
    
    # Mock the service methods to return test data
    research_manager.perplexity_service.generate_insights.return_value = (
        "Industry insights", "Company insights", "Vision insights"
    )
    research_manager.openai_service.generate_talk_track.return_value = "Talk track"
    
    # Test the method
    result = research_manager.generate_research("Test Company")
    
    # Assert we get expected response
    assert result["success"] == True
    assert result["industry_insights"] == "Industry insights"
    assert result["company_insights"] == "Company insights"
    assert result["vision_insights"] == "Vision insights"
    assert result["talk_track"] == "Talk track"

@patch('sdr_assistant.core.research.account_manager')
def test_generate_research_api_failure(mock_account_manager, research_manager):
    """Test research generation with API failures."""
    # Mock account_manager to return an account
    mock_account_manager.get_account_by_name.return_value = {
        "id": "test_id",
        "name": "Test Company"
    }
    
    # Mock perplexity service to simulate an error
    research_manager.perplexity_service.generate_insights.side_effect = Exception("API error")
    
    # Test the method - should not raise exception
    result = research_manager.generate_research("Test Company")
    
    # Assert we still get a result with fallback data
    assert result["success"] == True
    assert "Test Company" in result["industry_insights"]
