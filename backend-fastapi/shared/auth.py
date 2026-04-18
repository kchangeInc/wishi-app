# shared/auth.py
import jwt
import os
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

SECRET = os.getenv("SECRET_KEY", "CHANGE_THIS_TO_ENV")
ALGORITHM = "HS256"

def create_token(user_id, email=None, role="buyer"):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": now + timedelta(minutes=30),
        "iat": now,
        "iss": "wishi-auth"
    }
    logger.debug(f"Token created for user_id={user_id} role={role}")
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.warning("Token verification failed: expired")
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Token verification failed: invalid")
        raise ValueError("Invalid token")
