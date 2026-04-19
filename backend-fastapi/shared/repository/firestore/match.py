"""Firestore Match repository implementation."""

import logging
from datetime import datetime
from typing import Optional, List

from shared.dto import MatchDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.match import IMatchRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> Optional[MatchDTO]:
    if data is None:
        return None
    return MatchDTO(
        id=data.get("id"),
        url=data.get("url", ""),
        cluster_id=data.get("cluster_id"),
        wishlist_id=data.get("wishlist_id"),
        marketplace_source_id=data.get("marketplace_source_id"),
        source=data.get("source"),
        title=data.get("title"),
        description=data.get("description"),
        price=data.get("price"),
        formatted_price=data.get("formatted_price"),
        location=data.get("location"),
        image_url=data.get("image_url"),
        score=data.get("score"),
        status=data.get("status", "pending"),
        validation_attempts=data.get("validation_attempts", 0),
        last_validation_error=data.get("last_validation_error"),
        validation_details=data.get("validation_details"),
        specs=data.get("specs"),
        seller_tag=data.get("seller_tag"),
        is_featured=data.get("is_featured", False),
        posted_at=data.get("posted_at"),
        is_active=data.get("is_active", True),
        is_deleted=data.get("is_deleted", False),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
        last_validated_at=data.get("last_validated_at"),
        created_by=data.get("created_by"),
        updated_by=data.get("updated_by"),
        version=data.get("version", 1),
    )


class FsMatchRepository(FsBaseRepository, IMatchRepository):
    """Firestore implementation of match repository."""

    def __init__(self, client):
        super().__init__(client, col.MATCHES)

    def create_match(self, cluster_id: int = None, url: str = "", source: str = "",
                     score: int = 0, status: str = "pending", user_id: int = None,
                     **kwargs) -> MatchDTO:
        now = datetime.utcnow()
        data = self.create(
            cluster_id=cluster_id,
            url=url,
            source=source,
            score=score,
            status=status,
            is_active=True,
            is_deleted=False,
            created_by=user_id,
            updated_by=user_id,
            created_at=now,
            updated_at=now,
            last_validated_at=now,
            version=1,
            **kwargs,
        )
        return _to_dto(data)

    def get_by_url(self, url: str) -> Optional[MatchDTO]:
        data = self._query_one(url=url, is_deleted=False)
        return _to_dto(data)

    def get_by_cluster(self, cluster_id: int, skip: int = 0, limit: int = 100) -> List[MatchDTO]:
        results = self._query_many(
            filters=[
                ("cluster_id", "==", cluster_id),
                ("is_deleted", "==", False),
            ],
            order_by="score",
            order_dir="DESCENDING",
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def get_pending_validation(self, limit: int = 50) -> List[MatchDTO]:
        """Get matches pending validation (status in auto_publish, admin_review, new)."""
        query = self.collection.where(
            "status", "in", ["auto_publish", "admin_review", "new"]
        ).where("is_deleted", "==", False).order_by(
            "last_validated_at"
        ).limit(limit)

        docs = list(query.stream())
        return [_to_dto(doc.to_dict()) for doc in docs]

    def update_match(self, id: int, user_id: int = None, **kwargs) -> Optional[MatchDTO]:
        data = self.get_by_id(id)
        if not data:
            return None

        kwargs["updated_by"] = user_id
        kwargs["updated_at"] = datetime.utcnow()
        kwargs["version"] = (data.get("version") or 0) + 1

        self.collection.document(str(id)).update(kwargs)
        data.update(kwargs)
        return _to_dto(data)

    def soft_delete_match(self, id: int, user_id: int = None) -> Optional[MatchDTO]:
        data = self.get_by_id(id)
        if not data:
            return None

        updates = {
            "is_deleted": True,
            "updated_by": user_id,
            "updated_at": datetime.utcnow(),
        }
        self.collection.document(str(id)).update(updates)
        data.update(updates)
        return _to_dto(data)

    def get_by_wishlist(self, wishlist_id: int, skip: int = 0, limit: int = 50) -> List[MatchDTO]:
        """Get matches for a wishlist (published or auto_publish)."""
        query = self.collection.where(
            "wishlist_id", "==", wishlist_id
        ).where(
            "is_deleted", "==", False
        ).where(
            "status", "in", ["published", "auto_publish"]
        ).order_by("score", direction="DESCENDING").limit(skip + limit)

        docs = list(query.stream())
        results = [_to_dto(doc.to_dict()) for doc in docs]
        return results[skip:]

    def get_active_matches(self, skip: int = 0, limit: int = 100) -> List[MatchDTO]:
        results = self._query_many(
            filters=[
                ("status", "==", "published"),
                ("is_active", "==", True),
                ("is_deleted", "==", False),
            ],
            order_by="score",
            order_dir="DESCENDING",
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[MatchDTO]:
        results = self._query_many(
            filters=[
                ("status", "==", status),
                ("is_deleted", "==", False),
            ],
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]
