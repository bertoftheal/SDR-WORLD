"""
Supabase Service for SDR World

This service handles all interactions with Supabase database,
providing a consistent data layer for accounts and research data.
"""

from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from supabase import create_client, Client

from ..config.settings import settings
from ..models.account import Account
from ..models.research import Research

class SupabaseService:
    """
    Service class for handling all Supabase interactions
    """
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance is created"""
        if cls._instance is None:
            cls._instance = super(SupabaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the Supabase client"""
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.is_configured = settings.is_supabase_configured()
        
        if self.is_configured:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                self.initialized = True
                print("Supabase client initialized successfully")
            except Exception as e:
                print(f"Error initializing Supabase client: {e}")
                self.initialized = False
                self._init_mock_data()
        else:
            print("Supabase not configured, using mock data")
            self.initialized = False
            self._init_mock_data()
    
    def _init_mock_data(self):
        """Initialize mock data for demo mode"""
        self.mock_accounts = [
            {
                "id": "1",
                "name": "NVIDIA",
                "logo_url": "https://logo.clearbit.com/nvidia.com",
                "industry": "Technology",
                "description": "NVIDIA is a technology company known for designing graphics processing units (GPUs) for gaming and professional markets, as well as system on a chip units for mobile computing and automotive markets.",
                "headquarters": "Santa Clara, CA",
                "status": "Researched",
                "updated_at": "Mar 9, 2025",
                "research_status": "Active Research",
                "employees": "26,000+",
                "market_cap": "$2.3 Trillion",
                "founded": "1993"
            },
            {
                "id": "2",
                "name": "Google",
                "logo_url": "https://logo.clearbit.com/google.com",
                "industry": "Technology",
                "description": "Google LLC is an American multinational technology company that specializes in Internet-related services and products.",
                "headquarters": "Mountain View, CA",
                "status": "Researched",
                "updated_at": "Mar 4, 2025"
            },
            {
                "id": "3",
                "name": "Microsoft",
                "logo_url": "https://logo.clearbit.com/microsoft.com",
                "industry": "Technology",
                "description": "Microsoft Corporation is an American multinational technology company that develops, licenses, and supports software, services, devices, and solutions.",
                "headquarters": "Redmond, WA",
                "status": "Researched",
                "updated_at": "Feb 28, 2025"
            },
            {
                "id": "4",
                "name": "Amazon",
                "logo_url": "https://logo.clearbit.com/amazon.com",
                "industry": "Retail",
                "description": "Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.",
                "headquarters": "Seattle, WA",
                "status": "Pending",
                "updated_at": "Mar 1, 2025"
            },
            {
                "id": "5",
                "name": "JP Morgan Chase",
                "logo_url": "https://logo.clearbit.com/jpmorganchase.com",
                "industry": "Finance",
                "description": "JPMorgan Chase & Co. is an American multinational investment bank and financial services holding company.",
                "headquarters": "New York, NY",
                "status": "Pending",
                "updated_at": "Mar 2, 2025"
            }
        ]
        
        self.mock_research = [
            {
                "id": "1",
                "account_id": "1",
                "company_name": "NVIDIA Corporation",
                "overview": "NVIDIA is a global technology company and inventor of the GPU...",
                "insights": [
                    "Recently acquired ARM Holdings for $40 billion to strengthen its AI capabilities",
                    "Growing demand in data center and AI sectors",
                    "Facing increased competition from AMD and Intel in the GPU market"
                ],
                "talk_tracks": [
                    "Your AI compute needs are growing rapidly - NVIDIA's latest data center GPUs could accelerate your ML initiatives by 40%",
                    "Your competitors are implementing AI-powered analytics - NVIDIA's enterprise solutions can help you maintain competitive edge"
                ],
                "created_at": "Mar 9, 2025"
            }
        ]
    
    def get_accounts(self) -> List[Account]:
        """Retrieve accounts from Supabase."""
        if not self.initialized:
            return Account.create_mock_accounts()
        
        try:
            response = self.client.from_('accounts').select('*').execute()
            if response.data:
                return [Account.from_supabase(record) for record in response.data]
            return Account.create_mock_accounts()
        except Exception as e:
            print(f"Error fetching accounts from Supabase: {str(e)}")
            return Account.create_mock_accounts()
    
    def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific account by ID"""
        if self.initialized:
            response = self.client.from_('accounts').select('*').eq('id', account_id).execute()
            if response.data:
                return response.data[0]
            return None
        
        # Find account in mock data
        for account in self.mock_accounts:
            if account['id'] == account_id:
                return account
        return None
    
    def get_account_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific account by name"""
        if self.initialized:
            response = self.client.from_('accounts').select('*').eq('name', name).execute()
            if response.data:
                return response.data[0]
            return None
        
        # Find account in mock data
        for account in self.mock_accounts:
            if account['name'] == name:
                return account
        return None
    
    def create_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new account"""
        if self.initialized:
            response = self.client.from_('accounts').insert(account_data).execute()
            return response.data[0] if response.data else None
        
        # Create account in mock data
        new_id = str(len(self.mock_accounts) + 1)
        account_data['id'] = new_id
        self.mock_accounts.append(account_data)
        return account_data
    
    def update_account(self, account_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing account"""
        if self.initialized:
            response = self.client.from_('accounts').update(account_data).eq('id', account_id).execute()
            return response.data[0] if response.data else None
        
        # Update account in mock data
        for i, account in enumerate(self.mock_accounts):
            if account['id'] == account_id:
                self.mock_accounts[i].update(account_data)
                return self.mock_accounts[i]
        return None
    
    def get_research(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get research for a specific account"""
        if self.initialized:
            response = self.client.from_('research').select('*').eq('account_id', account_id).execute()
            if response.data:
                return response.data[0]
            return None
        
        # Find research in mock data
        for research in self.mock_research:
            if research['account_id'] == account_id:
                return research
        return None
    
    def save_research(self, research: Research) -> Dict[str, Any]:
        """Save research to Supabase."""
        if not self.initialized:
            return {
                "success": False,
                "message": "Supabase is not configured. Research data would be saved here."
            }
        
        try:
            # Prepare data for Supabase
            research_data = {
                "account_id": research.account_id,
                "account_name": research.account_name,
                "industry_insights": research.industry_insights,
                "company_insights": research.company_insights,
                "vision_insights": research.vision_insights,
                "talk_track": research.talk_track,
                "created_by": research.created_by,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Check if research already exists for this account
            existing = self.client.from_('research').select('*').eq('account_id', research.account_id).execute()
            
            if existing.data:
                # Update existing research
                response = self.client.from_('research').update(research_data).eq('account_id', research.account_id).execute()
                return {
                    "success": True,
                    "message": "Research updated successfully",
                    "data": response.data[0] if response.data else None
                }
            else:
                # Create new research entry
                response = self.client.from_('research').insert(research_data).execute()
                return {
                    "success": True,
                    "message": "Research created successfully",
                    "data": response.data[0] if response.data else None
                }
                
        except Exception as e:
            print(f"Error saving research to Supabase: {str(e)}")
            return {
                "success": False,
                "message": f"Error saving research: {str(e)}"
            }
            
    def create_research(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new research (mock implementation)"""
        if self.initialized:
            response = self.client.from_('research').insert(research_data).execute()
            return response.data[0] if response.data else None
        
        # Create research in mock data
        new_id = str(len(self.mock_research) + 1)
        research_data['id'] = new_id
        self.mock_research.append(research_data)
        return research_data
    
    def update_research(self, research_id: str, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing research"""
        if self.initialized:
            response = self.client.from_('research').update(research_data).eq('id', research_id).execute()
            return response.data[0] if response.data else None
        
        # Update research in mock data
        for i, research in enumerate(self.mock_research):
            if research['id'] == research_id:
                self.mock_research[i].update(research_data)
                return self.mock_research[i]
        return None
    
    def export_data_to_json(self, filepath: str = "data/sdr_world_data.json"):
        """Export all data to a JSON file"""
        data = {
            "accounts": self.mock_accounts if not self.initialized else self.get_accounts(),
            "research": self.mock_research if not self.initialized else self.client.from_('research').select('*').execute().data
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def import_data_from_json(self, filepath: str = "data/sdr_world_data.json"):
        """Import data from a JSON file"""
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not self.initialized:
            self.mock_accounts = data.get('accounts', [])
            self.mock_research = data.get('research', [])
            return True
        
        # Clear existing data
        self.client.from_('accounts').delete().execute()
        self.client.from_('research').delete().execute()
        
        # Insert new data
        if data.get('accounts'):
            self.client.from_('accounts').insert(data['accounts']).execute()
        if data.get('research'):
            self.client.from_('research').insert(data['research']).execute()
        
        return True
