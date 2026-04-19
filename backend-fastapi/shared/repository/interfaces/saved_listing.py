"""Saved listing repository interface."""

from abc import ABC, abstractmethod
from typing import List
from shared.dto import SavedListingDTO


class ISavedListingRepository(ABC):

    @abstractmethod
    def save_listing(self, user_id: int, **kwargs) -> SavedListingDTO:
        ...

    @abstractmethod
    def get_user_saved(self, user_id: int, skip: int = 0, limit: int = 50) -> List[SavedListingDTO]:
        ...

    @abstractmethod
    def delete_saved(self, listing_id: int, user_id: int) -> bool:
        ...
