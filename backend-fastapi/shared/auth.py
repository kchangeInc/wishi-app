# shared/auth.py
import jwt
import os
from datetime import datetime, timedelta

SECRET = os.getenv("SECRET_KEY", "CHANGE_THIS_TO_ENV")
ALGORITHM = "HS256"

def create_token(user_id, email=None):
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iat": datetime.utcnow(),
        "iss": "wishi-auth"
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def verify_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")