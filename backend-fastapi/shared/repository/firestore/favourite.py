"""Firestore Favourite repository implementation."""

import logging
from datetime import datetime
from typing import Optional, List, Set

from shared.dto import FavouriteDTO, RemovedMatchDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.favourite import IFavouriteRepository

logger = logging.getLogger(__name__)


def _fav_to_dto(data: dict) -> Optional[FavouriteDTO]:
    if data is None:
        return None
    return FavouriteDTO(
        id=data.get("id", 0),
        user_id=data.get("user_id"),
        match_id=data.get("match_id"),
        wishlist_id=data.get("wishlist_id"),
        created_at=data.get("created_at"),
    )


def _rm_to_dto(data: dict) -> Optional[RemovedMatchDTO]:
    if data is None:
        return None
    return RemovedMatchDTO(
        id=data.get("id", 0),
        user_id=data.get("user_id"),
        match_id=data.get("match_id"),
        wishlist_id=data.get("wishlist_id"),
        reason=data.get("reason"),
        created_at=data.get("created_at"),
    )


class FsFavouriteRepository(FsBaseRepository, IFavouriteRepository):
    """Firestore implementation of favourite repository.

    Uses composite doc ID ``{user_id}_{match_id}`` for uniqueness.
    """

    def __init__(self, client):
        super().__init__(client, col.FAVOURITES)
        self._removed = client.collection(col.REMOVED_MATCHES)

    @staticmethod
    def _composite_id(user_id: int, match_id: int) -> str:
        return f"{user_id}_{match_id}"

    # ---- Favourites ----

    def add_favourite(self, user_id: int, match_id: int, wishlist_id: int = None) -> FavouriteDTO:
        doc_id = self._composite_id(user_id, match_id)
        now = datetime.utcnow()
        data = {
            "id": doc_id,
            "user_id": user_id,
            "match_id": match_id,
            "wishlist_id": wishlist_id,
            "created_at": now,
        }
        self.collection.document(doc_id).set(data)
        return _fav_to_dto(data)

    def remove_favourite(self, user_id: int, match_id: int) -> bool:
        doc_id = self._composite_id(user_id, match_id)
        doc_ref = self.collection.document(doc_id)
        doc = doc_ref.get()
        if not doc.exists:
            return False
        doc_ref.delete()
        return True

    def get_user_favourites(self, user_id: int, wishlist_id: int = None) -> List[FavouriteDTO]:
        query = self.collection.where("user_id", "==", user_id)
        if wishlist_id is not None:
            query = query.where("wishlist_id", "==", wishlist_id)
        query = query.order_by("created_at", direction="DESCENDING")
        docs = list(query.stream())
        return [_fav_to_dto(doc.to_dict()) for doc in docs]

    def get_favourite_match_ids(self, user_id: int, wishlist_id: int = None) -> Set[int]:
        query = self.collection.where("user_id", "==", user_id)
        if wishlist_id is not None:
            query = query.where("wishlist_id", "==", wishlist_id)
        docs = list(query.stream())
        return {doc.to_dict().get("match_id") for doc in docs}

    # ---- Removed / dismissed ----

    def dismiss_match(self, user_id: int, match_id: int, wishlist_id: int = None,
                      reason: str = None) -> RemovedMatchDTO:
        doc_id = self._composite_id(user_id, match_id)
        now = datetime.utcnow()
        data = {
            "id": doc_id,
            "user_id": user_id,
            "match_id": match_id,
            "wishlist_id": wishlist_id,
            "reason": reason,
            "created_at": now,
        }
        self._removed.document(doc_id).set(data)
        return _rm_to_dto(data)

    def get_dismissed_match_ids(self, user_id: int, wishlist_id: int = None) -> Set[int]:
        query = self._removed.where("user_id", "==", user_id)
        if wishlist_id is not None:
            query = query.where("wishlist_id", "==", wishlist_id)
        docs = list(query.stream())
        return {doc.to_dict().get("match_id") for doc in docs}
