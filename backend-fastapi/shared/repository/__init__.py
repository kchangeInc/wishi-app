# shared/repository/__init__.py
"""Repository pattern for database access"""

from shared.repository.base import BaseRepository
from shared.repository.user import UserRepository
from shared.repository.wishlist import WishlistRepository
from shared.repository.cluster import ClusterRepository
from shared.repository.match import MatchRepository
from shared.repository.category import CategoryRepository
from shared.repository.favourite import FavouriteRepository
from shared.repository.saved_listing import SavedListingRepository
from shared.repository.notification import NotificationRepository
from shared.repository.notification_setting import NotificationSettingRepository
from shared.repository.feedback import FeedbackRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "WishlistRepository",
    "ClusterRepository",
    "MatchRepository",
    "CategoryRepository",
    "FavouriteRepository",
    "SavedListingRepository",
    "NotificationRepository",
    "NotificationSettingRepository",
    "FeedbackRepository",
]
