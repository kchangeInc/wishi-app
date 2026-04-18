"""Centralized database configuration from environment variables."""

from shared.config.settings import get_settings


def _get(key: str, default: str) -> str:
    settings = get_settings().database
    mapping = {
        "DB_HOST": settings.host,
        "DB_PORT": settings.port,
        "DB_NAME": settings.name,
        "DB_USER": settings.user,
        "DB_PASSWORD": settings.password,
    }
    return mapping.get(key, default)


def get_db_settings() -> dict:
    """Return normalized database settings used across all DB helpers."""
    settings = get_settings().database
    return {
        "host": settings.host,
        "port": settings.port,
        "name": settings.name,
        "user": settings.user,
        "password": settings.password,
    }


def build_database_url() -> str:
    """Build SQLAlchemy-compatible DATABASE_URL with environment override."""
    return get_settings().database.url
