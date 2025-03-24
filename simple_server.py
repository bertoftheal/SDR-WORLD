from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__, static_folder='sdr_assistant/static')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('sdr_assistant/templates', 'home.html')

@app.route('/home.html')
def serve_home():
    return send_from_directory('sdr_assistant/templates', 'home.html')

@app.route('/index.html')
def serve_research_page():
    return send_from_directory('sdr_assistant/templates', 'index.html')

@app.route('/accounts.html')
def serve_accounts():
    return send_from_directory('sdr_assistant/templates', 'accounts.html')
    
@app.route('/library.html')
def serve_library():
    return send_from_directory('sdr_assistant/templates', 'library.html')
    
@app.route('/dashboard.html')
def serve_dashboard():
    return send_from_directory('sdr_assistant/templates', 'dashboard.html')
    
@app.route('/account-detail.html')
def serve_account_detail():
    return send_from_directory('sdr_assistant/templates', 'account-detail.html')
    
@app.route('/research.html')
def serve_research():
    return send_from_directory('sdr_assistant/templates', 'research.html')
    
@app.route('/login.html')
def serve_login():
    return send_from_directory('sdr_assistant/templates', 'login.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('sdr_assistant/static', path)
    
@app.route('/js/<path:path>')
def serve_js(path):
    return send_from_directory('sdr_assistant/templates/js', path)

# API endpoint for library items
@app.route('/api/library')
def api_library():
    # Mock data for the library
    library_items = [
        {
            "id": 1,
            "title": "AI in Sales: How Machine Learning is Revolutionizing Deal Cycles",
            "content": "New research shows AI-powered sales tools can reduce deal cycles by up to 28% while increasing conversion rates.",
            "dateAdded": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(),
            "tags": ["AI", "Sales", "Technology"]
        },
        {
            "id": 2,
            "title": "Gartner Releases 2025 Sales Technology Magic Quadrant",
            "content": "The latest report shows shifting leadership in sales enablement platforms with an emphasis on integration capabilities.",
            "dateAdded": (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat(),
            "tags": ["Gartner", "Research", "Sales Tech"]
        },
        {
            "id": 3,
            "title": "Top 5 Messaging Strategies for Technical Buyers",
            "content": "New study reveals that technical decision makers respond better to specific value propositions backed by implementation details.",
            "dateAdded": (datetime.datetime.now() - datetime.timedelta(days=8)).isoformat(),
            "tags": ["Messaging", "Technical Sales", "Strategy"]
        },
        {
            "id": 4,
            "title": "Remote Selling Strategies Remain Crucial as Hybrid Work Models Persist",
            "content": "Despite return-to-office mandates, 67% of B2B buying processes still involve significant remote interaction components.",
            "dateAdded": (datetime.datetime.now() - datetime.timedelta(days=12)).isoformat(),
            "tags": ["Remote Selling", "Hybrid Work", "Sales Process"]
        },
        {
            "id": 5,
            "title": "Enterprise Software Spending Expected to Grow 14% in 2025",
            "content": "Forrester predicts accelerated investment in security, AI, and collaboration tools as digital transformation initiatives expand.",
            "dateAdded": (datetime.datetime.now() - datetime.timedelta(days=15)).isoformat(),
            "tags": ["Market Trends", "Budget", "Enterprise"]
        },
        {
            "id": 6,
            "title": "New Research Shows Personalized Outreach Improves Connection Rates by 35%",
            "content": "Study of over 10,000 sales interactions demonstrates the significant impact of customized messaging on initial engagement.",
            "dateAdded": (datetime.datetime.now() - datetime.timedelta(days=18)).isoformat(),
            "tags": ["Personalization", "Outreach", "Engagement"]
        }
    ]
    return jsonify(library_items)

if __name__ == '__main__':
    print("Starting simple Flask server on http://127.0.0.1:5005")
    app.run(debug=True, port=5005)
