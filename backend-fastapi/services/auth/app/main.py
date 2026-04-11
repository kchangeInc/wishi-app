from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client import OAuthError
import jwt
from datetime import datetime, timedelta
import psycopg2
import secrets
from shared.auth import create_token, verify_token
from shared.db.connection import get_db_connection

app = FastAPI()

# Database connection
conn = get_db_connection()

# JWT settings
SECRET_KEY = "your-secret-key-change-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# OAuth setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id="GOOGLE_CLIENT_ID",
    client_secret="GOOGLE_CLIENT_SECRET",
    server_metadata_url="https://accounts.google.com/.well-known/openid_configuration",
    client_kwargs={"scope": "openid email profile"},
)

security = HTTPBearer()

class TokenRequest(BaseModel):
    grant_type: str
    code: str | None = None
    refresh_token: str | None = None
    redirect_uri: str | None = None
    code_verifier: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: str | None = None

class UserInfo(BaseModel):
    id: int
    email: str
    name: str | None = None
    display_name: str | None = None
    google_id: str | None = None
    role: str = "buyer"
    is_active: bool = True
    is_deleted: bool = False
    last_login_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    created_by: int | None = None
    updated_by: int | None = None
    version: int = 1

def _ensure_tables():
    # Tables are now managed by Alembic migrations
    pass

@app.on_event("startup")
def startup():
    _ensure_tables()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    user_id = data.get("sub")
    email = data.get("email")
    return create_token(user_id, email), datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id: int):
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
            (user_id, token, expires_at)
        )
        conn.commit()
    return token

def verify_access_token(token: str):
    try:
        return verify_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_access_token(credentials.credentials)
    user_id = payload.get("sub")
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, email, name, display_name, google_id, role, is_active, is_deleted,
                   last_login_at, created_at, updated_at, created_by, updated_by, version
            FROM users WHERE id = %s AND is_deleted = FALSE
        """, (user_id,))
        row = cur.fetchone()
    if not row or not row[6]:  # is_active
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return UserInfo(
        id=row[0], email=row[1], name=row[2], display_name=row[3], google_id=row[4],
        role=row[5], is_active=row[6], is_deleted=row[7], last_login_at=row[8],
        created_at=row[9], updated_at=row[10], created_by=row[11], updated_by=row[12], version=row[13]
    )

@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=error.error)

    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="No user info")

    # Upsert user with enhanced fields
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (email, name, display_name, google_id, role, is_active, last_login_at, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 'buyer', TRUE, NOW(), NOW(), NOW())
            ON CONFLICT (google_id) DO UPDATE SET
                name = EXCLUDED.name,
                display_name = EXCLUDED.display_name,
                last_login_at = NOW(),
                updated_at = NOW()
            RETURNING id
        """, (user_info['email'], user_info.get('name'), user_info.get('name'), user_info['sub']))
        user_id = cur.fetchone()[0]
        conn.commit()

    # Create tokens
    access_token, expire = create_access_token({"sub": user_id, "email": user_info['email']})
    refresh_token = create_refresh_token(user_id)

    return TokenResponse(
        access_token=access_token,
        expires_in=int((expire - datetime.utcnow()).total_seconds()),
        refresh_token=refresh_token
    )

@app.post("/token", response_model=TokenResponse)
def token_endpoint(request: TokenRequest):
    if request.grant_type == "authorization_code":
        # Handle auth code flow (simplified, in prod use PKCE)
        # For now, assume code is handled in callback
        raise HTTPException(status_code=400, detail="Use /callback for auth code")

    elif request.grant_type == "refresh_token":
        if not request.refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token required")

        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, expires_at, revoked FROM refresh_tokens WHERE token = %s",
                (request.refresh_token,)
            )
            row = cur.fetchone()
        if not row or row[2] or datetime.utcnow() > row[1]:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = row[0]
        with conn.cursor() as cur:
            cur.execute("""
                SELECT email, name, display_name FROM users
                WHERE id = %s AND is_deleted = FALSE AND is_active = TRUE
            """, (user_id,))
            user_row = cur.fetchone()
        if not user_row:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        email = user_row[0]

        # Revoke old refresh token
        with conn.cursor() as cur:
            cur.execute("UPDATE refresh_tokens SET revoked = TRUE WHERE token = %s", (request.refresh_token,))
            conn.commit()

        # Issue new tokens
        access_token, expire = create_access_token({"sub": user_id, "email": email})
        refresh_token = create_refresh_token(user_id)

        return TokenResponse(
            access_token=access_token,
            expires_in=int((expire - datetime.utcnow()).total_seconds()),
            refresh_token=refresh_token
        )

    else:
        raise HTTPException(status_code=400, detail="Unsupported grant_type")

@app.get("/validate")
def validate_token(current_user: UserInfo = Depends(get_current_user)):
    return {"valid": True, "user": current_user}

@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_access_token(credentials.credentials)
    user_id = payload.get("sub")
    with conn.cursor() as cur:
        cur.execute("UPDATE refresh_tokens SET revoked = TRUE WHERE user_id = %s", (user_id,))
        conn.commit()
    return {"message": "Logged out"}

@app.get("/me", response_model=UserInfo)
def get_me(current_user: UserInfo = Depends(get_current_user)):
    return current_user

@app.get("/health")
def health():
    return {"status": "auth ok"}
