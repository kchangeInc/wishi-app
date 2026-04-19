"""Repository factory for database-agnostic repository creation."""

import logging
from contextlib import contextmanager
from shared.db.provider import DbBackend
from shared.config.settings import get_settings

logger = logging.getLogger(__name__)


def get_db_backend() -> DbBackend:
    return DbBackend(get_settings().db_backend)


@contextmanager
def create_repos():
    """Create a RepositoryFactory for non-FastAPI contexts (Celery tasks, background threads).

    Usage:
        with create_repos() as repos:
            user_repo = repos.user()
            user = user_repo.get_active_user(1)
    """
    backend = get_db_backend()
    if backend == DbBackend.POSTGRESQL:
        from shared.db.session import SessionLocal
        db = SessionLocal()
        try:
            yield RepositoryFactory(backend, db)
        finally:
            db.close()
    else:
        from shared.repository.firestore.client import get_firestore_client
        yield RepositoryFactory(backend, get_firestore_client())


class RepositoryFactory:
    """Creates repository instances for the configured database backend."""

    def __init__(self, backend: DbBackend, db_session):
        self.backend = backend
        self.db = db_session

    def user(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.user import PgUserRepository
            return PgUserRepository(self.db)
        from shared.repository.firestore.user import FsUserRepository
        return FsUserRepository(self.db)

    def wishlist(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.wishlist import PgWishlistRepository
            return PgWishlistRepository(self.db)
        from shared.repository.firestore.wishlist import FsWishlistRepository
        return FsWishlistRepository(self.db)

    def cluster(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.cluster import PgClusterRepository
            return PgClusterRepository(self.db)
        from shared.repository.firestore.cluster import FsClusterRepository
        return FsClusterRepository(self.db)

    def match(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.match import PgMatchRepository
            return PgMatchRepository(self.db)
        from shared.repository.firestore.match import FsMatchRepository
        return FsMatchRepository(self.db)

    def category(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.category import PgCategoryRepository
            return PgCategoryRepository(self.db)
        from shared.repository.firestore.category import FsCategoryRepository
        return FsCategoryRepository(self.db)

    def favourite(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.favourite import PgFavouriteRepository
            return PgFavouriteRepository(self.db)
        from shared.repository.firestore.favourite import FsFavouriteRepository
        return FsFavouriteRepository(self.db)

    def notification(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.notification import PgNotificationRepository
            return PgNotificationRepository(self.db)
        from shared.repository.firestore.notification import FsNotificationRepository
        return FsNotificationRepository(self.db)

    def notification_setting(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.notification_setting import PgNotificationSettingRepository
            return PgNotificationSettingRepository(self.db)
        from shared.repository.firestore.notification_setting import FsNotificationSettingRepository
        return FsNotificationSettingRepository(self.db)

    def saved_listing(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.saved_listing import PgSavedListingRepository
            return PgSavedListingRepository(self.db)
        from shared.repository.firestore.saved_listing import FsSavedListingRepository
        return FsSavedListingRepository(self.db)

    def feedback(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.feedback import PgFeedbackRepository
            return PgFeedbackRepository(self.db)
        from shared.repository.firestore.feedback import FsFeedbackRepository
        return FsFeedbackRepository(self.db)

    def banner_idea(self):
        if self.backend == DbBackend.POSTGRESQL:
            from shared.repository.pg.banner_idea import PgBannerIdeaRepository
            return PgBannerIdeaRepository(self.db)
        from shared.repository.firestore.banner_idea import FsBannerIdeaRepository
        return FsBannerIdeaRepository(self.db)
