"""
Core functionality for research generation and management.
Handles operations related to generating and storing research insights.
"""
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
import logging

from ..models.research import Research
from ..models.account import Account
from ..services.supabase_service import SupabaseService
from ..services.airtable_service import AirtableService
from ..services.perplexity_service import PerplexityService
from ..services.openai_service import OpenAIService
from ..core.accounts import account_manager
from ..config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class ResearchManager:
    """Manager for research operations."""
    
    def __init__(self):
        """Initialize the research manager."""
        # Primary data source is Supabase
        self.supabase_service = SupabaseService()
        
        # Keep Airtable as fallback for legacy support
        self.airtable_service = AirtableService()
        
        # AI services
        self.perplexity_service = PerplexityService()
        self.openai_service = OpenAIService()
        
        # Use Supabase if configured, otherwise fall back to Airtable
        self.use_supabase = settings.is_supabase_configured()
        if self.use_supabase:
            logger.info("Research Manager using Supabase as primary data source")
        else:
            logger.info("Research Manager using Airtable as data source")
    
    def generate_research(self, account_name: str) -> Dict[str, Any]:
        """
        Generate comprehensive research for an account.
        
        Args:
            account_name: Name of the account
            
        Returns:
            Dictionary containing research results
        """
        # Get account details if in database, but don't require it
        account = account_manager.get_account_by_name(account_name)
        
        # Log what we're doing
        logger.info(f"Generating research for: {account_name}")
        if account:
            logger.info(f"Found account in database")
        else:
            logger.info(f"Account not found in database, will generate research directly")
        
        # Generate insights using Perplexity API - force a fresh generation every time
        try:
            logger.info(f"Generating fresh research insights for {account_name} using Perplexity API")
            industry_insights, company_insights, vision_insights = self.perplexity_service.generate_insights(account_name)
            
            # Log whether we got real data
            if industry_insights and company_insights and vision_insights:
                logger.info(f"✅ Successfully generated all research sections for {account_name}")
            else:
                logger.warning(f"⚠️ Some research sections were missing for {account_name}")
            
            # Ensure we have data (fallback should already handle this, but just in case)
            if not industry_insights:
                logger.warning(f"⚠️ No industry insights generated, using fallback for {account_name}")
                industry_insights = f"### Industry Insights for {account_name}\nIndustry trends and competitive landscape information would appear here."
            
            if not company_insights:
                logger.warning(f"⚠️ No company insights generated, using fallback for {account_name}")
                company_insights = f"### Company Information for {account_name}\nCompany background, products, and strategic initiatives would appear here."
                
            if not vision_insights:
                logger.warning(f"⚠️ No vision insights generated, using fallback for {account_name}")
                vision_insights = f"### Forward Thinking Vision for {account_name}\nFuture opportunities and strategic recommendations would appear here."   
        except Exception as e:
            logger.error(f"❌ Error in generate_insights: {str(e)}")
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
        Save research data to the database.
        
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
        
        # Save to Supabase if configured, otherwise fall back to Airtable
        if self.use_supabase:
            logger.info(f"Saving research for {research.account_name} to Supabase")
            return self.supabase_service.save_research(research)
        else:
            logger.info(f"Saving research for {research.account_name} to Airtable")
            return self.airtable_service.save_research(research)


# Singleton instance for easy import
research_manager = ResearchManager()
