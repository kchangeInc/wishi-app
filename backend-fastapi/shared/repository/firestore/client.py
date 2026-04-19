"""Firestore client singleton."""

import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_firestore_client():
    """Get or create Firestore client singleton."""
    import firebase_admin
    from firebase_admin import credentials, firestore
    from shared.config.settings import get_settings

    settings = get_settings().firestore

    if not firebase_admin._apps:
        if settings.credentials_path:
            cred = credentials.Certificate(settings.credentials_path)
            firebase_admin.initialize_app(cred, {"projectId": settings.project_id})
        else:
            firebase_admin.initialize_app(options={"projectId": settings.project_id})

    client = firestore.client()
    logger.info(f"Firestore client initialized: project={settings.project_id}")
    return client
