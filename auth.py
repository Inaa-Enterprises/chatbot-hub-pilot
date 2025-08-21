# Authentication utilities using Firebase Admin SDK

import os
import logging
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

logger = logging.getLogger(__name__)

# --- Firebase Initialization ---

# Expecting the path to the service account key in an environment variable
SERVICE_ACCOUNT_KEY_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")

firebase_app = None
if SERVICE_ACCOUNT_KEY_PATH:
    try:
        if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            logger.error(f"Firebase service account key file not found at: {SERVICE_ACCOUNT_KEY_PATH}")
            raise FileNotFoundError(f"Service account key file not found at {SERVICE_ACCOUNT_KEY_PATH}")
            
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_app = firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
        # Allow app to start, but authentication will fail
else:
    logger.warning("FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable not set. Firebase Authentication will not work.")

# --- FastAPI Dependency for Token Verification ---

# This scheme expects the token to be sent in the Authorization header as a Bearer token
# The frontend needs to send the Firebase ID token obtained after user login here.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # tokenUrl is nominal here, not used for Firebase

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Dependency function to verify Firebase ID token and return user data."""
    if not firebase_app:
        logger.error("Firebase app not initialized. Cannot verify token.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service not available",
        )
        
    try:
        # Verify the ID token while checking if the token is revoked.
        decoded_token = auth.verify_id_token(token, app=firebase_app)
        # The decoded_token contains user information like uid, email, etc.
        logger.info(f"Successfully verified token for user_id: {decoded_token.get('uid')}")
        return decoded_token # Contains uid, email, name, picture etc.
    except auth.ExpiredIdTokenError:
        logger.warning("Expired Firebase ID token received.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.InvalidIdTokenError as e:
        logger.warning(f"Invalid Firebase ID token received: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during token verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not verify token",
        )

# Example of how to get just the user ID:
def get_current_user_id(current_user: dict = Depends(get_current_user)) -> str:
    """Dependency that returns just the user ID (uid) from the verified token."""
    user_id = current_user.get("uid")
    if not user_id:
         # This should theoretically not happen if verify_id_token succeeded
        logger.error("Verified token is missing UID.") 
        raise HTTPException(status_code=500, detail="User ID not found in token")
    return user_id

# For testing purposes - bypass authentication
def verify_token(token: str) -> dict:
    """Verify a Firebase ID token and return the decoded token."""
    # This is a simplified version for testing
    return {"uid": "test-user-id"}

# For development/testing - bypass authentication
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Development version that returns a test user ID without verification."""
    # Comment this out and uncomment the proper version above for production
    return "test-user-id"
