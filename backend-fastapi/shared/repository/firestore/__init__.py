"""Firestore repository implementations."""

from shared.repository.firestore.user import FsUserRepository
from shared.repository.firestore.wishlist import FsWishlistRepository
from shared.repository.firestore.cluster import FsClusterRepository
from shared.repository.firestore.match import FsMatchRepository
from shared.repository.firestore.category import FsCategoryRepository
from shared.repository.firestore.favourite import FsFavouriteRepository
from shared.repository.firestore.notification import FsNotificationRepository
from shared.repository.firestore.notification_setting import FsNotificationSettingRepository
from shared.repository.firestore.saved_listing import FsSavedListingRepository
from shared.repository.firestore.feedback import FsFeedbackRepository

__all__ = [
    "FsUserRepository",
    "FsWishlistRepository",
    "FsClusterRepository",
    "FsMatchRepository",
    "FsCategoryRepository",
    "FsFavouriteRepository",
    "FsNotificationRepository",
    "FsNotificationSettingRepository",
    "FsSavedListingRepository",
    "FsFeedbackRepository",
]
