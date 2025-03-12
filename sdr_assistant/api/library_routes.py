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
