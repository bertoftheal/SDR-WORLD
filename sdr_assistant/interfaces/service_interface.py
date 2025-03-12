"""
Base interfaces for service classes in the SDR Assistant application.
These interfaces define the contract that service implementations must fulfill.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List

class ServiceInterface(ABC):
    """Base interface for all service classes."""
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if the service is properly configured."""
        pass

class AirtableServiceInterface(ServiceInterface):
    """Interface for Airtable service implementations."""
    
    @abstractmethod
    def get_accounts(self) -> List[Dict[str, Any]]:
        """
        Get all accounts from Airtable.
        
        Returns:
            List of account dictionaries
        """
        pass
    
    @abstractmethod
    def get_account_by_id(self, account_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an account by its ID.
        
        Args:
            account_id: ID of the account to retrieve
            
        Returns:
            Account dictionary if found, None otherwise
        """
        pass
    
    @abstractmethod
    def save_research(self, research_data: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Save research data to Airtable.
        
        Args:
            research_data: Research data to save
            user_id: Optional ID of the user saving the research
            
        Returns:
            Dictionary with success status and message
        """
        pass

class OpenAIServiceInterface(ServiceInterface):
    """Interface for OpenAI service implementations."""
    
    @abstractmethod
    def generate_talk_track(self, account_name: str, insights: Dict[str, str]) -> Optional[str]:
        """
        Generate a sales talk track for an account using the OpenAI API.
        
        Args:
            account_name: Name of the account
            insights: Dictionary containing research insights
            
        Returns:
            Generated talk track, or None if generation fails
        """
        pass

class PerplexityServiceInterface(ServiceInterface):
    """Interface for Perplexity service implementations."""
    
    @abstractmethod
    def generate_insights(self, account_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Generate insights about a company using the Perplexity API.
        
        Args:
            account_name: Name of the account/company
            
        Returns:
            Tuple of (industry_insights, company_insights, vision_insights)
        """
        pass
