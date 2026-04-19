from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt as pyjwt
import secrets
import logging
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from shared.auth import create_token, verify_token
from shared.config.settings import get_settings
from shared.db.dependencies import get_db, get_repos
from shared.repository.factory import RepositoryFactory, create_repos
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("auth")
logger = logging.getLogger(__name__)
settings = get_settings()

# Ensure Firebase Admin SDK is initialized (needed for verify_id_token)
if not firebase_admin._apps:
    fs = settings.firestore
    if fs.credentials_path:
        cred = credentials.Certificate(fs.credentials_path)
        firebase_admin.initialize_app(cred, {"projectId": fs.project_id})
    else:
        firebase_admin.initialize_app(options={"projectId": fs.project_id})

app = FastAPI()
add_logging_middleware(app)

# Settings from env
SECRET_KEY = settings.auth.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.auth.refresh_token_expire_days
GOOGLE_CLIENT_ID = settings.auth.google_client_id

security = HTTPBearer()

# ---- Pydantic models ----

class GoogleTokenRequest(BaseModel):
    id_token: str

class EmailLoginRequest(BaseModel):
    email: str
    password: str

class TokenRequest(BaseModel):
    grant_type: str
    refresh_token: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    user: Optional[dict] = None

class UserInfo(BaseModel):
    id: int
    email: str
    name: Optional[str] = None
    display_name: Optional[str] = None
    google_id: Optional[str] = None
    role: str = "buyer"
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None

# ---- helpers ----

def _user_to_dict(user) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "display_name": user.display_name,
        "google_id": user.google_id,
        "role": user.role,
        "phone": user.phone,
        "location": user.location,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "website": user.website,
        "instagram": user.instagram,
        "twitter": user.twitter,
        "is_active": user.is_active,
        "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }

def _issue_tokens(user) -> TokenResponse:
    access_token = create_token(user.id, user.email, user.role or "buyer")
    with create_repos() as repos:
        repo = repos.user()
        refresh = repo.create_refresh_token(user.id, REFRESH_TOKEN_EXPIRE_DAYS)
    logger.info(f"Tokens issued for user_id={user.id} email={user.email}")
    return TokenResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        refresh_token=refresh,
        user=_user_to_dict(user),
    )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    user_id = payload.get("sub")
    with create_repos() as repos:
        repo = repos.user()
        user = repo.get_active_user(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

# ---- endpoints ----

@app.post("/google-token", response_model=TokenResponse)
def google_token_login(body: GoogleTokenRequest, repos: RepositoryFactory = Depends(get_repos)):
    """Frontend-initiated: verify Firebase ID token, upsert user, return JWT"""
    try:
        decoded = firebase_auth.verify_id_token(body.id_token)
    except Exception:
        logger.warning("Firebase ID token verification failed", exc_info=True)
        raise HTTPException(status_code=401, detail="Invalid Firebase ID token")

    email = decoded.get("email")
    google_id = decoded.get("uid")
    name = decoded.get("name")
    avatar = decoded.get("picture")

    if not email:
        raise HTTPException(status_code=400, detail="Email not available from token")

    repo = repos.user()
    user = repo.create_or_update_google_user(email, google_id, name)
    if avatar and not user.avatar_url:
        repo.update_user(user.id, avatar_url=avatar)

    return _issue_tokens(user)

@app.post("/login", response_model=TokenResponse)
def email_password_login(body: EmailLoginRequest, repos: RepositoryFactory = Depends(get_repos)):
    """Login with email and password (for pre-seeded company/demo users)"""
    logger.info(f"Email login attempt: email={body.email}")
    repo = repos.user()
    user = repo.verify_password_login(body.email, body.password)
    if not user:
        logger.warning(f"Failed email login: email={body.email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return _issue_tokens(user)

@app.post("/token", response_model=TokenResponse)
def token_endpoint(request: TokenRequest, repos: RepositoryFactory = Depends(get_repos)):
    if request.grant_type != "refresh_token":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")
    if not request.refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    repo = repos.user()
    user_id = repo.validate_refresh_token(request.refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    repo.revoke_refresh_token(request.refresh_token, user_id)
    user = repo.get_active_user(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return _issue_tokens(user)

@app.get("/validate")
def validate_token(current_user=Depends(get_current_user)):
    return {"valid": True, "user": _user_to_dict(current_user)}

@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security), repos: RepositoryFactory = Depends(get_repos)):
    try:
        payload = verify_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    user_id = payload.get("sub")
    repo = repos.user()
    repo.revoke_all_user_tokens(user_id)
    logger.info(f"User logout: user_id={user_id}")
    return {"message": "Logged out"}

@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return _user_to_dict(current_user)

@app.put("/me")
def update_me(body: ProfileUpdate, current_user=Depends(get_current_user), repos: RepositoryFactory = Depends(get_repos)):
    updates = body.model_dump(exclude_unset=True)
    if not updates:
        return _user_to_dict(current_user)
    repo = repos.user()
    user = repo.update_user(current_user.id, **updates)
    return _user_to_dict(user)

@app.get("/health")
def health():
    return {"status": "auth ok"}
