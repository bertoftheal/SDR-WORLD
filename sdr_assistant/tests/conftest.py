"""
Pytest configuration file for SDR Assistant tests.
Contains fixtures and setup code for testing.
"""
import pytest
import os
import sys
import json
from typing import Dict, Any

# Add the parent directory to the path so we can import from the sdr_assistant package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_env_variables(monkeypatch):
    """Fixture to set up mock environment variables for testing."""
    monkeypatch.setenv("AIRTABLE_API_KEY", "mock_airtable_key")
    monkeypatch.setenv("AIRTABLE_BASE_ID", "mock_base_id")
    monkeypatch.setenv("OPENAI_API_KEY", "mock_openai_key")
    monkeypatch.setenv("PERPLEXITY_API_KEY", "mock_perplexity_key")
    monkeypatch.setenv("JWT_SECRET_KEY", "mock_jwt_secret")

@pytest.fixture
def sample_account_data() -> Dict[str, Any]:
    """Fixture to provide sample account data for testing."""
    return {
        "id": "sample_account_id",
        "name": "Sample Company",
        "industry": "Technology",
        "website": "https://sample-company.example.com",
        "employees": 500,
        "description": "A sample company for testing purposes"
    }

@pytest.fixture
def sample_research_data() -> Dict[str, Any]:
    """Fixture to provide sample research data for testing."""
    return {
        "account_id": "sample_account_id",
        "account_name": "Sample Company",
        "industry_insights": "### Industry Insights\nSample industry analysis.",
        "company_insights": "### Company Information\nSample company information.",
        "vision_insights": "### Forward Thinking Vision\nSample vision analysis.",
        "talk_track": "# Personalized Talk Track\nSample talk track content."
    }
