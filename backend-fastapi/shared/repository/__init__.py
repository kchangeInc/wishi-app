# shared/repository/__init__.py
"""Repository pattern for database access"""

from shared.repository.base import BaseRepository
from shared.repository.user import UserRepository
from shared.repository.wishlist import WishlistRepository
from shared.repository.cluster import ClusterRepository
from shared.repository.match import MatchRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "WishlistRepository",
    "ClusterRepository",
    "MatchRepository"
]
