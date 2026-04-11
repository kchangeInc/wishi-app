# shared/user.py
from fastapi import Request, HTTPException

def get_current_user(request: Request) -> dict:
    """Extract user info from request headers (set by gateway)"""
    user_id_str = request.headers.get("X-User-ID")
    user_email = request.headers.get("X-User-Email")
    
    if not user_id_str or not user_email:
        raise HTTPException(status_code=401, detail="User info not found in headers")
    
    try:
        return {
            "user_id": int(user_id_str),
            "email": user_email
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user info in headers")

def get_optional_user(request: Request) -> dict | None:
    """Extract user info from request headers (optional)"""
    user_id_str = request.headers.get("X-User-ID")
    user_email = request.headers.get("X-User-Email")
    
    if not user_id_str or not user_email:
        return None
    
    try:
        return {
            "user_id": int(user_id_str),
            "email": user_email
        }
    except ValueError:
        return None
