# shared/repository/wishlist.py
"""Wishlist repository - handles all wishlist CRUD operations"""

import logging
from sqlalchemy.orm import Session
from shared.models import Wishlist, WishlistFieldValue, WishlistPreferredMarketplace

logger = logging.getLogger(__name__)
from shared.repository.base import BaseRepository
from typing import List, Optional
from datetime import datetime


class WishlistRepository(BaseRepository[Wishlist]):
    """Wishlist-specific repository with custom queries"""

    def __init__(self, db: Session):
        super().__init__(Wishlist, db)

    def create_wishlist(self, title: str, user_id: int, user_email: str, **kwargs) -> Wishlist:
        wishlist = Wishlist(
            title=title,
            user_id=user_id,
            user_email=user_email,
            created_by=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **kwargs,
        )
        self.db.add(wishlist)
        self.db.commit()
        self.db.refresh(wishlist)
        return wishlist

    def get_by_id_not_deleted(self, id: int) -> Optional[Wishlist]:
        return self.db.query(Wishlist).filter(Wishlist.id == id, Wishlist.is_deleted == False).first()

    def get_all_not_deleted(self, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        return (
            self.db.query(Wishlist)
            .filter(Wishlist.is_deleted == False)
            .offset(skip).limit(limit).all()
        )

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        return (
            self.db.query(Wishlist)
            .filter(Wishlist.user_id == user_id, Wishlist.is_deleted == False)
            .order_by(Wishlist.created_at.desc())
            .offset(skip).limit(limit).all()
        )

    def update_wishlist(self, id: int, user_id: int, **kwargs) -> Optional[Wishlist]:
        wishlist = self.get_by_id_not_deleted(id)
        if wishlist:
            kwargs["updated_by"] = user_id
            kwargs["updated_at"] = datetime.utcnow()
            kwargs["version"] = (wishlist.version or 0) + 1
            for key, value in kwargs.items():
                setattr(wishlist, key, value)
            self.db.commit()
            self.db.refresh(wishlist)
        return wishlist

    def soft_delete_wishlist(self, id: int, user_id: int) -> Optional[Wishlist]:
        wishlist = self.get_by_id_not_deleted(id)
        if wishlist:
            wishlist.is_deleted = True
            wishlist.updated_by = user_id
            wishlist.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(wishlist)
        return wishlist

    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        return (
            self.db.query(Wishlist)
            .filter(Wishlist.category_id == category_id, Wishlist.is_deleted == False)
            .offset(skip).limit(limit).all()
        )

    def get_active_wishlists(self, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        return (
            self.db.query(Wishlist)
            .filter(Wishlist.is_active == True, Wishlist.is_deleted == False, Wishlist.status == "active")
            .offset(skip).limit(limit).all()
        )

    # ---------- field values ----------

    def set_field_values(self, wishlist_id: int, field_values: list[dict]) -> None:
        """Replace all field values for a wishlist. Each dict: {field_definition_id, value_text?, value_numeric?}"""
        self.db.query(WishlistFieldValue).filter(WishlistFieldValue.wishlist_id == wishlist_id).delete()
        for fv in field_values:
            self.db.add(WishlistFieldValue(wishlist_id=wishlist_id, **fv))
        self.db.commit()

    def get_field_values(self, wishlist_id: int) -> List[WishlistFieldValue]:
        return self.db.query(WishlistFieldValue).filter(WishlistFieldValue.wishlist_id == wishlist_id).all()

    # ---------- preferred marketplaces ----------

    def set_preferred_marketplaces(self, wishlist_id: int, source_ids: list[int]) -> None:
        self.db.query(WishlistPreferredMarketplace).filter(
            WishlistPreferredMarketplace.wishlist_id == wishlist_id
        ).delete()
        for sid in source_ids:
            self.db.add(WishlistPreferredMarketplace(wishlist_id=wishlist_id, marketplace_source_id=sid))
        self.db.commit()
