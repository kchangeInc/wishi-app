"""Abstract repository interfaces for database-agnostic access."""

from .base import IBaseRepository
from .user import IUserRepository
from .wishlist import IWishlistRepository
from .cluster import IClusterRepository
from .match import IMatchRepository
from .category import ICategoryRepository
from .favourite import IFavouriteRepository
from .notification import INotificationRepository
from .notification_setting import INotificationSettingRepository
from .saved_listing import ISavedListingRepository
from .feedback import IFeedbackRepository

__all__ = [
    "IBaseRepository",
    "IUserRepository",
    "IWishlistRepository",
    "IClusterRepository",
    "IMatchRepository",
    "ICategoryRepository",
    "IFavouriteRepository",
    "INotificationRepository",
    "INotificationSettingRepository",
    "ISavedListingRepository",
    "IFeedbackRepository",
]
