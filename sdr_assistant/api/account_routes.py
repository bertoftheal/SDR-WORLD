"""
API routes for account management functionality.
"""
from flask import Blueprint, jsonify, request
from typing import Dict, Any

from ..core.auth import auth_manager
from ..core.accounts import account_manager


accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/accounts", methods=["GET"])
@accounts_bp.route("/accounts/list", methods=["GET"])
def get_accounts():
    """
    API Route: Retrieve accounts
    
    Fetches accounts from Airtable or returns mock account data.
    
    Returns:
        JSON array of accounts with 'id' and 'name' properties
    """
    accounts = account_manager.get_accounts()
    
    # Convert to simple format with just id and name
    account_list = [{"id": account.id, "name": account.name} for account in accounts]
    
    return jsonify(account_list)


@accounts_bp.route("/accounts/details", methods=["GET"])
def get_account_details():
    """
    API Route: Get detailed account information
    
    Returns accounts with additional details like industry, employees, and location.
    
    Returns:
        JSON array of account objects with detailed information
    """
    accounts = account_manager.get_accounts()
    
    # Convert to detailed format
    account_details = [account.to_dict() for account in accounts]
    
    return jsonify(account_details)
