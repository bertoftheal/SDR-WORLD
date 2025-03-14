"""
Service for interacting with the OpenAI API.
Handles operations related to generating talk tracks and other content.
"""
import os
import requests
import json
from typing import Dict, Any, Optional

from ..config.settings import settings


class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self):
        """Initialize the OpenAI service."""
        self.api_key = settings.OPENAI_API_KEY
    
    def generate_talk_track(self, account_name: str, insights: Dict[str, str]) -> Optional[str]:
        """
        Generate a talk track using OpenAI based on research insights.
        
        Args:
            account_name: Name of the account/company
            insights: Dictionary containing industry_insights, company_insights, and vision_insights
            
        Returns:
            The generated talk track or None if there was an error
        """
        industry_insights = insights.get('industry_insights', '')
        company_insights = insights.get('company_insights', '')
        vision_insights = insights.get('vision_insights', '')
        
        # Construct the prompt for the talk track
        talk_track_prompt = f"""You are an experienced SDR at Codeium, an AI coding assistant company that helps developers write code faster and more accurately. 

I'm about to contact {account_name} and need a compelling, highly personalized talk track based on the following AI-generated research insights. CRUCIAL: Extract specific facts from these insights to create a tailored approach.

INDUSTRY INSIGHTS:
{industry_insights}

COMPANY INSIGHTS:
{company_insights}

FORWARD-THINKING VISION:
{vision_insights}

Create a talk track that does ALL of the following:

**1. Hypothesis:**
- Start with a specific, factual hook about {account_name} from the research
- The value hypothesis should take the current research and frame it like this: "If Codeium can [Help avoid risk/deliver critical capability] then <customer> can [business initiative] and achieve [business strategy]"
- Show you've done your homework on their unique situation

**2. Targeted Questions:**
- Include 2-3 targeted questions based on {account_name}'s actual circumstances, list them in bullet points
- Focus on challenges mentioned in the research
- Frame questions to uncover pain points related to {account_name}'s

**3. Current State:**
- Write three bullet points that outline the current state. Underneath each current state bullet point, list at least one negative consequence. If you cannot accurately describe the before scenario your input should be "Need more information to complete request".
- Current state & negative consequences should take into consideration that they should be focus around three things: Is it making the business money? Is it saving the business money? or does it mitigate risk?
- Rank in list order of importance

**4. Clear Next Steps:**
- Suggest a logical next action that makes sense for {account_name}
- Align this with their company profile and apparent buying process
- Make the ask specific and appropriate to their position in the market

Make every aspect of this talk track SPECIFIC to {account_name} - avoid generic statements that could apply to any company. Use actual facts about their technology, challenges, and business objectives from the research.

Structure your response with clear sections, bullet points for key talking points, and bolded headers for better readability. Keep it under 250 words and ensure it flows naturally for a conversation."""

        if not self.api_key:
            print("⚠️ WARNING: OpenAI API key is not configured or is empty")
            return self._get_fallback_talk_track(account_name)
            
        if self.api_key == "your_openai_api_key_here" or self.api_key == "placeholder_key" or self.api_key == "sk-...": 
            print("⚠️ WARNING: Using placeholder OpenAI API key. Please update with a real key.")
            return self._get_fallback_talk_track(account_name)

        print(f"📤 Making OpenAI API request for talk track generation for {account_name}...")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an experienced SDR that creates personalized talk tracks. You MUST follow the exact structure requested by the user, including using the exact section titles (Hypothesis, Targeted Questions, Current State, Clear Next Steps) as specified. Do not use alternative headings like 'Hook' or anything else that was not specifically requested."},
                {"role": "user", "content": talk_track_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            print(f"📡 Connecting to OpenAI API...")
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                response_data = response.json()
                talk_track = response_data['choices'][0]['message']['content']
                print(f"✅ OpenAI API request successful: received {len(talk_track)} characters")
                return talk_track
            else:
                print(f"❌ OpenAI API Error: Status {response.status_code}")
                print(f"Error details: {response.text}")
                return self._get_fallback_talk_track(account_name)
                
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection Error: Could not connect to OpenAI API: {str(e)}")
            return self._get_fallback_talk_track(account_name)
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout Error: OpenAI API request timed out: {str(e)}")
            return self._get_fallback_talk_track(account_name)
        except Exception as e:
            print(f"❌ Unexpected error making OpenAI API request: {str(e)}")
            return self._get_fallback_talk_track(account_name)
            
    def _get_fallback_talk_track(self, account_name: str) -> str:
        """Generate a fallback talk track when API calls fail."""
        return f"""# Personalized Talk Track for {account_name}

**Hypothesis:**
* Based on my research, {account_name} appears to be investing in modernizing your development infrastructure 
* If Codeium can help your developers write better code faster, then {account_name} can accelerate your software delivery and gain competitive advantage
* Your focus on innovation suggests AI coding tools would align well with your technical direction

**Targeted Questions:**
* How are your development teams currently measuring and improving their coding efficiency?
* What challenges is {account_name} facing with code quality and developer productivity?
* How much time do your developers spend on repetitive coding tasks that could be automated?

**Current State:**
* Manual coding processes are slowing down your feature delivery
  * Consequence: Longer time-to-market for new innovations
* Developers are spending time on repetitive tasks instead of high-value work
  * Consequence: Reduced job satisfaction and potential talent retention issues
* Inconsistent code quality across teams requires extensive review processes
  * Consequence: Technical debt accumulation and increased maintenance costs

**Clear Next Steps:**
* I'd like to schedule a 30-minute call to better understand your development workflow and demonstrate how Codeium has helped similar organizations improve developer productivity by 30%+
* Would Tuesday or Thursday afternoon work better for your schedule?"""
