# shared/service/wishlist_service.py
"""Wishlist business logic service layer"""

from sqlalchemy.orm import Session
from shared.repository.wishlist import WishlistRepository
from shared.models import Wishlist
from typing import List, Optional, Dict
from datetime import datetime
import json

class WishlistService:
    """Wishlist service - handles business logic"""
    
    def __init__(self, db: Session):
        self.repo = WishlistRepository(db)
        self.db = db
    
    def create_wishlist(self, title: str, user_id: int, user_email: str,
                       display_title: str = None, description: str = None,
                       category: str = None, subcategory: str = None,
                       filters_json: dict = None, expiry_date: datetime = None,
                       status: str = "active", priority: str = "medium") -> Dict:
        """Create a new wishlist"""
        wishlist = self.repo.create_wishlist(
            title=title,
            user_id=user_id,
            user_email=user_email,
            display_title=display_title,
            description=description,
            category=category,
            subcategory=subcategory,
            filters_json=filters_json,
            expiry_date=expiry_date,
            status=status,
            priority=priority
        )
        return self._wishlist_to_dict(wishlist)
    
    def get_wishlist(self, wishlist_id: int) -> Optional[Dict]:
        """Get wishlist by ID"""
        wishlist = self.repo.get_by_id_not_deleted(wishlist_id)
        return self._wishlist_to_dict(wishlist) if wishlist else None
    
    def get_all_wishlists(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all active wishlists"""
        wishlists = self.repo.get_all_not_deleted(skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]
    
    def get_user_wishlists(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get wishlists for a specific user"""
        wishlists = self.repo.get_by_user(user_id, skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]
    
    def get_wishlist_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get wishlists by category"""
        wishlists = self.repo.get_by_category(category, skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]
    
    def update_wishlist(self, wishlist_id: int, user_id: int, 
                       title: str = None, description: str = None,
                       category: str = None, filters_json: dict = None,
                       status: str = None, priority: str = None,
                       **kwargs) -> Optional[Dict]:
        """Update wishlist"""
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if category is not None:
            update_data['category'] = category
        if filters_json is not None:
            update_data['filters_json'] = filters_json
        if status is not None:
            update_data['status'] = status
        if priority is not None:
            update_data['priority'] = priority
        update_data.update(kwargs)
        
        wishlist = self.repo.update_wishlist(wishlist_id, user_id, **update_data)
        return self._wishlist_to_dict(wishlist) if wishlist else None
    
    def delete_wishlist(self, wishlist_id: int, user_id: int) -> bool:
        """Soft delete wishlist"""
        wishlist = self.repo.soft_delete_wishlist(wishlist_id, user_id)
        return wishlist is not None
    
    def get_active_wishlists(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all active wishlists"""
        wishlists = self.repo.get_active_wishlists(skip, limit)
        return [self._wishlist_to_dict(w) for w in wishlists]
    
    @staticmethod
    def _wishlist_to_dict(wishlist: Wishlist) -> Dict:
        """Convert wishlist ORM to dictionary"""
        if not wishlist:
            return None
        return {
            "id": wishlist.id,
            "title": wishlist.title,
            "display_title": wishlist.display_title,
            "description": wishlist.description,
            "category": wishlist.category,
            "subcategory": wishlist.subcategory,
            "filters_json": wishlist.filters_json,
            "user_email": wishlist.user_email,
            "user_id": wishlist.user_id,
            "expiry_date": wishlist.expiry_date,
            "status": wishlist.status,
            "priority": wishlist.priority,
            "is_active": wishlist.is_active,
            "is_deleted": wishlist.is_deleted,
            "created_at": wishlist.created_at,
            "updated_at": wishlist.updated_at,
            "created_by": wishlist.created_by,
            "updated_by": wishlist.updated_by,
            "version": wishlist.version
        }
