# shared/service/wishlist_service.py
"""Wishlist business logic service layer"""

from sqlalchemy.orm import Session
from shared.repository.wishlist import WishlistRepository
from shared.models import Wishlist
from typing import List, Optional, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WishlistService:
    """Wishlist service - handles business logic"""

    def __init__(self, db: Session):
        self.repo = WishlistRepository(db)
        self.db = db

    def create_wishlist(
        self, title: str, user_id: int, user_email: str,
        display_title: str = None, description: str = None,
        category_id: int = None, subcategory_id: int = None,
        filters_json: dict = None, notes: str = None,
        expiry_date: datetime = None,
        status: str = "active", priority: str = "medium",
        field_values: list = None, preferred_marketplace_ids: list = None,
    ) -> Dict:
        logger.info(f"Creating wishlist for user_id={user_id}: {title!r}")
        wishlist = self.repo.create_wishlist(
            title=title, user_id=user_id, user_email=user_email,
            display_title=display_title, description=description,
            category_id=category_id, subcategory_id=subcategory_id,
            filters_json=filters_json, notes=notes,
            expiry_date=expiry_date, status=status, priority=priority,
        )
        if field_values:
            self.repo.set_field_values(wishlist.id, field_values)
        if preferred_marketplace_ids:
            self.repo.set_preferred_marketplaces(wishlist.id, preferred_marketplace_ids)
        return self._wishlist_to_dict(wishlist)

    def get_wishlist(self, wishlist_id: int) -> Optional[Dict]:
        wishlist = self.repo.get_by_id_not_deleted(wishlist_id)
        return self._wishlist_to_dict(wishlist) if wishlist else None

    def get_all_wishlists(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        wishlists = self.repo.get_all_not_deleted(skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]

    def get_user_wishlists(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Dict]:
        wishlists = self.repo.get_by_user(user_id, skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]

    def update_wishlist(
        self, wishlist_id: int, user_id: int,
        title: str = None, description: str = None,
        category_id: int = None, subcategory_id: int = None,
        filters_json: dict = None, notes: str = None,
        status: str = None, priority: str = None,
        field_values: list = None, preferred_marketplace_ids: list = None,
        **kwargs,
    ) -> Optional[Dict]:
        update_data = {}
        if title is not None: update_data["title"] = title
        if description is not None: update_data["description"] = description
        if category_id is not None: update_data["category_id"] = category_id
        if subcategory_id is not None: update_data["subcategory_id"] = subcategory_id
        if filters_json is not None: update_data["filters_json"] = filters_json
        if notes is not None: update_data["notes"] = notes
        if status is not None: update_data["status"] = status
        if priority is not None: update_data["priority"] = priority
        update_data.update(kwargs)

        wishlist = self.repo.update_wishlist(wishlist_id, user_id, **update_data)
        if not wishlist:
            return None
        if field_values is not None:
            self.repo.set_field_values(wishlist_id, field_values)
        if preferred_marketplace_ids is not None:
            self.repo.set_preferred_marketplaces(wishlist_id, preferred_marketplace_ids)
        return self._wishlist_to_dict(wishlist)

    def delete_wishlist(self, wishlist_id: int, user_id: int) -> bool:
        logger.info(f"Deleting wishlist {wishlist_id} for user_id={user_id}")
        wishlist = self.repo.soft_delete_wishlist(wishlist_id, user_id)
        return wishlist is not None

    def get_active_wishlists(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        wishlists = self.repo.get_active_wishlists(skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]

    @staticmethod
    def _wishlist_to_dict(wishlist: Wishlist) -> Dict:
        if not wishlist:
            return None
        result = {
            "id": wishlist.id,
            "title": wishlist.title,
            "display_title": wishlist.display_title,
            "description": wishlist.description,
            "category_id": wishlist.category_id,
            "subcategory_id": wishlist.subcategory_id,
            "filters_json": wishlist.filters_json,
            "notes": wishlist.notes,
            "user_email": wishlist.user_email,
            "user_id": wishlist.user_id,
            "expiry_date": wishlist.expiry_date.isoformat() if wishlist.expiry_date else None,
            "status": wishlist.status,
            "priority": wishlist.priority,
            "is_active": wishlist.is_active,
            "is_deleted": wishlist.is_deleted,
            "created_at": wishlist.created_at.isoformat() if wishlist.created_at else None,
            "updated_at": wishlist.updated_at.isoformat() if wishlist.updated_at else None,
            "created_by": wishlist.created_by,
            "updated_by": wishlist.updated_by,
            "version": wishlist.version,
        }
        if wishlist.field_values:
            result["field_values"] = [
                {
                    "field_definition_id": fv.field_definition_id,
                    "value_text": fv.value_text,
                    "value_numeric": float(fv.value_numeric) if fv.value_numeric else None,
                }
                for fv in wishlist.field_values
            ]
        return result
