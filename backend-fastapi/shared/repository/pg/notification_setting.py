# shared/repository/pg/notification_setting.py
"""PostgreSQL NotificationSetting repository"""

import logging
from sqlalchemy.orm import Session
from shared.models import NotificationSetting
from shared.repository.interfaces.notification_setting import INotificationSettingRepository
from typing import Optional

logger = logging.getLogger(__name__)


class PgNotificationSettingRepository(INotificationSettingRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, user_id: int) -> NotificationSetting:
        setting = self.db.query(NotificationSetting).filter(
            NotificationSetting.user_id == user_id
        ).first()
        if not setting:
            setting = NotificationSetting(user_id=user_id)
            self.db.add(setting)
            self.db.commit()
            self.db.refresh(setting)
        return setting

    def update(self, user_id: int, **kwargs) -> NotificationSetting:
        setting = self.get_or_create(user_id)
        for key, value in kwargs.items():
            if hasattr(setting, key):
                setattr(setting, key, value)
        self.db.commit()
        self.db.refresh(setting)
        return setting
