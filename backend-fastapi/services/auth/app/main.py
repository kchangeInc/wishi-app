from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt as pyjwt
import os
import secrets
import logging
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from shared.auth import create_token, verify_token
from shared.db.session import get_db_session, SessionLocal
from shared.repository.user import UserRepository
from shared.log_config import setup_logging, add_logging_middleware

setup_logging("auth")
logger = logging.getLogger(__name__)

app = FastAPI()
add_logging_middleware(app)

# Settings from env
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_TO_ENV")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

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
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        refresh = repo.create_refresh_token(user.id, REFRESH_TOKEN_EXPIRE_DAYS)
    finally:
        db.close()

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
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_active_user(user_id)
    finally:
        db.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

# ---- endpoints ----

@app.post("/google-token", response_model=TokenResponse)
def google_token_login(body: GoogleTokenRequest):
    """Frontend-initiated: verify Google ID token, upsert user, return JWT"""
    try:
        idinfo = google_id_token.verify_oauth2_token(
            body.id_token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
    except Exception:
        logger.warning("Google token verification failed", exc_info=True)
        raise HTTPException(status_code=401, detail="Invalid Google ID token")

    email = idinfo.get("email")
    google_id = idinfo.get("sub")
    name = idinfo.get("name")
    avatar = idinfo.get("picture")

    if not email:
        raise HTTPException(status_code=400, detail="Email not available from Google")

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.create_or_update_google_user(email, google_id, name)
        if avatar and not user.avatar_url:
            repo.update_user(user.id, avatar_url=avatar)
            db.refresh(user)
    finally:
        db.close()

    return _issue_tokens(user)

@app.post("/login", response_model=TokenResponse)
def email_password_login(body: EmailLoginRequest):
    """Login with email and password (for pre-seeded company/demo users)"""
    logger.info(f"Email login attempt: email={body.email}")
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.verify_password_login(body.email, body.password)
        if not user:
            logger.warning(f"Failed email login: email={body.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
    finally:
        db.close()

    return _issue_tokens(user)

@app.post("/token", response_model=TokenResponse)
def token_endpoint(request: TokenRequest):
    if request.grant_type != "refresh_token":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")
    if not request.refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user_id = repo.validate_refresh_token(request.refresh_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        repo.revoke_refresh_token(request.refresh_token, user_id)
        user = repo.get_active_user(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found or inactive")
    finally:
        db.close()

    return _issue_tokens(user)

@app.get("/validate")
def validate_token(current_user=Depends(get_current_user)):
    return {"valid": True, "user": _user_to_dict(current_user)}

@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = verify_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    user_id = payload.get("sub")
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        repo.revoke_all_user_tokens(user_id)
    finally:
        db.close()
    logger.info(f"User logout: user_id={user_id}")
    return {"message": "Logged out"}

@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return _user_to_dict(current_user)

@app.put("/me")
def update_me(body: ProfileUpdate, current_user=Depends(get_current_user)):
    updates = body.dict(exclude_unset=True)
    if not updates:
        return _user_to_dict(current_user)
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.update_user(current_user.id, **updates)
    finally:
        db.close()
    return _user_to_dict(user)

@app.get("/health")
def health():
    return {"status": "auth ok"}
