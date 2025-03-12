"""
Core functionality for research generation and management.
Handles operations related to generating and storing research insights.
"""
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

from ..models.research import Research
from ..models.account import Account
from ..services.airtable_service import AirtableService
from ..services.perplexity_service import PerplexityService
from ..services.openai_service import OpenAIService
from ..core.accounts import account_manager


class ResearchManager:
    """Manager for research operations."""
    
    def __init__(self):
        """Initialize the research manager."""
        self.airtable_service = AirtableService()
        self.perplexity_service = PerplexityService()
        self.openai_service = OpenAIService()
    
    def generate_research(self, account_name: str) -> Dict[str, Any]:
        """
        Generate comprehensive research for an account.
        
        Args:
            account_name: Name of the account
            
        Returns:
            Dictionary containing research results
        """
        # Get account details
        account = account_manager.get_account_by_name(account_name)
        
        if not account:
            return {
                "success": False,
                "message": f"Account '{account_name}' not found"
            }
        
        # Generate insights using Perplexity API
        try:
            industry_insights, company_insights, vision_insights = self.perplexity_service.generate_insights(account_name)
            
            # Ensure we have data (fallback should already handle this, but just in case)
            if not industry_insights:
                industry_insights = f"### Industry Insights for {account_name}\nIndustry trends and competitive landscape information would appear here."
            
            if not company_insights:
                company_insights = f"### Company Information for {account_name}\nCompany background, products, and strategic initiatives would appear here."
                
            if not vision_insights:
                vision_insights = f"### Forward Thinking Vision for {account_name}\nFuture opportunities and strategic recommendations would appear here."   
        except Exception as e:
            print(f"Error in generate_insights: {str(e)}")
            # Use fallback data if API fails completely
            industry_insights = f"### Industry Insights for {account_name}\nIndustry trends and competitive landscape information would appear here."
            company_insights = f"### Company Information for {account_name}\nCompany background, products, and strategic initiatives would appear here."
            vision_insights = f"### Forward Thinking Vision for {account_name}\nFuture opportunities and strategic recommendations would appear here."
        
        # Generate talk track using OpenAI API
        insights = {
            "industry_insights": industry_insights,
            "company_insights": company_insights,
            "vision_insights": vision_insights
        }
        
        talk_track = self.openai_service.generate_talk_track(account_name, insights)
        
        if not talk_track:
            return {
                "success": False,
                "message": "Failed to generate talk track"
            }
        
        # Return the research results
        return {
            "success": True,
            "industryInsights": industry_insights,
            "companyInsights": company_insights,
            "visionInsights": vision_insights,
            "recommendedTalkTrack": talk_track
        }
    
    def save_research(self, research_data: Dict[str, Any], user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Save research data to Airtable.
        
        Args:
            research_data: Dictionary containing research data
            user_id: ID of the user saving the research
            
        Returns:
            Dictionary with success status and message
        """
        research = Research(
            account_id=research_data.get("accountId", ""),
            account_name=research_data.get("accountName", ""),
            industry_insights=research_data.get("industryInsights"),
            company_insights=research_data.get("companyInsights"),
            vision_insights=research_data.get("visionInsights"),
            recommended_talk_track=research_data.get("recommendedTalkTrack"),
            created_by=user_id
        )
        
        return self.airtable_service.save_research(research)


# Singleton instance for easy import
research_manager = ResearchManager()
