"""
Core functionality for account management.
Handles operations related to retrieving and managing accounts.
"""
from typing import List, Dict, Any, Optional

from ..models.account import Account
from ..services.airtable_service import AirtableService


class AccountManager:
    """Manager for account operations."""
    
    def __init__(self):
        """Initialize the account manager."""
        self.airtable_service = AirtableService()
    
    def get_accounts(self) -> List[Account]:
        """
        Retrieve all accounts.
        
        Returns:
            List of Account objects
        """
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


# Singleton instance for easy import
account_manager = AccountManager()
