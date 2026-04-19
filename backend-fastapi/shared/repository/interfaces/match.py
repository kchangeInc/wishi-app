"""Match repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from shared.dto import MatchDTO


class IMatchRepository(ABC):

    @abstractmethod
    def create_match(self, cluster_id: int = None, url: str = "", source: str = "",
                     score: int = 0, status: str = "pending", user_id: int = None,
                     **kwargs) -> MatchDTO:
        ...

    @abstractmethod
    def get_by_url(self, url: str) -> Optional[MatchDTO]:
        ...

    @abstractmethod
    def get_by_cluster(self, cluster_id: int, skip: int = 0, limit: int = 100) -> List[MatchDTO]:
        ...

    @abstractmethod
    def get_pending_validation(self, limit: int = 50) -> List[MatchDTO]:
        ...

    @abstractmethod
    def update_match(self, id: int, user_id: int = None, **kwargs) -> Optional[MatchDTO]:
        ...

    @abstractmethod
    def soft_delete_match(self, id: int, user_id: int = None) -> Optional[MatchDTO]:
        ...

    @abstractmethod
    def get_by_wishlist(self, wishlist_id: int, skip: int = 0, limit: int = 50) -> List[MatchDTO]:
        ...

    @abstractmethod
    def get_active_matches(self, skip: int = 0, limit: int = 100) -> List[MatchDTO]:
        ...

    @abstractmethod
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[MatchDTO]:
        ...
