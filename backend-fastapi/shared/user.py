from __future__ import annotations
# shared/user.py
from fastapi import Request, HTTPException
import logging

logger = logging.getLogger(__name__)

def get_current_user(request: Request) -> dict:
    """Extract user info from request headers (set by gateway)"""
    user_id_str = request.headers.get("X-User-ID")
    user_email = request.headers.get("X-User-Email")
    user_role = request.headers.get("X-User-Role", "buyer")

    if not user_id_str or not user_email:
        logger.warning("Auth headers missing from request")
        raise HTTPException(status_code=401, detail="User info not found in headers")

    try:
        return {
            "user_id": int(user_id_str),
            "email": user_email,
            "role": user_role,
        }
    except ValueError:
        logger.warning(f"Invalid user ID in header: {user_id_str}")
        raise HTTPException(status_code=401, detail="Invalid user info in headers")

def get_optional_user(request: Request) -> dict | None:
    """Extract user info from request headers (optional)"""
    user_id_str = request.headers.get("X-User-ID")
    user_email = request.headers.get("X-User-Email")
    user_role = request.headers.get("X-User-Role", "buyer")

    if not user_id_str or not user_email:
        return None

    try:
        return {
            "user_id": int(user_id_str),
            "email": user_email,
            "role": user_role,
        }
    except ValueError:
        return None

def require_role(*allowed_roles):
    """Dependency that ensures the caller has one of the allowed roles"""
    def _check(request: Request):
        user = get_current_user(request)
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _check
