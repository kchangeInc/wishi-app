"""Global backend settings loaded from environment variables."""

from dataclasses import dataclass
from functools import lru_cache
import os


def _get_str(key: str, default: str) -> str:
    value = os.getenv(key)
    if value is None:
        return default
    return value


def _get_int(key: str, default: int) -> int:
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class DatabaseSettings:
    host: str
    port: str
    name: str
    user: str
    password: str
    url: str


@dataclass(frozen=True)
class AuthSettings:
    secret_key: str
    google_client_id: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


@dataclass(frozen=True)
class MessagingSettings:
    kafka_bootstrap_servers: str
    celery_broker_url: str


@dataclass(frozen=True)
class ServiceUrls:
    auth: str
    wishlist: str
    seller: str
    matching: str
    cluster: str
    match: str
    validation: str
    notification: str
    admin: str


@dataclass(frozen=True)
class BackendSettings:
    database: DatabaseSettings
    auth: AuthSettings
    messaging: MessagingSettings
    service_urls: ServiceUrls


@lru_cache(maxsize=1)
def get_settings() -> BackendSettings:
    db_host = _get_str("DB_HOST", "localhost")
    db_port = _get_str("DB_PORT", "5432")
    db_name = _get_str("DB_NAME", "wishi")
    db_user = _get_str("DB_USER", "postgres")
    db_password = _get_str("DB_PASSWORD", "admin")
    db_url = _get_str(
        "DATABASE_URL",
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    )

    return BackendSettings(
        database=DatabaseSettings(
            host=db_host,
            port=db_port,
            name=db_name,
            user=db_user,
            password=db_password,
            url=db_url,
        ),
        auth=AuthSettings(
            secret_key=_get_str("SECRET_KEY", "CHANGE_THIS_TO_ENV"),
            google_client_id=_get_str("GOOGLE_CLIENT_ID", ""),
            access_token_expire_minutes=_get_int("ACCESS_TOKEN_EXPIRE_MINUTES", 30),
            refresh_token_expire_days=_get_int("REFRESH_TOKEN_EXPIRE_DAYS", 7),
        ),
        messaging=MessagingSettings(
            kafka_bootstrap_servers=_get_str("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
            celery_broker_url=_get_str("CELERY_BROKER_URL", "redis://redis:6379/0"),
        ),
        service_urls=ServiceUrls(
            auth=_get_str("AUTH_SERVICE_URL", "http://localhost:8001"),
            wishlist=_get_str("WISHLIST_SERVICE_URL", "http://localhost:8002"),
            seller=_get_str("SELLER_SERVICE_URL", "http://localhost:8003"),
            matching=_get_str("MATCHING_SERVICE_URL", "http://localhost:8004"),
            cluster=_get_str("CLUSTER_SERVICE_URL", "http://localhost:8005"),
            match=_get_str("MATCH_ENGINE_SERVICE_URL", "http://localhost:8006"),
            validation=_get_str("VALIDATION_SERVICE_URL", "http://localhost:8007"),
            notification=_get_str("NOTIFICATION_SERVICE_URL", "http://localhost:8008"),
            admin=_get_str("ADMIN_SERVICE_URL", "http://localhost:8009"),
        ),
    )
