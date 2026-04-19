"""Firestore NotificationSetting repository implementation."""

import logging
from datetime import datetime
from typing import Optional

from shared.dto import NotificationSettingDTO
from shared.repository.firestore import collections as col
from shared.repository.interfaces.notification_setting import INotificationSettingRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> Optional[NotificationSettingDTO]:
    if data is None:
        return None
    return NotificationSettingDTO(
        id=data.get("id", 0),
        user_id=data.get("user_id"),
        email_matches=data.get("email_matches", True),
        email_price_drops=data.get("email_price_drops", True),
        email_newsletter=data.get("email_newsletter", False),
        push_matches=data.get("push_matches", True),
        push_messages=data.get("push_messages", True),
        push_promotions=data.get("push_promotions", False),
        updated_at=data.get("updated_at"),
    )


# Default settings for a new user
_DEFAULTS = {
    "email_matches": True,
    "email_price_drops": True,
    "email_newsletter": False,
    "push_matches": True,
    "push_messages": True,
    "push_promotions": False,
}


class FsNotificationSettingRepository(INotificationSettingRepository):
    """Firestore implementation of notification setting repository.

    Uses user_id as the document ID (one doc per user).
    """

    def __init__(self, client):
        self.client = client
        self.collection = client.collection(col.NOTIFICATION_SETTINGS)

    def get_or_create(self, user_id: int) -> NotificationSettingDTO:
        doc_ref = self.collection.document(str(user_id))
        doc = doc_ref.get()

        if doc.exists:
            return _to_dto(doc.to_dict())

        # Create with defaults
        now = datetime.utcnow()
        data = {
            "id": user_id,
            "user_id": user_id,
            "updated_at": now,
            **_DEFAULTS,
        }
        doc_ref.set(data)
        return _to_dto(data)

    def update(self, user_id: int, **kwargs) -> NotificationSettingDTO:
        # Ensure the document exists
        self.get_or_create(user_id)

        doc_ref = self.collection.document(str(user_id))
        kwargs["updated_at"] = datetime.utcnow()

        # Filter to only known fields
        allowed = set(_DEFAULTS.keys()) | {"updated_at"}
        filtered = {k: v for k, v in kwargs.items() if k in allowed}

        doc_ref.update(filtered)
        updated = doc_ref.get()
        return _to_dto(updated.to_dict())
