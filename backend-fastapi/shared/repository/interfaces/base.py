"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")


class IBaseRepository(ABC, Generic[T]):

    @abstractmethod
    def create(self, **kwargs) -> T:
        ...

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        ...

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        ...

    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[T]:
        ...

    @abstractmethod
    def delete(self, id: int) -> bool:
        ...

    @abstractmethod
    def soft_delete(self, id: int, user_id: int = None) -> Optional[T]:
        ...
