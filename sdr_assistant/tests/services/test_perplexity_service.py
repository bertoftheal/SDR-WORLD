"""
Tests for the Perplexity service.
"""
import pytest
from unittest.mock import patch, MagicMock
from sdr_assistant.services.perplexity_service import PerplexityService

@pytest.fixture
def perplexity_service():
    """Fixture to create a PerplexityService instance for testing."""
    return PerplexityService()

def test_is_configured(perplexity_service, mock_env_variables):
    """Test that the service reports being correctly configured when API key exists."""
    assert perplexity_service.is_configured() == True

@patch('requests.post')
def test_generate_insights_success(mock_post, perplexity_service):
    """Test that generate_insights returns expected data on successful API call."""
    # Mock the API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [{'message': {'content': '## Industry Insights\nTest industry content\n## Company Information\nTest company content\n## Forward-Thinking Vision\nTest vision content'}}]
    }
    mock_post.return_value = mock_response
    
    # Test the method
    industry, company, vision = perplexity_service.generate_insights("Test Company")
    
    # Assert we get expected values
    assert "Industry Insights" in industry
    assert "Company Information" in company
    assert "Forward-Thinking Vision" in vision

@patch('requests.post')
def test_generate_insights_api_error(mock_post, perplexity_service):
    """Test that generate_insights returns fallback data when the API fails."""
    # Mock an API error
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Error"
    mock_post.return_value = mock_response
    
    # Test the method
    industry, company, vision = perplexity_service.generate_insights("Test Company")
    
    # Assert we get fallback data
    assert industry is not None
    assert company is not None
    assert vision is not None
    assert "Test Company" in industry
