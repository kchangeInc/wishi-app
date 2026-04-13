# shared/repository/notification.py
"""Notification repository"""

import logging
from sqlalchemy.orm import Session
from shared.models import Notification
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, type: str, title: str, **kwargs) -> Notification:
        notif = Notification(user_id=user_id, type=type, title=title, **kwargs)
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def get_user_notifications(
        self, user_id: int, type: str = None, is_read: bool = None, skip: int = 0, limit: int = 50
    ) -> List[Notification]:
        q = self.db.query(Notification).filter(
            Notification.user_id == user_id, Notification.is_deleted == False
        )
        if type:
            q = q.filter(Notification.type == type)
        if is_read is not None:
            q = q.filter(Notification.is_read == is_read)
        return q.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    def get_unread_count(self, user_id: int) -> int:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False, Notification.is_deleted == False)
            .count()
        )

    def mark_read(self, notification_id: int, user_id: int) -> bool:
        notif = self.db.query(Notification).filter(
            Notification.id == notification_id, Notification.user_id == user_id
        ).first()
        if notif:
            notif.is_read = True
            notif.read_at = datetime.utcnow()
            self.db.commit()
            return True
        return False

    def mark_all_read(self, user_id: int) -> int:
        count = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False, Notification.is_deleted == False)
            .update({"is_read": True, "read_at": datetime.utcnow()})
        )
        self.db.commit()
        return count

    def soft_delete(self, notification_id: int, user_id: int) -> bool:
        notif = self.db.query(Notification).filter(
            Notification.id == notification_id, Notification.user_id == user_id
        ).first()
        if notif:
            notif.is_deleted = True
            self.db.commit()
            return True
        return False

    def clear_all(self, user_id: int) -> int:
        count = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_deleted == False)
            .update({"is_deleted": True})
        )
        self.db.commit()
        return count
