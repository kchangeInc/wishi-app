"""Firestore SavedListing repository implementation."""

import logging
from datetime import datetime
from typing import List

from shared.dto import SavedListingDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.saved_listing import ISavedListingRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> SavedListingDTO:
    return SavedListingDTO(
        id=data.get("id"),
        user_id=data.get("user_id"),
        url=data.get("url", ""),
        title=data.get("title"),
        price=data.get("price"),
        price_numeric=data.get("price_numeric"),
        location=data.get("location"),
        category=data.get("category"),
        image_url=data.get("image_url"),
        source=data.get("source"),
        saved_at=data.get("saved_at"),
        is_deleted=data.get("is_deleted", False),
    )


class FsSavedListingRepository(FsBaseRepository, ISavedListingRepository):
    """Firestore implementation of saved listing repository."""

    def __init__(self, client):
        super().__init__(client, col.SAVED_LISTINGS)

    def save_listing(self, user_id: int, **kwargs) -> SavedListingDTO:
        now = datetime.utcnow()
        data = self.create(
            user_id=user_id,
            saved_at=now,
            is_deleted=False,
            **kwargs,
        )
        return _to_dto(data)

    def get_user_saved(self, user_id: int, skip: int = 0, limit: int = 50) -> List[SavedListingDTO]:
        results = self._query_many(
            filters=[
                ("user_id", "==", user_id),
                ("is_deleted", "==", False),
            ],
            order_by="saved_at",
            order_dir="DESCENDING",
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def delete_saved(self, listing_id: int, user_id: int) -> bool:
        doc_ref = self.collection.document(str(listing_id))
        doc = doc_ref.get()
        if not doc.exists:
            return False
        data = doc.to_dict()
        if data.get("user_id") != user_id:
            return False

        doc_ref.update({"is_deleted": True})
        return True
