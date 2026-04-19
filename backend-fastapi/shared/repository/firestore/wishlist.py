"""Firestore Wishlist repository implementation."""

import logging
from datetime import datetime
from typing import Optional, List

from shared.dto import WishlistDTO, WishlistFieldValueDTO
from shared.repository.firestore.base import FsBaseRepository
from shared.repository.firestore import collections as col
from shared.repository.interfaces.wishlist import IWishlistRepository

logger = logging.getLogger(__name__)


def _to_dto(data: dict) -> Optional[WishlistDTO]:
    if data is None:
        return None
    return WishlistDTO(
        id=data.get("id"),
        user_id=data.get("user_id"),
        title=data.get("title", ""),
        user_email=data.get("user_email"),
        display_title=data.get("display_title"),
        description=data.get("description"),
        category_id=data.get("category_id"),
        subcategory_id=data.get("subcategory_id"),
        filters_json=data.get("filters_json"),
        notes=data.get("notes"),
        expiry_date=data.get("expiry_date"),
        status=data.get("status", "active"),
        priority=data.get("priority", "medium"),
        is_active=data.get("is_active", True),
        is_deleted=data.get("is_deleted", False),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
        created_by=data.get("created_by"),
        updated_by=data.get("updated_by"),
        version=data.get("version", 1),
        field_values=[],
    )


def _fv_to_dto(data: dict) -> WishlistFieldValueDTO:
    return WishlistFieldValueDTO(
        id=data.get("id", 0),
        wishlist_id=data.get("wishlist_id", 0),
        field_definition_id=data.get("field_definition_id", 0),
        value_text=data.get("value_text"),
        value_numeric=data.get("value_numeric"),
        created_at=data.get("created_at"),
    )


class FsWishlistRepository(FsBaseRepository, IWishlistRepository):
    """Firestore implementation of wishlist repository."""

    def __init__(self, client):
        super().__init__(client, col.WISHLISTS)

    def _fv_collection(self, wishlist_id: int):
        """Get the field_values subcollection for a wishlist."""
        return self.collection.document(str(wishlist_id)).collection(col.WISHLIST_FIELD_VALUES)

    def _mp_collection(self, wishlist_id: int):
        """Get the preferred_marketplaces subcollection for a wishlist."""
        return self.collection.document(str(wishlist_id)).collection(col.WISHLIST_PREFERRED_MARKETPLACES)

    def create_wishlist(self, title: str, user_id: int, user_email: str, **kwargs) -> WishlistDTO:
        now = datetime.utcnow()
        field_values = kwargs.pop("field_values", [])
        source_ids = kwargs.pop("preferred_marketplace_ids", [])

        data = self.create(
            title=title,
            user_id=user_id,
            user_email=user_email,
            created_by=user_id,
            created_at=now,
            updated_at=now,
            is_active=True,
            is_deleted=False,
            status="active",
            priority=kwargs.get("priority", "medium"),
            version=1,
            **{k: v for k, v in kwargs.items() if k not in ("priority",)},
        )

        wishlist_id = data["id"]

        if field_values:
            self.set_field_values(wishlist_id, field_values)

        if source_ids:
            self.set_preferred_marketplaces(wishlist_id, source_ids)

        return _to_dto(data)

    def get_by_id_not_deleted(self, id: int) -> Optional[WishlistDTO]:
        data = self.get_by_id(id)
        if data and not data.get("is_deleted", False):
            return _to_dto(data)
        return None

    def get_all_not_deleted(self, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        results = self._query_many(
            filters=[("is_deleted", "==", False)],
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        results = self._query_many(
            filters=[
                ("user_id", "==", user_id),
                ("is_deleted", "==", False),
            ],
            order_by="created_at",
            order_dir="DESCENDING",
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def update_wishlist(self, id: int, user_id: int, **kwargs) -> Optional[WishlistDTO]:
        data = self.get_by_id(id)
        if not data or data.get("is_deleted", False):
            return None

        kwargs["updated_by"] = user_id
        kwargs["updated_at"] = datetime.utcnow()
        kwargs["version"] = (data.get("version") or 0) + 1

        self.collection.document(str(id)).update(kwargs)
        data.update(kwargs)
        return _to_dto(data)

    def soft_delete_wishlist(self, id: int, user_id: int) -> Optional[WishlistDTO]:
        data = self.get_by_id(id)
        if not data or data.get("is_deleted", False):
            return None

        updates = {
            "is_deleted": True,
            "updated_by": user_id,
            "updated_at": datetime.utcnow(),
        }
        self.collection.document(str(id)).update(updates)
        data.update(updates)
        return _to_dto(data)

    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        results = self._query_many(
            filters=[
                ("category_id", "==", category_id),
                ("is_deleted", "==", False),
            ],
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    def get_active_wishlists(self, skip: int = 0, limit: int = 100) -> List[WishlistDTO]:
        results = self._query_many(
            filters=[
                ("is_active", "==", True),
                ("is_deleted", "==", False),
                ("status", "==", "active"),
            ],
            skip=skip,
            limit=limit,
        )
        return [_to_dto(r) for r in results]

    # ---------- field values ----------

    def set_field_values(self, wishlist_id: int, field_values: list) -> None:
        """Replace all field values for a wishlist."""
        fv_col = self._fv_collection(wishlist_id)

        # Delete existing
        existing = list(fv_col.stream())
        batch = self.client.batch()
        for doc in existing:
            batch.delete(doc.reference)
        if existing:
            batch.commit()

        # Create new
        batch = self.client.batch()
        for idx, fv in enumerate(field_values):
            doc_ref = fv_col.document(str(idx + 1))
            fv_data = {
                "id": idx + 1,
                "wishlist_id": wishlist_id,
                "field_definition_id": fv.get("field_definition_id"),
                "value_text": fv.get("value_text"),
                "value_numeric": fv.get("value_numeric"),
                "created_at": datetime.utcnow(),
            }
            batch.set(doc_ref, fv_data)
        if field_values:
            batch.commit()

    def get_field_values(self, wishlist_id: int) -> List[WishlistFieldValueDTO]:
        fv_col = self._fv_collection(wishlist_id)
        docs = list(fv_col.stream())
        return [_fv_to_dto(doc.to_dict()) for doc in docs]

    # ---------- preferred marketplaces ----------

    def set_preferred_marketplaces(self, wishlist_id: int, source_ids: list) -> None:
        """Replace all preferred marketplaces for a wishlist."""
        mp_col = self._mp_collection(wishlist_id)

        # Delete existing
        existing = list(mp_col.stream())
        batch = self.client.batch()
        for doc in existing:
            batch.delete(doc.reference)
        if existing:
            batch.commit()

        # Create new
        batch = self.client.batch()
        for sid in source_ids:
            doc_ref = mp_col.document(str(sid))
            batch.set(doc_ref, {
                "wishlist_id": wishlist_id,
                "marketplace_source_id": sid,
            })
        if source_ids:
            batch.commit()
