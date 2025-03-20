"""
API routes for knowledge library functionality.
"""
from flask import Blueprint, jsonify, request
from typing import Dict, Any
from datetime import datetime
import uuid

from ..core.auth import auth_manager


# Mock library entries database - in production this would be in a real database
LIBRARY_ENTRIES = [
    {
        'id': '1',
        'title': "Anthropic's Hybrid Reasoning AI Model: Claude 3.7 Sonnet",
        'content': "Anthropic has introduced Claude 3.7 Sonnet, a 'hybrid reasoning model' that excels in solving complex problems, particularly in mathematics and coding. This model integrates both instinctive outputs and in-depth reasoning, allowing users to adjust the level of reasoning based on their needs. Claude 3.7 Sonnet is accessible via the Claude app, Anthropic's API, Amazon Bedrock, and Google's Vertex AI, maintaining the same operational cost as its predecessor.",
        'category': 'News',
        'dateAdded': '2025-03-17T09:30:00Z',
        'userId': '1',
        'tags': ['AI', 'Anthropic', 'Claude', 'Hybrid Reasoning']
    },
    {
        'id': '2',
        'title': "Emergence of 'Vibe Coding'",
        'content': "A new trend termed 'vibe coding,' introduced by Andrej Karpathy, co-founder of OpenAI, is gaining traction in Silicon Valley. This approach leverages AI to write code based on simple user instructions, minimizing direct coding efforts. Tools like OpenAI's Composer and Anthropic's AI models facilitate this process, enabling efficient software development with minimal manual input. Industry leaders anticipate significant shifts in software engineering due to this methodology.",
        'category': 'News',
        'dateAdded': '2025-03-15T14:15:00Z',
        'userId': '1',
        'tags': ['AI', 'Coding', 'OpenAI', 'Vibe Coding']
    },
    {
        'id': '3',
        'title': "OpenAI's New Developer Tools Amidst Rising Competition",
        'content': "OpenAI has launched new developer tools called the Responses API to aid in building advanced AI agents capable of executing complex tasks without direct human intervention. This tool replaces the Assistants API and is free for developers, with a phase-out of the old API expected by mid-2026. The launch comes amid increasing competition from Chinese AI startups, notably Monica, which recently introduced an AI agent named Manus, claiming it surpasses OpenAI's DeepResearch agent.",
        'category': 'News',
        'dateAdded': '2025-03-14T11:45:00Z',
        'userId': '1',
        'tags': ['AI', 'OpenAI', 'Developer Tools', 'Competition']
    },
    {
        'id': '4',
        'title': "AI's Growing Role in Software Development",
        'content': "Dario Amodei, CEO of Anthropic, predicts that AI could be writing 90% of software code within 3 to 6 months, potentially leading to AI generating all code in a year. While software developers will still be needed for design inputs initially, Amodei emphasizes the broader implications of AI across various industries. This prediction aligns with observations that many startup founders are already heavily relying on AI for coding.",
        'category': 'News',
        'dateAdded': '2025-03-12T16:20:00Z',
        'userId': '1',
        'tags': ['AI', 'Software Development', 'Anthropic', 'Future of Coding']
    },
    {
        'id': '5',
        'title': "Market Growth Projections for AI Coding Assistants",
        'content': "The global generative AI coding assistants market size was estimated at USD 18.6 million in 2023 and is projected to grow at a compound annual growth rate (CAGR) of 25.8% from 2024 to 2030, reaching USD 92.5 million by 2030. This growth reflects the increasing adoption and reliance on AI-driven coding solutions in the software development industry.",
        'category': 'News',
        'dateAdded': '2025-03-10T10:00:00Z',
        'userId': '1',
        'tags': ['AI', 'Market Growth', 'Coding Assistants', 'Industry Forecast']
    }
]


library_bp = Blueprint("library", __name__)


@library_bp.route("/library", methods=["GET"])
def get_library_entries():
    """
    API Route: Get knowledge library entries
    
    Returns saved insights and research from the knowledge library.
    
    Returns:
        JSON array of library entry objects
    """
    return jsonify(LIBRARY_ENTRIES)


@library_bp.route("/library/add", methods=["POST"])
def add_library_entry():
    """
    API Route: Add an entry to the knowledge library
    
    Saves a new insight or piece of research to the knowledge library.
    
    Returns:
        JSON with success status and the newly created entry
    """
    data = request.json
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
        
    # Get current user
    user = auth_manager.get_current_user(request.headers)
    
    if not user:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
        
    # Validate required fields
    required_fields = ['title', 'content', 'category', 'tags']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'{field} is required'}), 400
            
    # Create new library entry
    new_entry = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'content': data['content'],
        'category': data['category'],
        'tags': data['tags'],
        'dateAdded': datetime.utcnow().isoformat() + 'Z',
        'userId': user['id']
    }
    
    # Add to our mock database
    LIBRARY_ENTRIES.append(new_entry)
    
    return jsonify({
        'success': True,
        'message': 'Library entry added successfully',
        'entry': new_entry
    })
