# shared/repository/feedback.py
"""Feedback repository"""

import logging
from sqlalchemy.orm import Session
from shared.models import Feedback
from typing import List

logger = logging.getLogger(__name__)


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, rating: int, message: str = None) -> Feedback:
        fb = Feedback(user_id=user_id, rating=rating, message=message)
        self.db.add(fb)
        self.db.commit()
        self.db.refresh(fb)
        return fb

    def get_user_feedback(self, user_id: int) -> List[Feedback]:
        return (
            self.db.query(Feedback)
            .filter(Feedback.user_id == user_id)
            .order_by(Feedback.created_at.desc())
            .all()
        )
