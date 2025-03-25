"""
Data model for account-related functionality.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class Account:
    """Data model representing an account/company."""
    
    id: str
    name: str
    industry: Optional[str] = None
    location: Optional[str] = None
    employees: Optional[int] = None
    revenue: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contacts: List[Dict[str, Any]] = field(default_factory=list)
    
    @classmethod
    def from_airtable(cls, airtable_record):
        """Create an Account instance from an Airtable record."""
        fields = airtable_record.get('fields', {})
        
        return cls(
            id=airtable_record.get('id', ''),
            name=fields.get('Name', ''),
            industry=fields.get('Industry'),
            location=fields.get('HQ Location'),
            employees=fields.get('Employee Count'),
            revenue=fields.get('Revenue'),
            website=fields.get('Website'),
            description=fields.get('Description')
        )
        
    @classmethod
    def from_supabase(cls, supabase_record):
        """Create an Account instance from a Supabase record."""
        return cls(
            id=supabase_record.get('id', ''),
            name=supabase_record.get('name', ''),
            industry=supabase_record.get('industry'),
            location=supabase_record.get('location') or supabase_record.get('headquarters'),
            employees=supabase_record.get('employee_count') or supabase_record.get('employees'),
            revenue=supabase_record.get('revenue'),
            website=supabase_record.get('website'),
            description=supabase_record.get('description')
        )
    
    @classmethod
    def create_mock_accounts(cls):
        """Create a list of mock account objects for demonstration purposes."""
        return [
            cls(id="mock1", name="Acme Corporation", industry="Technology", 
                location="San Francisco, CA", employees=500, 
                website="https://acme.example.com"),
            cls(id="mock2", name="TechGiant Inc", industry="Software", 
                location="Seattle, WA", employees=10000, 
                website="https://techgiant.example.com"),
            cls(id="mock3", name="Global Financial", industry="Finance", 
                location="New York, NY", employees=2500, 
                website="https://globalfinancial.example.com"),
            cls(id="mock4", name="Healthcare Systems", industry="Healthcare", 
                location="Boston, MA", employees=1200, 
                website="https://healthcare.example.com"),
            cls(id="mock5", name="Retail Stores", industry="Retail", 
                location="Chicago, IL", employees=3000, 
                website="https://retailstores.example.com")
        ]

    def to_dict(self):
        """Convert the account to a dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'industry': self.industry,
            'location': self.location,
            'employees': self.employees,
            'revenue': self.revenue,
            'website': self.website,
            'description': self.description,
            'contacts': self.contacts
        }
