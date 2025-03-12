"""
API routes for authentication functionality.
"""
from flask import Blueprint, request, jsonify
from typing import Dict, Any

from ..core.auth import auth_manager


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    API Route: User login
    
    Authenticates a user and returns a JWT token if credentials are valid.
    
    Returns:
        JSON with success status, token if successful, and error message if not
    """
    data = request.json
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400
    
    user = auth_manager.authenticate_user(email, password)
    
    if not user:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401
    
    token = auth_manager.generate_token(user["id"])
    
    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
    })


@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    """
    API Route: Get current user
    
    Returns the current user based on the JWT token in the request headers.
    
    Returns:
        JSON with user information or error message
    """
    user = auth_manager.get_current_user(request.headers)
    
    if not user:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
    })
