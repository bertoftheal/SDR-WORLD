"""
Service for interacting with the Airtable API.
Handles operations related to accounts and research data storage.
"""
from pyairtable import Table
from typing import List, Dict, Any, Optional
import json

from ..config.settings import settings
from ..models.account import Account
from ..models.research import Research


class AirtableService:
    """Service for Airtable API interactions."""
    
    def __init__(self):
        """Initialize the Airtable service."""
        self.api_key = settings.AIRTABLE_API_KEY
        self.base_id = settings.AIRTABLE_BASE_ID
        self.table_name = settings.AIRTABLE_TABLE_NAME
        self.is_configured = settings.is_airtable_configured()
    
    def get_accounts(self) -> List[Account]:
        """Retrieve accounts from Airtable."""
        if not self.is_configured:
            return Account.create_mock_accounts()
        
        try:
            table = Table(self.api_key, self.base_id, self.table_name)
            records = table.all()
            
            return [Account.from_airtable(record) for record in records]
        except Exception as e:
            print(f"Error fetching accounts from Airtable: {str(e)}")
            return Account.create_mock_accounts()
    
    def save_research(self, research: Research) -> Dict[str, Any]:
        """Save research to Airtable."""
        if not self.is_configured:
            return {
                "success": False,
                "message": "Airtable is not configured. Research data would be saved here."
            }
        
        try:
            # Create a table instance for research data
            research_table = Table(self.api_key, self.base_id, 'Research')
            
            # Check if research already exists for this account
            existing_records = research_table.all(formula=f"{{Account ID}}='{research.account_id}'")
            
            if existing_records:
                # Update existing record
                record_id = existing_records[0]['id']
                research.updated_at = None  # Force update of timestamp in __post_init__
                
                data = {
                    'Account ID': research.account_id,
                    'Account Name': research.account_name,
                    'Industry Insights': research.industry_insights,
                    'Company Insights': research.company_insights,
                    'Vision Insights': research.vision_insights,
                    'Recommended Talk Track': research.recommended_talk_track,
                    'Updated At': research.updated_at.isoformat()
                }
                
                research_table.update(record_id, data)
                return {"success": True, "message": "Research updated successfully"}
            else:
                # Create new record
                data = {
                    'Account ID': research.account_id,
                    'Account Name': research.account_name,
                    'Industry Insights': research.industry_insights,
                    'Company Insights': research.company_insights,
                    'Vision Insights': research.vision_insights,
                    'Recommended Talk Track': research.recommended_talk_track,
                    'Created At': research.created_at.isoformat(),
                    'Updated At': research.updated_at.isoformat()
                }
                
                if research.created_by:
                    data['Created By'] = research.created_by
                
                research_table.create(data)
                return {"success": True, "message": "Research saved successfully"}
                
        except Exception as e:
            print(f"Error saving research to Airtable: {str(e)}")
            return {"success": False, "message": f"Error: {str(e)}"}
