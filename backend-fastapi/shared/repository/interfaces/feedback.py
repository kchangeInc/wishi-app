"""Feedback repository interface."""

from abc import ABC, abstractmethod
from typing import List
from shared.dto import FeedbackDTO


class IFeedbackRepository(ABC):

    @abstractmethod
    def create(self, user_id: int, rating: int, message: str = None) -> FeedbackDTO:
        ...

    @abstractmethod
    def get_user_feedback(self, user_id: int) -> List[FeedbackDTO]:
        ...
