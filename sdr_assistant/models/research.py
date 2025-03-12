"""
Data model for research-related functionality.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Research:
    """Data model representing research for a company."""
    
    account_id: str
    account_name: str
    industry_insights: Optional[str] = None
    company_insights: Optional[str] = None
    vision_insights: Optional[str] = None
    recommended_talk_track: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    created_by: Optional[str] = None
    
    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def to_dict(self):
        """Convert research to a dictionary representation."""
        return {
            'account_id': self.account_id,
            'account_name': self.account_name,
            'industry_insights': self.industry_insights,
            'company_insights': self.company_insights,
            'vision_insights': self.vision_insights,
            'recommended_talk_track': self.recommended_talk_track,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }
    
    @classmethod
    def from_airtable(cls, airtable_record):
        """Create a Research instance from an Airtable record."""
        fields = airtable_record.get('fields', {})
        
        created_at = None
        if 'Created At' in fields:
            try:
                created_at = datetime.fromisoformat(fields['Created At'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
                
        updated_at = None
        if 'Updated At' in fields:
            try:
                updated_at = datetime.fromisoformat(fields['Updated At'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                pass
        
        return cls(
            account_id=fields.get('Account ID', ''),
            account_name=fields.get('Account Name', ''),
            industry_insights=fields.get('Industry Insights'),
            company_insights=fields.get('Company Insights'),
            vision_insights=fields.get('Vision Insights'),
            recommended_talk_track=fields.get('Recommended Talk Track'),
            created_at=created_at,
            updated_at=updated_at,
            created_by=fields.get('Created By')
        )
