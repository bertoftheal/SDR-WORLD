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

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.urls import url_parse
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

# Try to load environment variables from virtual environment .env file first
venv_env_path = os.path.join(os.path.dirname(__file__), 'venv (backend)', '.env')
if os.path.exists(venv_env_path):
    load_dotenv(venv_env_path, override=True)  # Use the venv .env file with priority
else:
    # Fall back to project-level .env file
    load_dotenv(override=True)  # Force reload environment variables

# Configure API keys
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME', 'Companies')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Print loaded environment variables for debugging
print("Loading environment variables:")
print(f"AIRTABLE_API_KEY: {'Set (truncated for security)' if AIRTABLE_API_KEY else 'Not set'}")
print(f"AIRTABLE_BASE_ID: {AIRTABLE_BASE_ID}")
print(f"AIRTABLE_TABLE_NAME: {AIRTABLE_TABLE_NAME}")

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
    is_configured = AIRTABLE_API_KEY and AIRTABLE_BASE_ID and AIRTABLE_TABLE_NAME
    
    # Log detailed information for debugging
    if not is_configured:
        if not AIRTABLE_API_KEY:
            print("ERROR: AIRTABLE_API_KEY is missing")
        if not AIRTABLE_BASE_ID:
            print("ERROR: AIRTABLE_BASE_ID is missing")
        if not AIRTABLE_TABLE_NAME:
            print("ERROR: AIRTABLE_TABLE_NAME is missing")
    
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
        # If Airtable is configured, try to get accounts from Airtable
        if is_airtable_configured():
            try:
                print(f"Attempting to connect to Airtable with Base ID: {AIRTABLE_BASE_ID}, Table: {AIRTABLE_TABLE_NAME}")
                table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
                
                # Attempt to check API connectivity with enhanced error handling
                try:
                    # Make a direct API request to check authentication status
                    auth_test_url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
                    headers = {
                        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    # Log the attempt with obfuscated API key for debugging
                    masked_key = AIRTABLE_API_KEY[:4] + "*****" + AIRTABLE_API_KEY[-4:] if len(AIRTABLE_API_KEY) > 8 else "***masked***"
                    print(f"Testing Airtable connection with Base ID: {AIRTABLE_BASE_ID}, Table: {AIRTABLE_TABLE_NAME}, Auth: Bearer {masked_key}")
                    
                    # Try a direct GET request first to validate API key and permissions
                    import requests
                    auth_test = requests.get(auth_test_url, headers=headers)
                    
                    if auth_test.status_code != 200:
                        print(f"Airtable API test failed with status code: {auth_test.status_code}")
                        print(f"Error response: {auth_test.text}")
                        raise Exception(f"Airtable API test failed: {auth_test.status_code} - {auth_test.text}")
                    else:
                        print("Airtable API connection validated successfully")
                    
                    # Now proceed with the regular fetch
                    records = table.all()
                    # Debug the raw Airtable response
                    print(f"Raw Airtable response contains {len(records)} records")
                    if records and len(records) > 0:
                        sample_record = records[0]
                        print(f"Sample record fields: {list(sample_record['fields'].keys())}")
                    else:
                        print("Airtable returned empty records list (valid API call but no data)")
                        
                except requests.exceptions.RequestException as req_error:
                    print(f"Airtable HTTP request error: {str(req_error)}")
                    raise Exception(f"Airtable connection error: {str(req_error)}")
                except Exception as airtable_error:
                    error_msg = str(airtable_error)
                    print(f"Airtable error: {error_msg}")
                    
                    if 'AUTHENTICATION_REQUIRED' in error_msg or 'Unauthorized' in error_msg or '401' in error_msg:
                        print(f"Airtable authentication failed: API key may be invalid or expired. Using mock data instead.")
                    elif 'NOT_FOUND' in error_msg or '404' in error_msg:
                        print(f"Airtable resource not found: Base ID or Table name may be incorrect.")
                    elif 'PERMISSION_DENIED' in error_msg or '403' in error_msg:
                        print(f"Airtable permission denied: The API key may not have access to this base/table.")
                    
                    # Fall through to the mock data logic below
                    raise Exception(f"Airtable error: {error_msg} - using mock data instead")
                
                if records:
                    # Try multiple field names that might contain company names
                    possible_name_fields = ['Name', 'Company', 'Account', 'Company Name', 'Account Name']
                    
                    accounts = []
                    for record in records:
                        # Check all possible fields for the company name
                        company_name = None
                        for field in possible_name_fields:
                            if field in record['fields'] and record['fields'][field]:
                                company_name = record['fields'][field]
                                break
                        
                        if company_name:
                            accounts.append({
                                'id': record['id'],
                                'name': company_name
                            })
                    
                    print(f"Successfully extracted {len(accounts)} account names from Airtable")
                    if accounts:
                        print(f"First few accounts: {[a['name'] for a in accounts[:5]]}")
                    
                    # Remove duplicates while preserving order
                    unique_accounts = []
                    seen_names = set()
                    for account in accounts:
                        if account['name'] not in seen_names:
                            seen_names.add(account['name'])
                            unique_accounts.append(account)
                    
                    # Sort alphabetically by name
                    unique_accounts.sort(key=lambda x: x['name'])
                    
                    if unique_accounts:
                        print(f"Returning {len(unique_accounts)} unique accounts from Airtable")
                        return jsonify(unique_accounts)
                    else:
                        print("No valid account names found in Airtable records")
                else:
                    print("No records returned from Airtable")
            except Exception as e:
                print(f"Error fetching from Airtable: {str(e)}")
                # Print traceback for more detailed error information
                import traceback
                traceback.print_exc()
        
        # Fallback to mock data with a smaller list of key companies
        print("Using mock account data as fallback due to Airtable authentication issue")
        mock_accounts = [
            {"id": "rec123", "name": "Cisco"},
            {"id": "rec456", "name": "Hitachi Vantara"},
            {"id": "rec789", "name": "BNY Mellon"},
            {"id": "rec101", "name": "Hubspot"},
            {"id": "rec202", "name": "Microsoft"},
            {"id": "rec303", "name": "Google"},
            {"id": "rec404", "name": "Amazon"},
            {"id": "rec505", "name": "Apple"},
            {"id": "rec606", "name": "Salesforce"},
            {"id": "rec707", "name": "Oracle"},
            {"id": "rec808", "name": "Adobe"},
            {"id": "rec909", "name": "Slack"},
            {"id": "rec1010", "name": "Tesla"},
            {"id": "rec1111", "name": "IBM"},
            {"id": "rec1212", "name": "Intel"}
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
        
        # Prepare comprehensive mock data that follows the expected format with headers and content
        def get_mock_industry_insights(company):
            return f"### 1. AI Adoption Trends\n{company} is seeing significant AI adoption, particularly in network infrastructure upgrades for AI applications, with over $700 million in AI infrastructure orders in the first half of fiscal 2025.\n\n### 2. Developer Tools\nDevelopers at {company} utilize a wide range of tools to streamline network and data center management, potentially integrating AI code assistants for efficiency.\n\n### 3. Development Challenges\nKey challenges include maintaining development velocity and ensuring code quality while integrating complex AI systems.\n\n### 4. Market Opportunity\nAI coding assistants like Codeium can enhance development speed and quality, offering significant efficiency gains.\n\n### 5. Competitive Landscape\nThe market includes tools like GitHub Copilot and TabNine. Codeium differentiates with its proprietary language models and enterprise-grade security."
        
        def get_mock_company_insights(company):
            return f"### 1. Technology Stack\n{company} utilizes a diverse technology stack including Python, Java, and JavaScript for their development needs, with a growing focus on cloud-native technologies.\n\n### 2. AI Strategy\nTheir public AI strategy focuses on integrating machine learning across their product portfolio, with recent announcements highlighting investments in generative AI.\n\n### 3. Development Team\nWith over 5,000 engineers worldwide, {company} has a decentralized development organization with specialized teams for each product area.\n\n### 4. Pain Points\nDevelopment velocity remains a key challenge, with code reviews and quality assurance processes creating bottlenecks in delivery pipelines.\n\n### 5. Recent Initiatives\nRecent digital transformation efforts focus on modernizing legacy systems and improving developer productivity through automation and AI tools."
        
        def get_mock_vision_insights(company):
            return f"### 1. AI Integration Strategy\n{company}'s future AI strategy likely includes deeper integration of coding assistants across their development workflow, potentially starting with their most active product teams.\n\n### 2. Efficiency Improvements\nImplementing tools like Codeium could reduce development cycle times by 18-25%, freeing up developer resources for innovation rather than routine coding tasks.\n\n### 3. Codeium Implementation\n{company} could leverage Codeium to accelerate their modernization initiatives, particularly for teams working on legacy code maintenance and migration.\n\n### 4. Return on Investment\nBased on their team size, {company} could expect 7-figure annual productivity gains from implementing AI coding assistants company-wide.\n\n### 5. Risk Mitigation\nFalling behind in AI adoption could impact their competitive position, particularly as rivals implement similar solutions to accelerate development."
        
        def get_mock_talk_track(company):
            return f"### Opening Hook\nI've been following {company}'s recent digital transformation initiatives, particularly your focus on modernizing development practices through AI integration. Your CTO's recent comment about improving developer velocity caught my attention.\n\n### Targeted Questions\n1. How are your engineering teams currently addressing the code review bottlenecks mentioned in your recent tech blog?\n2. With your expansion into cloud-native services, what challenges are you facing with maintaining development speed?\n3. How are you currently measuring and improving developer productivity across your global engineering organization?\n\n### Value Proposition\nCodeium has helped companies similar to {company} reduce development cycles by up to 25% while improving code quality. Our enterprise-grade AI coding assistant integrates seamlessly with your existing tools and supports all the languages in your stack.\n\n### Clear Next Steps\nI'd like to arrange a brief demo with one of your engineering leaders to show how Codeium specifically addresses your development challenges. Would Tuesday or Wednesday next week work for an introductory call?"
        
        if use_mock:
            print("Using mock data as API keys are not properly set")
            mock_industry = get_mock_industry_insights(account_name)
            mock_company = get_mock_company_insights(account_name)
            mock_vision = get_mock_vision_insights(account_name)
            mock_talk_track = get_mock_talk_track(account_name)
            
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
                    },
                    timeout=15  # Add a timeout to prevent hanging connections
                )
                
                if response.status_code == 200:
                    results[key] = response.json()['choices'][0]['message']['content']
                else:
                    print(f"Perplexity API error: {response.status_code} - {response.text}")
                    # Fall back to mock data when API call fails
                    if key == 'industryInsights':
                        results[key] = get_mock_industry_insights(account_name)
                    elif key == 'companyInsights':
                        results[key] = get_mock_company_insights(account_name)
                    elif key == 'visionInsights':
                        results[key] = get_mock_vision_insights(account_name)
            except requests.exceptions.RequestException as e:
                print(f"Perplexity API request error: {str(e)}")
                # Fall back to mock data on request errors
                if key == 'industryInsights':
                    results[key] = get_mock_industry_insights(account_name)
                elif key == 'companyInsights':
                    results[key] = get_mock_company_insights(account_name)
                elif key == 'visionInsights':
                    results[key] = get_mock_vision_insights(account_name)
            except Exception as e:
                print(f"Unexpected error with Perplexity API: {str(e)}")
                # Fall back to mock data on any other errors
                if key == 'industryInsights':
                    results[key] = get_mock_industry_insights(account_name)
                elif key == 'companyInsights':
                    results[key] = get_mock_company_insights(account_name)
                elif key == 'visionInsights':
                    results[key] = get_mock_vision_insights(account_name)
        
        # Generate talk track using OpenAI's ChatGPT API
        # Read API key directly from .env file as a fallback in case environment variables didn't load properly
        api_key_for_request = OPENAI_API_KEY
        
        # If the API key is empty, try to read it directly from the .env file
        if not api_key_for_request or len(api_key_for_request) < 10:
            print("OpenAI API key not found in environment variables, attempting to read from .env file...")
            try:
                with open('/Users/albertperez.codeium/Desktop/CascadeProjects/SDR-WORLD/.env', 'r') as env_file:
                    for line in env_file:
                        if line.startswith('OPENAI_API_KEY='):
                            api_key_for_request = line.strip().split('=', 1)[1]
                            print(f"Successfully read OpenAI API key from .env file. Length: {len(api_key_for_request)}")
                            break
            except Exception as e:
                print(f"Error reading .env file: {str(e)}")
        
        # Add debug information
        if api_key_for_request and len(api_key_for_request) > 10:
            print(f"\nOpenAI API Key: {api_key_for_request[:5]}...{api_key_for_request[-5:]}")
        else:
            print("\nOpenAI API Key is still invalid or empty")
        
        openai_headers = {
            'Authorization': f'Bearer {api_key_for_request}',
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
        
        try:
            try:
                # Print debugging info for OpenAI API call
                print(f"\n=== CALLING OPENAI API FOR TALK TRACK ===\nAccount: {account_name}\nAPI Key Status: {'Valid' if OPENAI_API_KEY and len(OPENAI_API_KEY) > 20 else 'Invalid/Missing'}")
                print(f"API Key: {OPENAI_API_KEY[:5]}...{OPENAI_API_KEY[-5:] if OPENAI_API_KEY and len(OPENAI_API_KEY) > 10 else 'N/A'}")
                
                # Call OpenAI API for the talk track with enhanced error handling
                try:
                    print("Attempting to call OpenAI API...")
                    talk_track_response = requests.post(
                        'https://api.openai.com/v1/chat/completions',
                        headers=openai_headers,
                        json={
                            'model': 'gpt-3.5-turbo',
                            'messages': [{'role': 'user', 'content': talk_track_prompt}],
                            'max_tokens': 500
                        },
                        timeout=30  # Increased timeout for better reliability
                    )
                    print(f"OpenAI API response status code: {talk_track_response.status_code}")
                    
                    # Print full response for debugging
                    if talk_track_response.status_code != 200:
                        print(f"OpenAI API error response: {talk_track_response.text}")
                    
                except requests.exceptions.ConnectionError as conn_err:
                    print(f"OpenAI API connection error: {str(conn_err)}")
                    print("This could be due to network issues or an invalid API key format")
                    # Don't try to continue with the actual request, jump to the mock data
                    print("Falling back to mock talk track data due to connection error")
                    results['recommendedTalkTrack'] = get_mock_talk_track(account_name)
                    return jsonify(results)
                
                # Log response information
                print(f"OpenAI API Response Status: {talk_track_response.status_code}")
                
                if talk_track_response.status_code == 200:
                    response_json = talk_track_response.json()
                    print(f"OpenAI response successful. Content length: {len(response_json['choices'][0]['message']['content'])}")
                    results['recommendedTalkTrack'] = response_json['choices'][0]['message']['content']
                    print("Talk track successfully generated and saved to results dictionary")
                else:
                    # For any error status code, use the mock data function
                    print(f"OpenAI API error: {talk_track_response.status_code} - {talk_track_response.text}")
                    print("Falling back to mock talk track data")
                    mock_talk_track = get_mock_talk_track(account_name)
                    results['recommendedTalkTrack'] = mock_talk_track
                    print(f"Mock talk track successfully generated: {len(mock_talk_track)} characters")
            except requests.exceptions.SSLError as ssl_err:
                # Handle SSL error specifically with better logging
                print(f"OpenAI API SSL error: {str(ssl_err)}")
                results['recommendedTalkTrack'] = get_mock_talk_track(account_name)
            except requests.exceptions.RequestException as req_err:
                # Handle request exceptions with better logging
                print(f"OpenAI API request error: {str(req_err)}")
                results['recommendedTalkTrack'] = get_mock_talk_track(account_name)
            except Exception as e:
                # General exception handler with better logging
                print(f"Unexpected error with OpenAI API: {str(e)}")
                results['recommendedTalkTrack'] = get_mock_talk_track(account_name)
        except Exception as e:
            # Outer exception handler catches any issues with the mock data generation
            print(f"Error in talk track generation process: {str(e)}")
            results['recommendedTalkTrack'] = get_mock_talk_track(account_name)
        
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
    app.run(debug=True, port=5001)
