"""
Service for interacting with the Perplexity API.
Handles operations related to generating insights about companies and industries.
"""
import requests
import json
from typing import Dict, Any, Optional, List, Tuple

from ..config.settings import settings


class PerplexityService:
    """Service for Perplexity API interactions."""
    
    def __init__(self):
        """Initialize the Perplexity service."""
        self.api_key = settings.PERPLEXITY_API_KEY
    
    def generate_insights(self, account_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Generate insights about a company using the Perplexity API.
        If API fails, returns placeholder data for demonstration purposes.
        
        Args:
            account_name: Name of the account/company
            
        Returns:
            Tuple of (industry_insights, company_insights, vision_insights)
        """
        if not self.api_key:
            print("Perplexity API key not configured")
            return self._get_placeholder_insights(account_name)
        
        try:
            # Make a single API call to get all insights for better performance
            all_insights = self._get_combined_insights(account_name)
            
            if not all_insights:
                return self._get_placeholder_insights(account_name)
                
            return all_insights
        except Exception as e:
            print(f"Error generating insights via API: {str(e)}")
            return self._get_placeholder_insights(account_name)
            
    def _get_combined_insights(self, account_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Generate all insights for the account in a single API call for better performance."""
        prompt = f"""Provide comprehensive research on {account_name} divided into exactly three separate sections. 
        Format each section with a Markdown header.
        
        SECTION 1 - INDUSTRY INSIGHTS:
        Analyze the industry in which {account_name} operates:
        1. Recent industry trends and developments
        2. Competitive landscape and market dynamics
        3. Regulatory factors or challenges affecting the industry
        
        SECTION 2 - COMPANY INFORMATION:
        Specific information about {account_name}:
        1. Core products, services, and business model
        2. Recent company news, initiatives, or strategic shifts
        3. Key challenges and pain points they might be experiencing
        
        SECTION 3 - FORWARD-THINKING VISION:
        Strategic recommendations for {account_name}:
        1. Potential growth opportunities based on market trends
        2. Technology adoption that could provide competitive advantages
        3. How AI coding assistants could benefit their development processes
        4. Future challenges they might face without modernizing their development tools
        
        Format your response with three clearly labeled sections with markdown headers. Keep each section concise but informative.
        """
        
        response = self._make_perplexity_request(prompt)
        
        if not response:
            return None, None, None
            
        # Split the response into three sections
        try:
            # Look for markdown headers to split the content
            sections = []
            current_section = ""
            lines = response.split('\n')
            
            for line in lines:
                if line.startswith("## ") or line.startswith("### "):
                    if current_section:
                        sections.append(current_section.strip())
                        current_section = ""
                current_section += line + "\n"
                
            if current_section:
                sections.append(current_section.strip())
                
            # Ensure we have exactly three sections
            if len(sections) == 3:
                return tuple(sections)
            elif len(sections) > 3:
                # Take the first three sections
                return tuple(sections[:3])
            else:
                # If we couldn't properly split, use the response as industry insights and provide placeholders for others
                placeholder = self._get_placeholder_insights(account_name)
                return response, placeholder[1], placeholder[2]
                
        except Exception as e:
            print(f"Error splitting insights: {str(e)}")
            return None, None, None
    
    def _get_industry_insights(self, account_name: str) -> Optional[str]:
        """Generate industry insights for the account."""
        prompt = f"""I need to prepare for a sales call with {account_name}. 
        Give me a detailed analysis of their industry, including:
        1. Key market trends and challenges in their industry
        2. Common technical challenges companies in this space face
        3. How AI and developer tools are typically utilized in this industry
        4. Regulatory or compliance considerations specific to their sector
        
        Focus only on the industry insights, not on {account_name} specifically.
        Provide comprehensive insights I can use to show industry expertise.
        Include specific metrics and trends where possible.
        """
        
        return self._make_perplexity_request(prompt)
    
    def _get_company_insights(self, account_name: str) -> Optional[str]:
        """Generate company-specific insights for the account."""
        prompt = f"""I need detailed information about {account_name} for a sales call.
        Provide me with:
        1. Their main products/services and target customers
        2. Recent company announcements, initiatives, or strategic shifts
        3. Their technology stack and development practices (if known)
        4. Key business challenges they're likely facing
        5. Their competitive positioning in the market
        
        Focus specifically on {account_name}, not general industry information.
        Include factual information that would be valuable for a sales conversation.
        """
        
        return self._make_perplexity_request(prompt)
    
    def _get_vision_insights(self, account_name: str) -> Optional[str]:
        """Generate forward-thinking vision insights for the account."""
        prompt = f"""Based on current trends and {account_name}'s position, give me a forward-thinking analysis of:
        1. How AI and advanced developer tools could transform their business operations
        2. Potential opportunities for innovation in their development processes
        3. How they could gain competitive advantage through improved coding efficiency
        4. Future challenges they might face without modernizing their development tools
        
        Be specific to {account_name}'s situation and provide insights that demonstrate thought leadership.
        Focus on the transformative potential of AI coding assistants for their business.
        """
        
        return self._make_perplexity_request(prompt)
    
    def _make_perplexity_request(self, prompt: str) -> Optional[str]:
        """Make a request to the Perplexity API."""
        if not self.api_key:
            print("⚠️ WARNING: Perplexity API key is not configured or is empty")
            return None
            
        if self.api_key == "your_perplexity_api_key_here" or self.api_key == "placeholder_key":
            print("⚠️ WARNING: Using placeholder Perplexity API key. Please update with a real key.")
            return None
            
        print(f"📤 Making Perplexity API request with prompt: {prompt[:50]}...")
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a helpful research assistant that provides accurate, concise, and well-structured information."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            print(f"📡 Connecting to Perplexity API...")
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                insight_text = response_data['choices'][0]['message']['content']
                print(f"✅ Perplexity API request successful: received {len(insight_text)} characters")
                return insight_text
            else:
                print(f"❌ Perplexity API Error: Status {response.status_code}")
                print(f"Error details: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: Could not connect to Perplexity API: {str(e)}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout Error: Perplexity API request timed out: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error making Perplexity API request: {str(e)}")
            return None
            
    def _get_placeholder_insights(self, account_name: str) -> Tuple[str, str, str]:
        """Generate placeholder insights when API calls fail."""
        industry_insights = f"""### Industry Trends for {account_name}
1. The industry is experiencing rapid digital transformation with companies investing in cloud technology.
2. There's a growing demand for AI and machine learning solutions to improve operational efficiency.
3. Cybersecurity remains a top priority as threats become more sophisticated.

### Technical Challenges
1. Legacy system integration with modern cloud infrastructure
2. Scaling development teams to meet growing technology demands
3. Maintaining security compliance across distributed systems

### AI Utilization
1. Developer productivity tools are becoming essential for competitive advantage
2. Code generation and analysis tools are reducing development time by 30-40%
3. AI pair programming assistants are being adopted by forward-thinking companies"""

        company_insights = f"""### About {account_name}
1. {account_name} is a recognized leader in their market segment
2. They've recently announced initiatives to modernize their tech stack
3. Their development teams are working on several high-priority projects

### Technology Stack
1. Uses a mix of legacy and modern systems
2. Development primarily happens in multiple languages including Java, Python, and JavaScript
3. Moving toward containerized microservices architecture

### Business Challenges
1. Growing technical debt affecting development velocity
2. Need to accelerate innovation while maintaining quality
3. Competition from nimble startups with modern tech stacks"""

        vision_insights = f"""### AI Transformation Opportunities
1. {account_name} could leverage AI coding assistants to reduce technical debt by 25%
2. Implementing automated code reviews could improve quality while reducing manual effort
3. Standardizing on AI development tools could create consistency across teams

### Innovation Potential
1. Reducing time-to-market for new features by 30-40%
2. Improving developer retention by eliminating repetitive coding tasks
3. Creating a more collaborative development environment across global teams

### Competitive Advantages
1. Early adoption of AI development tools could position {account_name} as an industry innovator
2. Improved code quality and standardization would reduce production issues
3. Developer satisfaction and productivity gains would translate to business results"""

        return industry_insights, company_insights, vision_insights
