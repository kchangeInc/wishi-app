# shared/repository/__init__.py
"""Repository pattern for database access.

Backward-compatible re-exports from the pg/ sub-package so that existing
imports like ``from shared.repository import UserRepository`` keep working.
"""

from shared.repository.pg import (
    PgBaseRepository as BaseRepository,
    PgUserRepository as UserRepository,
    PgWishlistRepository as WishlistRepository,
    PgClusterRepository as ClusterRepository,
    PgMatchRepository as MatchRepository,
    PgCategoryRepository as CategoryRepository,
    PgFavouriteRepository as FavouriteRepository,
    PgNotificationRepository as NotificationRepository,
    PgNotificationSettingRepository as NotificationSettingRepository,
    PgSavedListingRepository as SavedListingRepository,
    PgFeedbackRepository as FeedbackRepository,
)

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
