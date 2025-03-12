"""
Core authentication functionality for SDR Assistant.
Handles user authentication and token generation/verification.
"""
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union

from ..config.settings import settings


class AuthManager:
    """Manager for authentication operations."""
    
    def __init__(self):
        """Initialize the authentication manager."""
        self.secret_key = settings.JWT_SECRET_KEY
        self.expiration = settings.JWT_EXPIRATION
        
        # Mock users database for demonstration
        # In a production environment, this would be a database
        self._users = {
            "demo@codeium.com": {
                "id": "user1",
                "email": "demo@codeium.com",
                "name": "Demo User",
                "password_hash": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            }
        }
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by email and password.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            User object if authentication is successful, None otherwise
        """
        user = self._users.get(email)
        if not user:
            return None
            
        password_matches = bcrypt.checkpw(
            password.encode('utf-8'),
            user["password_hash"].encode('utf-8')
        )
        
        if not password_matches:
            return None
            
        return {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
    
    def generate_token(self, user_id: str) -> str:
        """
        Generate a JWT token for a user.
        
        Args:
            user_id: ID of the user
            
        Returns:
            JWT token
        """
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=self.expiration)
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify a JWT token and return the user ID if valid.
        
        Args:
            token: JWT token to verify
            
        Returns:
            User ID if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload["sub"]
        except jwt.PyJWTError:
            return None
    
    def get_current_user(self, headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Get the current user from request headers.
        
        Args:
            headers: HTTP request headers
            
        Returns:
            User object if token is valid, None otherwise
        """
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
            
        token = auth_header.split("Bearer ")[1]
        user_id = self.verify_token(token)
        
        if not user_id:
            return None
            
        # Find user by ID
        for user in self._users.values():
            if user["id"] == user_id:
                return {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"]
                }
                
        return None


# Singleton instance for easy import
auth_manager = AuthManager()
