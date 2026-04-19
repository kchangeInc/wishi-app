"""Notification repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from shared.dto import NotificationDTO


class INotificationRepository(ABC):

    @abstractmethod
    def create(self, user_id: int, type: str, title: str, **kwargs) -> NotificationDTO:
        ...

    @abstractmethod
    def get_user_notifications(self, user_id: int, type: str = None,
                                is_read: bool = None, skip: int = 0,
                                limit: int = 50) -> List[NotificationDTO]:
        ...

    @abstractmethod
    def get_unread_count(self, user_id: int) -> int:
        ...

    @abstractmethod
    def mark_read(self, notification_id: int, user_id: int) -> bool:
        ...

    @abstractmethod
    def mark_all_read(self, user_id: int) -> int:
        ...

    @abstractmethod
    def soft_delete(self, notification_id: int, user_id: int) -> bool:
        ...

    @abstractmethod
    def clear_all(self, user_id: int) -> int:
        ...
