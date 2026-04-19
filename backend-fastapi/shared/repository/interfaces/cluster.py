"""Cluster repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from shared.dto import ClusterDTO


class IClusterRepository(ABC):

    @abstractmethod
    def get_or_create(self, normalized_filters: str, user_id: int = None) -> ClusterDTO:
        ...

    @abstractmethod
    def get_by_normalized_filters(self, normalized_filters: str) -> Optional[ClusterDTO]:
        ...

    @abstractmethod
    def get_not_deleted(self, id: int) -> Optional[ClusterDTO]:
        ...

    @abstractmethod
    def get_active_clusters(self, skip: int = 0, limit: int = 100) -> List[ClusterDTO]:
        ...

    @abstractmethod
    def update_cluster(self, id: int, user_id: int = None, **kwargs) -> Optional[ClusterDTO]:
        ...

    @abstractmethod
    def soft_delete_cluster(self, id: int, user_id: int = None) -> Optional[ClusterDTO]:
        ...
