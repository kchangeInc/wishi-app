"""Notification setting repository interface."""

from abc import ABC, abstractmethod
from shared.dto import NotificationSettingDTO


class INotificationSettingRepository(ABC):

    @abstractmethod
    def get_or_create(self, user_id: int) -> NotificationSettingDTO:
        ...

    @abstractmethod
    def update(self, user_id: int, **kwargs) -> NotificationSettingDTO:
        ...
