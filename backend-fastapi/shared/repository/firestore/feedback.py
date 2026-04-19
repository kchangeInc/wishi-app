"""Firestore Feedback repository implementation."""

import logging
from datetime import datetime
from typing import List

from shared.dto import FeedbackDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.feedback import IFeedbackRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> FeedbackDTO:
    return FeedbackDTO(
        id=data.get("id"),
        user_id=data.get("user_id"),
        rating=data.get("rating", 0),
        message=data.get("message"),
        created_at=data.get("created_at"),
    )


class FsFeedbackRepository(FsBaseRepository, IFeedbackRepository):
    """Firestore implementation of feedback repository."""

    def __init__(self, client):
        super().__init__(client, col.FEEDBACK)

    def create(self, user_id: int, rating: int, message: str = None) -> FeedbackDTO:
        now = datetime.utcnow()
        data = super().create(
            user_id=user_id,
            rating=rating,
            message=message,
            created_at=now,
        )
        return _to_dto(data)

    def get_user_feedback(self, user_id: int) -> List[FeedbackDTO]:
        results = self._query_many(
            filters=[("user_id", "==", user_id)],
            order_by="created_at",
            order_dir="DESCENDING",
        )
        return [_to_dto(r) for r in results]
