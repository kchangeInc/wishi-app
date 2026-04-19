"""Firestore Notification repository implementation."""

import logging
from datetime import datetime
from typing import Optional, List

from shared.dto import NotificationDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.notification import INotificationRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> Optional[NotificationDTO]:
    if data is None:
        return None
    return NotificationDTO(
        id=data.get("id"),
        user_id=data.get("user_id"),
        type=data.get("type", ""),
        title=data.get("title", ""),
        description=data.get("description"),
        wishlist_id=data.get("wishlist_id"),
        match_id=data.get("match_id"),
        action_url=data.get("action_url"),
        is_read=data.get("is_read", False),
        read_at=data.get("read_at"),
        is_deleted=data.get("is_deleted", False),
        created_at=data.get("created_at"),
    )


class FsNotificationRepository(FsBaseRepository, INotificationRepository):
    """Firestore implementation of notification repository."""

    def __init__(self, client):
        super().__init__(client, col.NOTIFICATIONS)

    def create(self, user_id: int, type: str, title: str, **kwargs) -> NotificationDTO:
        now = datetime.utcnow()
        data = super().create(
            user_id=user_id,
            type=type,
            title=title,
            is_read=False,
            is_deleted=False,
            created_at=now,
            **kwargs,
        )
        return _to_dto(data)

    def get_user_notifications(self, user_id: int, type: str = None,
                                is_read: bool = None, skip: int = 0,
                                limit: int = 50) -> List[NotificationDTO]:
        filters = [
            ("user_id", "==", user_id),
            ("is_deleted", "==", False),
        ]
        if type is not None:
            filters.append(("type", "==", type))
        if is_read is not None:
            filters.append(("is_read", "==", is_read))

        results = self._query_many(
            filters=filters,
            order_by="created_at",
            order_dir="DESCENDING",
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def get_unread_count(self, user_id: int) -> int:
        query = self.collection.where(
            "user_id", "==", user_id
        ).where(
            "is_read", "==", False
        ).where(
            "is_deleted", "==", False
        )
        docs = list(query.stream())
        return len(docs)

    def mark_read(self, notification_id: int, user_id: int) -> bool:
        doc_ref = self.collection.document(str(notification_id))
        doc = doc_ref.get()
        if not doc.exists:
            return False
        data = doc.to_dict()
        if data.get("user_id") != user_id:
            return False

        doc_ref.update({
            "is_read": True,
            "read_at": datetime.utcnow(),
        })
        return True

    def mark_all_read(self, user_id: int) -> int:
        """Mark all unread notifications as read using batch writes."""
        query = self.collection.where(
            "user_id", "==", user_id
        ).where(
            "is_read", "==", False
        ).where(
            "is_deleted", "==", False
        )
        docs = list(query.stream())

        now = datetime.utcnow()
        count = 0
        batch = self.client.batch()
        for doc in docs:
            batch.update(doc.reference, {"is_read": True, "read_at": now})
            count += 1
            # Firestore batch limit is 500
            if count % 500 == 0:
                batch.commit()
                batch = self.client.batch()

        if count % 500 != 0:
            batch.commit()

        return count

    def soft_delete(self, notification_id: int, user_id: int) -> bool:
        doc_ref = self.collection.document(str(notification_id))
        doc = doc_ref.get()
        if not doc.exists:
            return False
        data = doc.to_dict()
        if data.get("user_id") != user_id:
            return False

        doc_ref.update({"is_deleted": True})
        return True

    def clear_all(self, user_id: int) -> int:
        """Mark all notifications as deleted using batch writes."""
        query = self.collection.where(
            "user_id", "==", user_id
        ).where(
            "is_deleted", "==", False
        )
        docs = list(query.stream())

        count = 0
        batch = self.client.batch()
        for doc in docs:
            batch.update(doc.reference, {"is_deleted": True})
            count += 1
            if count % 500 == 0:
                batch.commit()
                batch = self.client.batch()

        if count % 500 != 0:
            batch.commit()

        return count
