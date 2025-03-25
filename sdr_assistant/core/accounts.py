"""
Core functionality for account management.
Handles operations related to retrieving and managing accounts.
"""
from typing import List, Dict, Any, Optional
import logging

from ..models.account import Account
from ..services.supabase_service import SupabaseService
from ..services.airtable_service import AirtableService
from ..config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

class AccountManager:
    """Manager for account operations."""
    
    def __init__(self):
        """Initialize the account manager."""
        # Primary data source is Supabase
        self.supabase_service = SupabaseService()
        
        # Keep Airtable as fallback for legacy support
        self.airtable_service = AirtableService()
        
        # Use Supabase if configured, otherwise fall back to Airtable
        self.use_supabase = settings.is_supabase_configured()
        if self.use_supabase:
            logger.info("Using Supabase as primary data source")
        else:
            logger.info("Supabase not configured, using Airtable as data source")
    
    def get_accounts(self) -> List[Account]:
        """
        Retrieve all accounts.
        
        Returns:
            List of Account objects
        """
        if self.use_supabase:
            return self.supabase_service.get_accounts()
        else:
            return self.airtable_service.get_accounts()
    
    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        """
        Retrieve an account by ID.
        
        Args:
            account_id: ID of the account
            
        Returns:
            Account object if found, None otherwise
        """
        accounts = self.get_accounts()
        for account in accounts:
            if account.id == account_id:
                return account
        return None
    
    def get_account_by_name(self, account_name: str) -> Optional[Account]:
        """
        Retrieve an account by name.
        
        Args:
            account_name: Name of the account
            
        Returns:
            Account object if found, None otherwise
        """
        accounts = self.get_accounts()
        for account in accounts:
            if account.name.lower() == account_name.lower():
                return account
        return None
        
    def get_account_details(self) -> List[Dict[str, Any]]:
        """
        Get detailed account information.
        
        Returns:
            List of account dictionaries with detailed information
        """
        accounts = self.get_accounts()
        return [account.to_dict() for account in accounts]
    
    def create_account(self, account_data: Dict[str, Any]) -> Optional[Account]:
        """
        Create a new account.
        
        Args:
            account_data: Dictionary with account properties
            
        Returns:
            New Account object if successful, None otherwise
        """
        if self.use_supabase:
            return self.supabase_service.create_account(account_data)
        else:
            logger.warning("Creating accounts not implemented for Airtable")
            return None
    
    def update_account(self, account_id: str, account_data: Dict[str, Any]) -> Optional[Account]:
        """
        Update an existing account.
        
        Args:
            account_id: ID of the account to update
            account_data: Dictionary with updated account properties
            
        Returns:
            Updated Account object if successful, None otherwise
        """
        if self.use_supabase:
            return self.supabase_service.update_account(account_id, account_data)
        else:
            logger.warning("Updating accounts not implemented for Airtable")
            return None
    
    def delete_account(self, account_id: str) -> bool:
        """
        Delete an account.
        
        Args:
            account_id: ID of the account to delete
            
        Returns:
            True if successful, False otherwise
        """
        if self.use_supabase:
            return self.supabase_service.delete_account(account_id)
        else:
            logger.warning("Deleting accounts not implemented for Airtable")
            return False


# Singleton instance for easy import
account_manager = AccountManager()
