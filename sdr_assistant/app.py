"""
SDR Research Assistant Application
-----------------------------------
This application serves as a research tool for sales development representatives at Codeium.
It uses the Perplexity API to generate insights about companies and industries, and the OpenAI API 
to create a recommended talk track. The data can be stored in and retrieved from Airtable.

APIs Used:
- Perplexity API: For generating industry, company, and forward-thinking insights
- OpenAI API: For generating the recommended talk track
- Airtable API: For storing and retrieving account data and research

Main Functionality:
1. Retrieve accounts from Airtable (or use mock data if not configured)
2. Generate insights for selected accounts using AI
3. Save generated insights back to Airtable
"""

from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from pyairtable import Table
import os
import requests
import json
from datetime import datetime
import jwt
import bcrypt

# Create Flask app
app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)  # Enable CORS for all routes
load_dotenv(override=True)  # Force reload environment variables

# Configure API keys
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'dev_secret_key_change_in_production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 86400  # 24 hours in seconds

# Mock users for demo - in production, this would be in a database
USERS = [
    {
        'id': '1',
        'email': 'albert@example.com',
        'name': 'Albert Perez',
        'password_hash': bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    },
    {
        'id': '2',
        'email': 'sales@example.com',
        'name': 'Sales Rep',
        'password_hash': bcrypt.hashpw('demo'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    }
]

# Mock library entries for demo - in production, this would be in a database
LIBRARY_ENTRIES = [
    {
        'id': '1',
        'title': 'AI Trends in Enterprise Software',
        'content': 'The enterprise software industry is witnessing rapid adoption of AI technologies across various functions. Companies are integrating machine learning capabilities to enhance decision-making processes, automate routine tasks, and extract insights from vast amounts of data. Particularly notable is the implementation of natural language processing (NLP) to improve customer service interactions and generative AI to assist with content creation and coding tasks.',
        'category': 'Industry',
        'dateAdded': '2025-02-20T15:30:00Z',
        'userId': '1',
        'tags': ['AI', 'Enterprise Software', 'Machine Learning', 'NLP']
    },
    {
        'id': '2',
        'title': 'Cloud Computing Adoption Patterns',
        'content': 'Organizations are increasingly adopting multi-cloud strategies to avoid vendor lock-in and leverage best-in-class services from different providers. According to recent surveys, 85% of enterprises now employ a multi-cloud approach, with the average organization using services from 2.6 different cloud providers. This trend is particularly prevalent in highly regulated industries such as finance and healthcare, where specific compliance requirements necessitate different cloud configurations.',
        'category': 'Industry',
        'dateAdded': '2025-02-15T10:15:00Z',
        'userId': '1',
        'tags': ['Cloud Computing', 'Multi-cloud', 'Digital Transformation']
    }
]

# Debug output
print(f"Loading environment variables:")
print(f"AIRTABLE_API_KEY: {'Set (hidden for security)' if AIRTABLE_API_KEY else 'Not set'}")
print(f"AIRTABLE_BASE_ID: {AIRTABLE_BASE_ID}")
print(f"AIRTABLE_TABLE_NAME: {AIRTABLE_TABLE_NAME}")
print(f"PERPLEXITY_API_KEY: {'Set (hidden for security)' if PERPLEXITY_API_KEY else 'Not set'}")
print(f"OPENAI_API_KEY: {'Set (hidden for security)' if OPENAI_API_KEY else 'Not set'}")

# Check if Airtable credentials are properly configured
def is_airtable_configured():
    """Check if Airtable credentials are properly configured"""
    is_configured = (AIRTABLE_API_KEY and AIRTABLE_API_KEY != 'your_airtable_api_key_here' and
            AIRTABLE_BASE_ID and AIRTABLE_BASE_ID != 'your_airtable_base_id_here' and
            AIRTABLE_TABLE_NAME and AIRTABLE_TABLE_NAME != 'your_airtable_table_name_here')
    
    print(f"Airtable configured: {is_configured}")
    return is_configured

# Add version for cache busting
VERSION = '1.0.3'

@app.route('/')
def index():
    """
    Root route: Serves the main application interface.
    Returns the static index.html file when a user visits the root URL.
    """
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Authentication helper functions
def generate_token(user_id):
    """Generate a new JWT token for a user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow().timestamp() + JWT_EXPIRATION
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token):
    """Verify a JWT token and return the user_id if valid"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def get_current_user(request):
    """Get the current user from request headers"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return None
    
    # Find the user in our mock database
    for user in USERS:
        if user['id'] == user_id:
            # Don't include password_hash in the returned user
            return {
                'id': user['id'],
                'email': user['email'],
                'name': user['name']
            }
    
    return None

# Authentication API endpoints
@app.route('/api/login', methods=['POST'])
def login():
    """
    API Route: User login
    
    Authenticates a user and returns a JWT token if credentials are valid.
    
    Returns:
        JSON with success status, token if successful, and error message if not
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    # Find user by email
    user = None
    for u in USERS:
        if u['email'] == email:
            user = u
            break
    
    if not user:
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    # Generate token
    token = generate_token(user['id'])
    
    return jsonify({
        'success': True,
        'token': token,
        'userName': user['name']
    })

@app.route('/api/accounts')
def get_accounts():
    """
    API Route: Retrieve accounts 
    
    Either fetches accounts from Airtable if credentials are configured,
    or returns mock account data for demonstration purposes.
    
    Returns:
        JSON array of accounts with 'id' and 'name' properties
    """
    try:
        # Print environment variables for debugging
        print(f"AIRTABLE_API_KEY: {AIRTABLE_API_KEY[:10]}... (truncated for security)")
        print(f"AIRTABLE_BASE_ID: {AIRTABLE_BASE_ID}")
        print(f"AIRTABLE_TABLE_NAME: {AIRTABLE_TABLE_NAME}")
        
        # If Airtable is configured, try to get accounts from Airtable
        if is_airtable_configured():
            try:
                print(f"Attempting to connect to Airtable with Base ID: {AIRTABLE_BASE_ID}, Table: {AIRTABLE_TABLE_NAME}")
                table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
                records = table.all()
                
                if records:
                    # Extract account names from the 'Name' field in Airtable
                    accounts = [{'id': record['id'], 'name': record['fields'].get('Name', '')} for record in records if 'Name' in record['fields']]
                    
                    print(f"Successfully fetched {len(accounts)} accounts from Airtable")
                    print(f"First few accounts: {[a['name'] for a in accounts[:5]]}")
                    
                    # Only return non-empty records
                    accounts = [account for account in accounts if account['name']]
                    
                    if accounts:
                        return jsonify(accounts)
                    else:
                        print("No valid account names found in Airtable records")
                else:
                    print("No records returned from Airtable")
            except Exception as e:
                print(f"Error fetching from Airtable: {str(e)}")
        
        # Fallback to mock data if Airtable fetch fails or not configured
        print("Using mock account data as fallback")
        mock_accounts = [
            {"id": "rec123", "name": "TechNova Solutions"},
            {"id": "rec456", "name": "Quantum Innovations"},
            {"id": "rec789", "name": "DevOps Masters Inc."},
            {"id": "rec101", "name": "CloudSync Technologies"},
            {"id": "rec202", "name": "Agile Development Partners"},
            {"id": "rec303", "name": "ByteForge Software"},
            {"id": "rec404", "name": "CodeStream Labs"},
            {"id": "rec505", "name": "AI Engineering Group"},
            {"id": "rec606", "name": "DataStack Solutions"},
            {"id": "rec707", "name": "Neural Systems"}
        ]
        return jsonify(mock_accounts)
        
    except Exception as e:
        print(f"Unhandled error in get_accounts: {str(e)}")
        # Return a minimal set of mock data in case of error
        mock_accounts = [
            {"id": "rec123", "name": "TechNova Solutions"},
            {"id": "rec456", "name": "Quantum Innovations"},
            {"id": "rec789", "name": "DevOps Masters Inc."}
        ]
        return jsonify(mock_accounts)

@app.route('/api/accounts/details')
def get_account_details():
    """
    API Route: Get detailed account information
    
    Returns accounts with additional details like industry, employees, and location.
    
    Returns:
        JSON array of account objects with detailed information
    """
    try:
        # Get the base accounts first
        accounts_response = get_accounts()
        accounts = json.loads(accounts_response.data)
        
        # Add mock details for demonstration purposes
        # In a real implementation, this data would come from Airtable
        industries = ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail']
        locations = ['San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA', 'Chicago, IL']
        
        for account in accounts:
            # Add random details
            account_name = account['name'].lower()
            
            if 'tech' in account_name or 'nova' in account_name or 'software' in account_name:
                account['industry'] = 'Technology'
            elif 'finance' in account_name or 'bank' in account_name:
                account['industry'] = 'Finance'
            elif 'health' in account_name or 'care' in account_name or 'med' in account_name:
                account['industry'] = 'Healthcare'
            else:
                import random
                account['industry'] = random.choice(industries)
            
            # Add employees count
            account['employees'] = str(int(hash(account['name']) % 9000 + 1000))
            
            # Add location
            account['location'] = locations[hash(account['name']) % len(locations)]
            
        return jsonify(accounts)
    except Exception as e:
        print(f"Error in get_account_details: {str(e)}")
        return jsonify([]), 500

@app.route('/api/research', methods=['POST'])
def generate_research():
    """
    API Route: Generate Research
    
    Accepts a POST request with an account name.
    Uses Perplexity API to generate three types of insights:
    - Industry insights
    - Company insights
    - Forward-thinking vision
    
    Then uses OpenAI API to generate a recommended talk track based on these insights.
    
    Request Body:
        JSON: { "accountName": "Company Name" }
        
    Returns:
        JSON with four fields: industryInsights, companyInsights, visionInsights, recommendedTalkTrack
    """
    try:
        data = request.json
        account_name = data.get('accountName')  # Changed from account_name to accountName to match frontend
        account_id = data.get('accountId')  # Changed for consistency
        
        # Create result dictionary
        results = {}
        
        # For demo purposes, if API keys are not set, return mock data
        print(f"PERPLEXITY_API_KEY set: {bool(PERPLEXITY_API_KEY)}")
        print(f"OPENAI_API_KEY set: {bool(OPENAI_API_KEY)}")
        print(f"Account name: {account_name}")
        
        use_mock = not PERPLEXITY_API_KEY or not OPENAI_API_KEY
        print(f"Using mock data: {use_mock}")
        
        if use_mock:
            print("Using mock data as API keys are not properly set")
            mock_industry = "The technology sector continues to evolve rapidly with AI integration becoming a standard across all verticals. Companies focusing on cloud solutions are seeing 30% YoY growth, while cybersecurity spending is projected to reach $170B globally by end of year."
            mock_company = "{} has positioned itself strategically in the enterprise software space with recent acquisitions strengthening their product portfolio. Their Q2 earnings exceeded analyst expectations by 15%, and their market share has grown by 7% this fiscal year.".format(account_name)
            mock_vision = "The company is investing heavily in AI and machine learning capabilities, allocating 22% of their R&D budget to these initiatives. Their 5-year roadmap includes expansion into emerging markets and development of industry-specific solutions."
            mock_talk_track = "When engaging with {}, highlight our complementary technology stack and how our solution addresses their publicly stated goal of improving operational efficiency. Reference their recent digital transformation initiative and position our offering as an accelerator for their strategic objectives.".format(account_name)
            
            results = {
                'industryInsights': mock_industry,
                'companyInsights': mock_company,
                'visionInsights': mock_vision,
                'recommendedTalkTrack': mock_talk_track
            }
            return jsonify(results)
        
        # Call Perplexity API to generate top 3 insight sections
        perplexity_headers = {
            'Authorization': f'Bearer {PERPLEXITY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Industry Insights
        industry_prompt = f"""As an expert SDR at Codeium with a PHD level of sales experience, an innovative AI coding assistant company, provide detailed, SPECIFIC industry insights about {account_name}'s market. 
        
**Focus specifically on these key areas:**

**1. AI Adoption Trends:**
- Current AI adoption trends in {account_name}'s specific industry sector (not general AI trends)

- How companies in this sector are implementing AI in development workflows

**2. Developer Tools:**
- How {account_name} and similar companies are utilizing developer tools and AI code assistants

- Popular development environments and frameworks in their sector

**3. Development Challenges:**
- Key challenges {account_name} likely faces with development velocity and code quality

- Pain points that engineering teams in this industry typically experience

**4. Market Opportunity:**
- Market opportunities for AI coding assistants specifically in {account_name}'s sector

- Potential efficiency gains they could realize with Codeium

**5. Competitive Landscape:**
- Competitive landscape for developer productivity tools that {account_name} might be evaluating

- How Codeium differentiates in their specific market

Research SPECIFIC facts about {account_name}'s industry position, tech stack, and development practices before responding.
Keep your response under 200 words, use bullet points and clear section headers for readability, and target it for a Codeium sales development representative preparing to contact {account_name}."""
        
        # Company Insights
        company_prompt = f"""As an SDR at Codeium, an AI coding assistant company, provide SPECIFIC, factual research about {account_name} as a company with focus on:

**1. Technology Stack:**
- {account_name}'s current technology stack and development processes

- Programming languages, frameworks, and tools they commonly use

- Development environments or platforms they rely on

**2. AI Strategy:**
- Public information about {account_name}'s AI adoption or strategy

- Recent AI-related announcements or initiatives

- Key technology leaders driving their AI vision

**3. Development Team:**
- Software development team size at {account_name} and structure if available

- Engineering leadership and organizational approach

- Recent engineering hires or team growth patterns

**4. Pain Points:**
- Development challenges {account_name} might be experiencing

- Technical debt or bottlenecks based on their stack and industry

- Opportunities for improving developer productivity

**5. Recent Initiatives:**
- Technology initiatives or digital transformation efforts

- Product launches requiring significant development resources

- Strategic technical pivots or roadmap shifts

**6. Budget Considerations:**
- Potential budget cycle or purchasing timeline information

- Financial reporting periods that might impact buying decisions

IMPORTANT: Research actual facts about {account_name}, not general information. Include specific technologies, tools, or practices they use, and cite industry reports or company announcements where possible.

Frame this for a Codeium SDR preparing to contact {account_name}. Use bullet points and clear section headers for readability. Keep your response under 200 words."""
        
        # Forward Thinking Vision
        vision_prompt = f"""As an SDR at Codeium, predict specifically how {account_name} might evolve their AI and development strategy over the next 2-3 years.

**Consider {account_name}'s future across these dimensions:**

**1. AI Integration Strategy:**
- How {account_name} might integrate AI into their development workflow

- Potential implementation phases based on their current tech stack

- Strategic areas where they'd likely prioritize AI assistance first

**2. Efficiency Improvements:**
- Quantifiable efficiency gains from adopting AI coding assistants

- Potential reduction in development cycle times (estimate percentage)

- How AI could transform their code review and QA processes

**3. Codeium Implementation:**
- Specific ways {account_name} could leverage Codeium for their unique needs

- How Codeium aligns with their apparent development challenges

- Team-specific benefits across their engineering organization

**4. Return on Investment:**
- The ROI {account_name} might expect from implementing AI tools

- Cost savings calculations based on their industry and company size

- Competitive advantages they would gain through earlier adoption

**5. Risk Mitigation:**
- Technical challenges they might face without AI assistance

- How falling behind in AI adoption could impact their market position

- Security and compliance benefits from standardized AI coding tools

Make this forward-looking vision SPECIFIC to {account_name} - reference their industry position, current tools, and business objectives where possible.

Use bullet points and clear section headers for better readability. This should help a Codeium SDR articulate a compelling future vision that positions Codeium as essential to {account_name}'s success. Keep your response under 200 words."""
        
        # Call Perplexity API for each of the top 3 sections
        prompts = {
            'industryInsights': industry_prompt,
            'companyInsights': company_prompt,
            'visionInsights': vision_prompt
        }
        
        for key, prompt in prompts.items():
            try:
                response = requests.post(
                    'https://api.perplexity.ai/chat/completions',
                    headers=perplexity_headers,
                    json={
                        'model': 'sonar',  # Updated to a verified model name from docs
                        'messages': [{'role': 'user', 'content': prompt}]
                    }
                )
                
                if response.status_code == 200:
                    results[key] = response.json()['choices'][0]['message']['content']
                else:
                    results[key] = f"Error generating {key}: {response.status_code} - {response.text}"
            except Exception as e:
                results[key] = f"Error generating {key}: {str(e)}"
        
        # Generate talk track using OpenAI's ChatGPT API
        openai_headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Prepare talk track prompt with the insights we gathered from Perplexity
        talk_track_prompt = f"""You are an experienced SDR at Codeium, an AI coding assistant company that helps developers write code faster and more accurately. 

I'm about to contact {account_name} and need a compelling, highly personalized talk track based on the following AI-generated research insights. CRUCIAL: Extract specific facts from these insights to create a tailored approach.

---RESEARCH INSIGHTS ABOUT {account_name.upper()}---

INDUSTRY INSIGHTS:
{results.get('industryInsights', 'No industry insights available')}

COMPANY INSIGHTS:
{results.get('companyInsights', 'No company insights available')}

FORWARD THINKING VISION:
{results.get('visionInsights', 'No vision insights available')}

---END OF RESEARCH INSIGHTS---

Create a talk track that does ALL of the following:

**1. Opening Hook:**
- Start with a specific, factual hook about {account_name} from the research
- Reference their specific challenges or initiatives
- Show you've done your homework on their unique situation

**2. Targeted Questions:**
- Include 2-3 targeted questions based on {account_name}'s actual circumstances
- Focus on challenges mentioned in the research
- Frame questions to uncover pain points related to developer productivity

**3. Value Proposition:**
- Provide clear value statements connecting Codeium's benefits to {account_name}'s specific needs
- Quantify potential improvements where possible (time savings, ROI)
- Address their particular technical environment and challenges

**4. Clear Next Steps:**
- Suggest a logical next action that makes sense for {account_name}
- Align this with their company profile and apparent buying process
- Make the ask specific and appropriate to their position in the market

Make every aspect of this talk track SPECIFIC to {account_name} - avoid generic statements that could apply to any company. Use actual facts about their technology, challenges, and business objectives from the research.

Structure your response with clear sections, bullet points for key talking points, and bolded headers for better readability. Keep it under 250 words and ensure it flows naturally for a conversation."""
        
        try:
            try:
                # Call OpenAI API for the talk track
                talk_track_response = requests.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers=openai_headers,
                    json={
                        'model': 'gpt-3.5-turbo',  # Using a more standard model
                        'messages': [{'role': 'user', 'content': talk_track_prompt}],
                        'max_tokens': 500
                    },
                    timeout=15  # Add a timeout to prevent hanging connections
                )
                
                if talk_track_response.status_code == 200:
                    results['recommendedTalkTrack'] = talk_track_response.json()['choices'][0]['message']['content']
                else:
                    # For any error status code, use mock data
                    mock_talk_track = f"""
Based on our research about {account_name}, here's how I recommend approaching your initial conversation:

**Opening Hook**: I noticed that {account_name} has been investing significantly in software development resources, particularly in AI integration. Given the increased complexity in your tech stack, I thought you might be interested in how other similar companies are improving developer productivity.

**Questions to Explore**:
1. How are your development teams currently handling coding efficiency across your growing technical needs?
2. What challenges are you facing with maintaining code quality as you scale?
3. Have you explored AI-assisted coding tools as part of your development workflow?

**Value Proposition**: Codeium has helped similar organizations achieve 15-25% faster development cycles while reducing bug rates by up to 30%. Our AI assistant integrates seamlessly with your existing workflow and requires minimal onboarding.

**Next Steps**: I'd love to schedule a 30-minute demo to show you specifically how Codeium could fit into your development environment. Would next Tuesday or Wednesday work for your team?
"""
                    results['recommendedTalkTrack'] = mock_talk_track
            except requests.exceptions.SSLError as ssl_err:
                # Handle SSL error specifically with a better message
                results['recommendedTalkTrack'] = f"""
**Sample Talk Track**

Based on the insights about {account_name}, here's a suggested approach for your call:

**Opening**: I've been following {account_name}'s recent initiatives in technology development and noticed your focus on improving developer productivity.

**Questions**:
1. How are your development teams currently managing the balance between delivery speed and code quality?
2. What tools are you using to support your developers' workflow?
3. Where do you see the biggest opportunities for efficiency gains in your development process?

**Value Proposition**: Codeium typically helps organizations reduce development time by 15-20% while improving code quality through AI-assisted suggestions and automated best practices.

**Call to Action**: I'd love to schedule a brief demo to show you specifically how this might work in your environment. Would that be valuable?

[Note: This is a mock talk track. OpenAI API connection error: SSL certificate verification failed. Please check your network settings or API key configuration.]
"""
            except Exception as e:
                # General exception handler with mock data
                results['recommendedTalkTrack'] = f"Unable to generate talk track: {str(e)}. Please check your API keys and network connection."
        except Exception as e:
            results['recommendedTalkTrack'] = f"Error generating talk track: {str(e)}"
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_to_airtable():
    """
    API Route: Save research to Airtable.
    
    Saves the generated industry insights, company insights, 
    vision insights, and talk track for a specific account to Airtable.
    
    Request Body:
        JSON: { 
            "accountId": "rec123", 
            "accountName": "Company Name",
            "industryInsights": "Text...",
            "companyInsights": "Text...",
            "visionInsights": "Text...",
            "recommendedTalkTrack": "Text..."
        }
        
    Returns:
        JSON: { "success": true/false, "message": "Success/error message" }
    """
    try:
        data = request.json
        
        # If Airtable is not configured or we're in demo mode, just return success
        if not is_airtable_configured():
            return jsonify({
                'success': True,
                'message': 'Demo mode: Research would be saved to Airtable if configured. Add your Airtable credentials to .env to enable saving.'
            })
            
        # Otherwise, attempt to save to Airtable
        account_id = data.get('accountId')
        account_name = data.get('accountName')
        industry_insights = data.get('industryInsights')
        company_insights = data.get('companyInsights')
        vision_insights = data.get('visionInsights')
        talk_track = data.get('recommendedTalkTrack')
        
        # Create table connection
        table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
        
        # Create a record in Airtable
        table.create({
            'Name': account_name,
            'Industry Insights': industry_insights,
            'Company Insights': company_insights,
            'Vision Insights': vision_insights,
            'Talk Track': talk_track,
            'Generated Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return jsonify({
            'success': True,
            'message': f'Research saved to Airtable for {account_name}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error saving to Airtable: {str(e)}. Please check your Airtable configuration.'
        })

@app.route('/api/library')
def get_library_entries():
    """
    API Route: Get knowledge library entries
    
    Returns saved insights and research from the knowledge library.
    
    Returns:
        JSON array of library entry objects
    """
    try:
        # In a real implementation, we would filter by user ID from the JWT token
        # For demo purposes, we'll return all entries
        return jsonify(LIBRARY_ENTRIES)
    except Exception as e:
        print(f"Error in get_library_entries: {str(e)}")
        return jsonify([]), 500

@app.route('/api/library', methods=['POST'])
def add_library_entry():
    """
    API Route: Add an entry to the knowledge library
    
    Saves a new insight or piece of research to the knowledge library.
    
    Returns:
        JSON with success status and the newly created entry
    """
    try:
        # Get the current user (would use JWT auth in production)
        data = request.json
        
        # Generate a unique ID (in production this would be handled by the database)
        import uuid
        entry_id = str(uuid.uuid4())
        
        # Create the entry
        new_entry = {
            'id': entry_id,
            'title': data.get('title'),
            'content': data.get('content'),
            'category': data.get('category'),
            'dateAdded': datetime.utcnow().isoformat() + 'Z',
            'userId': '1',  # Hard-coded for demo
            'accountName': data.get('accountName'),
            'tags': data.get('tags', [])
        }
        
        # Add to our "database"
        LIBRARY_ENTRIES.append(new_entry)
        
        return jsonify({
            'success': True,
            'entry': new_entry
        })
    except Exception as e:
        print(f"Error in add_library_entry: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to add library entry'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
