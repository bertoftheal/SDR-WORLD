"""
API routes for research generation and management.
"""
from flask import Blueprint, jsonify, request
from typing import Dict, Any

from ..core.auth import auth_manager
from ..core.research import research_manager


research_bp = Blueprint("research", __name__)


@research_bp.route("/generate-research", methods=["POST"])
def generate_research():
    """
    API Route: Generate Research
    
    Accepts a POST request with an account name and generates insights and a talk track.
    
    Returns:
        JSON with industry insights, company insights, vision insights, and recommended talk track
    """
    data = request.json
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    account_name = data.get("accountName")
    
    if not account_name:
        return jsonify({"success": False, "message": "Account name is required"}), 400
    
    result = research_manager.generate_research(account_name)
    
    if not result["success"]:
        return jsonify(result), 400
    
    return jsonify(result)


@research_bp.route("/save-research", methods=["POST"])
def save_research():
    """
    API Route: Save research to database
    
    Saves the generated insights and talk track for a specific account.
    The data is stored in Supabase, with Airtable as a fallback.
    
    Returns:
        JSON with success status and message
    """
    data = request.json
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    required_fields = ["accountId", "accountName", "industryInsights", 
                      "companyInsights", "visionInsights", "recommendedTalkTrack"]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Field '{field}' is required"}), 400
    
    # Get current user if authenticated
    user = auth_manager.get_current_user(request.headers)
    user_id = user["id"] if user else None
    
    result = research_manager.save_research(data, user_id)
    
    return jsonify(result)
