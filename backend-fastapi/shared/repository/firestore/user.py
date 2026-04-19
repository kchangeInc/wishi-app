"""Firestore User repository implementation."""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional

from passlib.hash import bcrypt

from shared.dto import UserDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.user import IUserRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> Optional[UserDTO]:
    """Convert a Firestore document dict to UserDTO."""
    if data is None:
        return None
    return UserDTO(
        id=data.get("id"),
        email=data.get("email", ""),
        name=data.get("name"),
        display_name=data.get("display_name"),
        google_id=data.get("google_id"),
        password_hash=data.get("password_hash"),
        role=data.get("role", "buyer"),
        phone=data.get("phone"),
        location=data.get("location"),
        bio=data.get("bio"),
        avatar_url=data.get("avatar_url"),
        website=data.get("website"),
        instagram=data.get("instagram"),
        twitter=data.get("twitter"),
        is_active=data.get("is_active", True),
        is_deleted=data.get("is_deleted", False),
        last_login_at=data.get("last_login_at"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
        created_by=data.get("created_by"),
        updated_by=data.get("updated_by"),
        version=data.get("version", 1),
    )


class FsUserRepository(FsBaseRepository, IUserRepository):
    """Firestore implementation of user repository."""

    def __init__(self, client):
        super().__init__(client, col.USERS)
        self._tokens = client.collection(col.REFRESH_TOKENS)

    # ---- IUserRepository ----

    def get_by_email(self, email: str) -> Optional[UserDTO]:
        data = self._query_one(email=email, is_deleted=False)
        return _to_dto(data)

    def get_by_google_id(self, google_id: str) -> Optional[UserDTO]:
        data = self._query_one(google_id=google_id, is_deleted=False)
        return _to_dto(data)

    def get_active_user(self, id: int) -> Optional[UserDTO]:
        data = self.get_by_id(id)
        if data and not data.get("is_deleted", False) and data.get("is_active", True):
            return _to_dto(data)
        return None

    def verify_password_login(self, email: str, password: str) -> Optional[UserDTO]:
        """Verify email/password credentials. Returns UserDTO or None."""
        # Query for user with email, not deleted, active, and has a password
        query = self.collection
        query = query.where("email", "==", email)
        query = query.where("is_deleted", "==", False)
        query = query.where("is_active", "==", True)
        docs = list(query.limit(1).stream())
        if not docs:
            logger.warning(f"Failed password login: email={email}")
            return None

        data = docs[0].to_dict()
        if not data.get("password_hash"):
            logger.warning(f"Failed password login: email={email}")
            return None

        if not bcrypt.verify(password, data["password_hash"]):
            logger.warning(f"Failed password login: email={email}")
            return None

        # Update last_login_at
        now = datetime.utcnow()
        self.collection.document(str(data["id"])).update({
            "last_login_at": now,
            "updated_at": now,
        })
        data["last_login_at"] = now
        data["updated_at"] = now
        return _to_dto(data)

    def create_or_update_google_user(self, email: str, google_id: str, name: str = None) -> UserDTO:
        """Create new user or update existing Google user."""
        existing = self._query_one(google_id=google_id, is_deleted=False)
        now = datetime.utcnow()

        if existing:
            doc_id = existing["id"]
            updates = {
                "name": name or existing.get("name"),
                "display_name": name or existing.get("display_name"),
                "last_login_at": now,
                "updated_at": now,
            }
            self.collection.document(str(doc_id)).update(updates)
            existing.update(updates)
            logger.info(f"Updated Google user: email={email}")
            return _to_dto(existing)

        # Create new user
        data = self.create(
            email=email,
            name=name,
            display_name=name,
            google_id=google_id,
            role="buyer",
            is_active=True,
            is_deleted=False,
            last_login_at=now,
            created_at=now,
            updated_at=now,
            version=1,
        )
        logger.info(f"New Google user created: email={email}")
        return _to_dto(data)

    def update_user(self, id: int, **kwargs) -> Optional[UserDTO]:
        """Update user fields, incrementing version."""
        data = self.get_by_id(id)
        if not data or data.get("is_deleted") or not data.get("is_active"):
            return None

        kwargs["updated_at"] = datetime.utcnow()
        kwargs["version"] = (data.get("version") or 0) + 1
        # Prevent overwriting protected fields
        kwargs.pop("id", None)
        kwargs.pop("created_at", None)

        self.collection.document(str(id)).update(kwargs)
        data.update(kwargs)
        return _to_dto(data)

    # ---- Refresh token methods ----

    def create_refresh_token(self, user_id: int, expires_days: int = 7) -> str:
        """Create and store a refresh token."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=expires_days)
        now = datetime.utcnow()

        self._tokens.document(token).set({
            "user_id": user_id,
            "token": token,
            "expires_at": expires_at,
            "revoked": False,
            "revoked_at": None,
            "revoked_by": None,
            "created_at": now,
        })
        return token

    def validate_refresh_token(self, token: str) -> Optional[int]:
        """Validate refresh token and return user_id if valid."""
        doc = self._tokens.document(token).get()
        if not doc.exists:
            return None

        data = doc.to_dict()
        if data.get("revoked"):
            return None
        if data.get("expires_at") and data["expires_at"] <= datetime.utcnow():
            return None

        return data.get("user_id")

    def revoke_refresh_token(self, token: str, user_id: int) -> bool:
        """Revoke a single refresh token."""
        doc_ref = self._tokens.document(token)
        doc = doc_ref.get()
        if not doc.exists:
            return False

        doc_ref.update({
            "revoked": True,
            "revoked_at": datetime.utcnow(),
            "revoked_by": user_id,
        })
        return True

    def revoke_all_user_tokens(self, user_id: int) -> int:
        """Revoke all refresh tokens for a user."""
        query = self._tokens.where("user_id", "==", user_id).where("revoked", "==", False)
        docs = list(query.stream())

        now = datetime.utcnow()
        batch = self.client.batch()
        count = 0
        for doc in docs:
            batch.update(doc.reference, {
                "revoked": True,
                "revoked_at": now,
                "revoked_by": user_id,
            })
            count += 1

        if count > 0:
            batch.commit()
        logger.info(f"Revoked {count} refresh tokens for user_id={user_id}")
        return count
