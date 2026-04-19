"""User repository interface."""

from abc import ABC, abstractmethod
from typing import Optional
from shared.dto import UserDTO


class IUserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserDTO]:
        ...

    @abstractmethod
    def get_by_google_id(self, google_id: str) -> Optional[UserDTO]:
        ...

    @abstractmethod
    def get_active_user(self, id: int) -> Optional[UserDTO]:
        ...

    @abstractmethod
    def verify_password_login(self, email: str, password: str) -> Optional[UserDTO]:
        ...

    @abstractmethod
    def create_or_update_google_user(self, email: str, google_id: str, name: str = None) -> UserDTO:
        ...

    @abstractmethod
    def update_user(self, id: int, **kwargs) -> Optional[UserDTO]:
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int, expires_days: int = 7) -> str:
        ...

    @abstractmethod
    def validate_refresh_token(self, token: str) -> Optional[int]:
        ...

    @abstractmethod
    def revoke_refresh_token(self, token: str, user_id: int) -> bool:
        ...

    @abstractmethod
    def revoke_all_user_tokens(self, user_id: int) -> int:
        ...
