"""FastAPI dependency injection for database sessions and repositories."""

from fastapi import Depends
from shared.config.settings import get_settings
from shared.db.provider import DbBackend
from shared.repository.factory import RepositoryFactory, get_db_backend


def get_db():
    """Yields the appropriate database session/client based on config."""
    backend = get_db_backend()
    if backend == DbBackend.POSTGRESQL:
        from shared.db.session import SessionLocal
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        from shared.repository.firestore.client import get_firestore_client
        yield get_firestore_client()


def get_repos(db=Depends(get_db)) -> RepositoryFactory:
    """Get a RepositoryFactory instance for the current request."""
    backend = get_db_backend()
    return RepositoryFactory(backend, db)
