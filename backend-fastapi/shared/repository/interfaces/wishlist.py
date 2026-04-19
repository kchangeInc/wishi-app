"""Wishlist repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from shared.dto import WishlistDTO, WishlistFieldValueDTO


class IWishlistRepository(ABC):

    @abstractmethod
    def create_wishlist(self, title: str, user_id: int, user_email: str, **kwargs) -> WishlistDTO:
        ...

    @abstractmethod
    def get_by_id_not_deleted(self, id: int) -> Optional[WishlistDTO]:
        ...

    @abstractmethod
    def get_all_not_deleted(self, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        ...

    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        ...

    @abstractmethod
    def update_wishlist(self, id: int, user_id: int, **kwargs) -> Optional[WishlistDTO]:
        ...

    @abstractmethod
    def soft_delete_wishlist(self, id: int, user_id: int) -> Optional[WishlistDTO]:
        ...

    @abstractmethod
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        ...

    @abstractmethod
    def get_active_wishlists(self, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        ...

    @abstractmethod
    def set_field_values(self, wishlist_id: int, field_values: list) -> None:
        ...

    @abstractmethod
    def get_field_values(self, wishlist_id: int) -> List[WishlistFieldValueDTO]:
        ...

    @abstractmethod
    def set_preferred_marketplaces(self, wishlist_id: int, source_ids: list) -> None:
        ...
