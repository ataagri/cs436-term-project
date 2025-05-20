import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Path to service account credentials
# Note: Replace with the path to your Firebase service account JSON file
# or use environment variables/Kubernetes secrets
SERVICE_ACCOUNT_PATH = "firebase-service-account.json"

# Initialize Firebase Admin SDK
# This will be initialized when the module is imported
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
except ValueError:
    # The app might already be initialized
    pass
except FileNotFoundError:
    print("Firebase service account file not found. Authentication will not work.")
    # In production, you might want to fail loudly here with an exception

# HTTP Bearer security scheme for FastAPI
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify the Firebase ID token passed in the Authorization header.
    
    This function can be used as a FastAPI dependency to protect routes.
    Example: @app.get("/protected", dependencies=[Depends(verify_token)])
    
    Returns:
        dict: The decoded token payload with user information
    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token_data: dict = Depends(verify_token)):
    """
    Extract and return the user ID from the token data.
    
    This function can be used as a FastAPI dependency to get the current user's ID.
    Example: @app.get("/me", response_model=User)
    def read_users_me(current_user: str = Depends(get_current_user)):
        return {"user_id": current_user}
    
    Args:
        token_data: The decoded token from verify_token
    
    Returns:
        str: The user ID from the token
    """
    return token_data["uid"]

# Optional: Helper functions

def create_custom_token(uid, additional_claims=None):
    """
    Create a custom Firebase token for a user.
    
    This is typically used for server-to-server authentication
    or for testing authentication in development.
    
    Args:
        uid: The user ID to create a token for
        additional_claims: Additional claims to include in the token
        
    Returns:
        str: A custom token that can be used to sign in to Firebase
    """
    return auth.create_custom_token(uid, additional_claims)

def revoke_refresh_tokens(uid):
    """
    Revoke all refresh tokens for a user.
    
    This is useful when you need to force a user to re-authenticate,
    such as after a password change or when suspicious activity is detected.
    
    Args:
        uid: The user ID to revoke tokens for
    """
    auth.revoke_refresh_tokens(uid)