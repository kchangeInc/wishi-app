"""Database backend enum."""

from enum import Enum


class DbBackend(str, Enum):
    POSTGRESQL = "postgresql"
    FIRESTORE = "firestore"
