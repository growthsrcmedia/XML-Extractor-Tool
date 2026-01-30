"""
Firebase Authentication Module

Handles Firebase Admin SDK initialization and token verification.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
from typing import Optional, Dict

# Load environment variables
load_dotenv()


def get_mode() -> str:
    """
    Get the current application mode from environment.
    
    Returns:
        'development' or 'production'
    """
    return os.getenv("MODE", "development").lower()


def is_production() -> bool:
    """Check if app is running in production mode."""
    return get_mode() == "production"


def is_development() -> bool:
    """Check if app is running in development mode."""
    return get_mode() == "development"


def initialize_firebase() -> None:
    """
    Initialize Firebase Admin SDK with credentials from environment variables.
    Only initializes once to prevent duplicate app errors.
    Only initializes in production mode.
    """
    # Skip Firebase initialization in development mode
    if is_development():
        print("ℹ️ Running in DEVELOPMENT mode - Firebase authentication disabled")
        return
    
    if not firebase_admin._apps:
        try:
            # Build the credentials dictionary from environment variables
            firebase_creds = {
                "type": os.getenv("FIREBASE_TYPE"),
                "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
                "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
                "universe_domain": os.getenv("UNIVERSE_DOAMIN", "googleapis.com")
            }
            
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
            
            print("✅ Firebase Admin SDK initialized successfully (PRODUCTION mode)")
        except Exception as e:
            print(f"❌ Error initializing Firebase: {str(e)}")
            raise
    else:
        print("ℹ️ Firebase Admin SDK already initialized")


def verify_token(id_token: str) -> Optional[Dict]:
    """
    Verify Firebase ID token and return decoded user information.
    In development mode, returns a mock user.
    
    Args:
        id_token: The Firebase ID token to verify
        
    Returns:
        Dictionary containing user information if token is valid, None otherwise.
        User info includes: uid, email, name, picture, etc.
    """
    # In development mode, return mock user
    if is_development():
        return {
            "uid": "dev-user-123",
            "email": "developer@localhost.dev",
            "email_verified": True,
            "name": "Development User",
            "picture": None,
            "mode": "development"
        }
    
    # Production mode - verify token
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        
        # Extract user information
        user_info = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
            "auth_time": decoded_token.get("auth_time"),
            "exp": decoded_token.get("exp"),
            "firebase": decoded_token.get("firebase", {}),
            "mode": "production"
        }
        
        return user_info
    except auth.InvalidIdTokenError:
        print("❌ Invalid ID token")
        return None
    except auth.ExpiredIdTokenError:
        print("❌ Token has expired")
        return None
    except auth.RevokedIdTokenError:
        print("❌ Token has been revoked")
        return None
    except Exception as e:
        print(f"❌ Error verifying token: {str(e)}")
        return None


def get_user_by_uid(uid: str) -> Optional[Dict]:
    """
    Get additional user information from Firebase by UID.
    In development mode, returns mock user data.
    
    Args:
        uid: The Firebase user ID
        
    Returns:
        Dictionary containing user information if found, None otherwise
    """
    # In development mode, return mock data
    if is_development():
        return {
            "uid": uid,
            "email": "developer@localhost.dev",
            "email_verified": True,
            "display_name": "Development User",
            "photo_url": None,
            "disabled": False,
            "mode": "development"
        }
    
    # Production mode - fetch from Firebase
    try:
        user = auth.get_user(uid)
        
        user_info = {
            "uid": user.uid,
            "email": user.email,
            "email_verified": user.email_verified,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "disabled": user.disabled,
            "created_at": user.user_metadata.creation_timestamp,
            "last_sign_in": user.user_metadata.last_sign_in_timestamp,
            "provider_data": [
                {
                    "provider_id": provider.provider_id,
                    "uid": provider.uid,
                    "email": provider.email,
                    "display_name": provider.display_name,
                    "photo_url": provider.photo_url
                }
                for provider in user.provider_data
            ],
            "mode": "production"
        }
        
        return user_info
    except Exception as e:
        print(f"❌ Error fetching user: {str(e)}")
        return None


# Initialize Firebase when module is imported
initialize_firebase()
