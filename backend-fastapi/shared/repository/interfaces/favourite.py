"""Favourite repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List, Set
from shared.dto import FavouriteDTO, RemovedMatchDTO


class IFavouriteRepository(ABC):

    @abstractmethod
    def add_favourite(self, user_id: int, match_id: int, wishlist_id: int = None) -> FavouriteDTO:
        ...

    @abstractmethod
    def remove_favourite(self, user_id: int, match_id: int) -> bool:
        ...

    @abstractmethod
    def get_user_favourites(self, user_id: int, wishlist_id: int = None) -> List[FavouriteDTO]:
        ...

    @abstractmethod
    def get_favourite_match_ids(self, user_id: int, wishlist_id: int = None) -> Set[int]:
        ...

    @abstractmethod
    def dismiss_match(self, user_id: int, match_id: int, wishlist_id: int = None, reason: str = None) -> RemovedMatchDTO:
        ...

    @abstractmethod
    def get_dismissed_match_ids(self, user_id: int, wishlist_id: int = None) -> Set[int]:
        ...
