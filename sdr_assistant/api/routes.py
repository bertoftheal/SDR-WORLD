"""
Central router that registers all API routes.
"""
from flask import Blueprint, jsonify, request, send_from_directory, current_app
import os

from .auth_routes import auth_bp
from .account_routes import accounts_bp
from .research_routes import research_bp
from .library_routes import library_bp


# Create main API blueprint
api_bp = Blueprint("api", __name__)

# We're not using nested blueprints as they're causing endpoint issues
# All blueprints already have /api prefix


# Base API route for testing
@api_bp.route("/", methods=["GET"])
def api_root():
    """
    Base API route for testing connectivity.
    """
    return jsonify({
        "name": "SDR Assistant API",
        "status": "operational",
        "version": "1.0.0"
    })


def register_routes(app):
    """
    Register all routes with the Flask application.
    
    Args:
        app: Flask application instance
    """
    # Register all API routes with /api prefix
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(accounts_bp, url_prefix='/api')
    app.register_blueprint(research_bp, url_prefix='/api')
    app.register_blueprint(library_bp, url_prefix='/api')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Serve static files and HTML pages directly from static directory
    @app.route('/')
    def serve_index():
        return send_from_directory('static', 'index.html')
    
    @app.route('/accounts.html')
    def serve_accounts():
        return send_from_directory('static', 'accounts.html')
        
    @app.route('/library.html')
    def serve_library():
        return send_from_directory('static', 'library.html')
        
    @app.route('/login.html')
    def serve_login():
        return send_from_directory('static', 'login.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)
