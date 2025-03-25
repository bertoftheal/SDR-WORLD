"""
API routes for company metadata retrieval.
"""
from flask import Blueprint, jsonify, request

from ..services.metadata_service import metadata_service

metadata_bp = Blueprint("metadata", __name__)

@metadata_bp.route("/company-metadata", methods=["POST"])
def get_company_metadata():
    """
    API Route: Get Company Metadata
    
    Retrieves structured company metadata using the Perplexity API.
    
    Returns:
        JSON with company metadata (headquarters, employees, founded, market_cap, description)
    """
    # Add detailed request logging
    print(f"Received metadata request from: {request.remote_addr}")
    
    data = request.json
    
    if not data:
        print("Metadata request received with no data")
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    company_name = data.get("companyName")
    
    if not company_name:
        print("Metadata request missing company name")
        return jsonify({"success": False, "message": "Company name is required"}), 400
    
    print(f"Fetching metadata for company: {company_name}")
    
    try:
        # Get metadata from service
        metadata = metadata_service.get_company_metadata(company_name)
        
        # Log the results (excluding potentially sensitive data)
        print(f"Successfully retrieved metadata for {company_name} with fields: {', '.join(metadata.keys())}")
        
        return jsonify({
            "success": True,
            "metadata": metadata
        })
    except Exception as e:
        print(f"Error retrieving metadata for {company_name}: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error retrieving company metadata: {str(e)}"
        }), 500
