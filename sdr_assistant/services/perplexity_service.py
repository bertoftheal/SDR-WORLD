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
        # Use the API key from settings if available, otherwise use a demo mode
        self.api_key = settings.PERPLEXITY_API_KEY
        # Demo mode flag
        self.demo_mode = True if not self.api_key else False
    
    def generate_insights(self, account_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Generate insights about a company using the Perplexity API.
        If API fails, returns explicit error message instead of placeholder data.
        
        Args:
            account_name: Name of the account/company
            
        Returns:
            Tuple of (industry_insights, company_insights, vision_insights)
        """
        if not self.api_key:
            print("Perplexity API key not configured")
            return self._get_perplexity_error_message()
        
        try:
            # Make a single API call to get all insights for better performance
            all_insights = self._get_combined_insights(account_name)
            
            if not all_insights:
                return self._get_perplexity_error_message()
                
            return all_insights
        except Exception as e:
            print(f"Error generating insights via API: {str(e)}")
            return self._get_perplexity_error_message()
            
    def _get_combined_insights(self, account_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Generate all insights for the account in a single API call for better performance."""
        # Simplified prompt as requested - just ask for a two sentence overview
        prompt = f"Provide a two sentence overview of {account_name}"
        
        response = self._make_perplexity_request(prompt)
        
        if not response:
            return None, None, None
            
        # Since we're using a simple overview prompt, we need to adapt the response
        # to fit the expected three-section structure for compatibility
        try:
            # Get the clean overview text
            overview = response.strip()
            
            # Create three sections with the same overview content to maintain
            # compatibility with the rest of the application
            industry_insights = f"### Industry Context\n{overview}"
            company_insights = f"### Company Overview\n{overview}"
            vision_insights = f"### Strategic Direction\n{overview}"
            
            return industry_insights, company_insights, vision_insights
                
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
            
        print(f"📤 Making Perplexity API request for prompt: {prompt[:100]}...")
        print(f"📤 Using API key: {self.api_key[:5]}...{self.api_key[-5:]}")
        
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
            
    def _get_realistic_starbucks_insights(self) -> Tuple[str, str, str]:
        """Return realistic insights for Starbucks."""
        industry_insights = "### Coffee and Fast-Food Industry\nThe coffee shop industry is highly competitive with significant growth in specialty coffee and digital ordering. Consumer preferences are shifting toward sustainability and ethically sourced products, with increasing demand for plant-based alternatives and innovative flavor profiles."
        
        company_insights = "### Company Overview\nStarbucks Corporation is a multinational chain of coffeehouses and roastery reserves headquartered in Seattle, Washington. It is the world's largest coffeehouse chain, operating over 35,000 stores in 80 countries, known for its high-quality coffee, distinctive store experience, and strong brand loyalty."
        
        vision_insights = "### Strategic Direction\nStarbucks is focusing on digital transformation through its mobile app and rewards program, expanding in international markets especially China, and enhancing sustainability initiatives including waste reduction and ethical sourcing commitments."
        
        return industry_insights, company_insights, vision_insights
    
    def _get_realistic_microsoft_insights(self) -> Tuple[str, str, str]:
        """Return realistic insights for Microsoft."""
        industry_insights = "### Technology Industry\nThe technology sector continues to be driven by cloud computing, artificial intelligence, and digital transformation. Enterprise software companies are focusing on subscription-based models, with increasing emphasis on security, compliance, and scalable infrastructure solutions."
        
        company_insights = "### Company Overview\nMicrosoft Corporation is a multinational technology company headquartered in Redmond, Washington. As one of the world's largest software makers, Microsoft develops, manufactures, licenses, and sells computer software, consumer electronics, personal computers, and related services including cloud platforms, productivity tools, and enterprise solutions."
        
        vision_insights = "### Strategic Direction\nMicrosoft is heavily investing in its Azure cloud platform, AI capabilities, and collaborative tools like Microsoft 365. The company is pursuing a cross-platform strategy while advancing quantum computing research and expanding its gaming division through strategic acquisitions."
        
        return industry_insights, company_insights, vision_insights
    
    def _get_realistic_apple_insights(self) -> Tuple[str, str, str]:
        """Return realistic insights for Apple."""
        industry_insights = "### Consumer Electronics Industry\nThe consumer electronics industry is characterized by rapid innovation cycles and increasing integration of AI features into devices. Companies are competing on ecosystem development, with services becoming a critical revenue stream alongside hardware sales."
        
        company_insights = "### Company Overview\nApple Inc. is a multinational technology company headquartered in Cupertino, California, that designs, develops, and sells consumer electronics, computer software, and online services. Known for its premium products including iPhone, iPad, Mac computers, Apple Watch, and AirPods, Apple maintains a closed ecosystem with tight integration between hardware and software."
        
        vision_insights = "### Strategic Direction\nApple is expanding its services segment including Apple TV+, Apple Music, and Apple Pay, while developing new technologies in augmented reality and autonomous systems. The company continues its focus on privacy as a competitive advantage and is transitioning its Mac line to custom Apple Silicon processors."
        
        return industry_insights, company_insights, vision_insights
      
    def _get_realistic_google_insights(self) -> Tuple[str, str, str]:
        """Return realistic insights for Google/Alphabet."""
        industry_insights = "### Technology and Digital Advertising Industry\nThe digital advertising ecosystem is evolving with privacy regulations challenging traditional tracking methods. Search and discovery platforms are incorporating more AI-driven features while diversifying revenue streams beyond advertising."
        
        company_insights = "### Company Overview\nGoogle (Alphabet Inc.) is a multinational technology company specializing in Internet-related services and products, including online advertising technologies, a search engine, cloud computing, software, and hardware. As the world's most popular search engine, Google processes billions of search queries daily and offers products ranging from Android OS to YouTube to Google Cloud."
        
        vision_insights = "### Strategic Direction\nGoogle is heavily investing in artificial intelligence research, expanding its cloud computing business, and developing advanced hardware including Pixel devices. The company is navigating privacy challenges while exploring new frontiers in quantum computing and life sciences through various Alphabet subsidiaries."
        
        return industry_insights, company_insights, vision_insights
    
    def _get_realistic_amazon_insights(self) -> Tuple[str, str, str]:
        """Return realistic insights for Amazon."""
        industry_insights = "### E-commerce and Cloud Computing Industry\nThe e-commerce sector continues to grow with emphasis on logistics optimization and last-mile delivery innovation. Companies are leveraging data analytics for personalization while cloud services represent a high-margin growth avenue for technology leaders."
        
        company_insights = "### Company Overview\nAmazon.com Inc. is a multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence. Founded by Jeff Bezos, Amazon has expanded far beyond its original focus as an online bookstore to become the world's largest online marketplace, AI assistant provider, and cloud computing platform."
        
        vision_insights = "### Strategic Direction\nAmazon is strengthening its AWS cloud platform, expanding physical retail presence through Amazon Fresh and Whole Foods, and growing its advertising business. The company continues investing in logistics infrastructure while developing new consumer devices and entertainment content through Amazon Studios."
        
        return industry_insights, company_insights, vision_insights
    
    def _get_realistic_netflix_insights(self) -> Tuple[str, str, str]:
        """Return realistic insights for Netflix."""
        industry_insights = "### Streaming Media Industry\nThe streaming entertainment market is increasingly competitive with multiple major players vying for subscriber growth. Content production costs continue to rise while regional content has become critical for international expansion and audience retention."
        
        company_insights = "### Company Overview\nNetflix, Inc. is a subscription streaming service and production company headquartered in Los Gatos, California. With over 200 million paid subscribers worldwide, Netflix offers a vast library of films, television series, documentaries, and mobile games through its distribution platform."
        
        vision_insights = "### Strategic Direction\nNetflix is expanding its original content production globally, experimenting with interactive and gaming content, and implementing measures to prevent password sharing. The company is adapting its content strategy to regional preferences while exploring ad-supported tiers to drive growth in maturing markets."
        
        return industry_insights, company_insights, vision_insights
        
    def _get_perplexity_error_message(self) -> Tuple[str, str, str]:
        """Return an explicit error message when Perplexity API cannot be used."""
        error_message = "Perplexity can't run"
        
        # Return the same error message for all three sections
        industry_insights = f"### Industry Context\n{error_message}"
        company_insights = f"### Company Overview\n{error_message}"
        vision_insights = f"### Strategic Direction\n{error_message}"
        
        return industry_insights, company_insights, vision_insights
        
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
