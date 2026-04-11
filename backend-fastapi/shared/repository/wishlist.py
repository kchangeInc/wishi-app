# shared/repository/wishlist.py
"""Wishlist repository - handles all wishlist CRUD operations"""

from sqlalchemy.orm import Session
from shared.models import Wishlist
from shared.repository.base import BaseRepository
from typing import List, Optional
from datetime import datetime
import json

class WishlistRepository(BaseRepository[Wishlist]):
    """Wishlist-specific repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(Wishlist, db)
    
    def create_wishlist(self, title: str, user_id: int, user_email: str, **kwargs) -> Wishlist:
        """Create a new wishlist with user tracking"""
        wishlist = Wishlist(
            title=title,
            user_id=user_id,
            user_email=user_email,
            created_by=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            **kwargs
        )
        self.db.add(wishlist)
        self.db.commit()
        self.db.refresh(wishlist)
        return wishlist
    
    def get_by_id_not_deleted(self, id: int) -> Optional[Wishlist]:
        """Get wishlist by ID, excluding deleted ones"""
        return self.db.query(Wishlist).filter(
            Wishlist.id == id,
            Wishlist.is_deleted == False
        ).first()
    
    def get_all_not_deleted(self, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        """Get all non-deleted wishlists"""
        return self.db.query(Wishlist).filter(
            Wishlist.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        """Get wishlists for a specific user"""
        return self.db.query(Wishlist).filter(
            Wishlist.user_id == user_id,
            Wishlist.is_deleted == False
        ).offset(skip).limit(limit).order_by(Wishlist.created_at.desc()).all()
    
    def update_wishlist(self, id: int, user_id: int, **kwargs) -> Optional[Wishlist]:
        """Update wishlist with user tracking"""
        wishlist = self.get_by_id_not_deleted(id)
        if wishlist:
            kwargs['updated_by'] = user_id
            kwargs['updated_at'] = datetime.utcnow()
            kwargs['version'] = (wishlist.version or 0) + 1
            for key, value in kwargs.items():
                setattr(wishlist, key, value)
            self.db.commit()
            self.db.refresh(wishlist)
        return wishlist
    
    def soft_delete_wishlist(self, id: int, user_id: int) -> Optional[Wishlist]:
        """Soft delete wishlist with user tracking"""
        wishlist = self.get_by_id_not_deleted(id)
        if wishlist:
            wishlist.is_deleted = True
            wishlist.updated_by = user_id
            wishlist.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(wishlist)
        return wishlist
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        """Get wishlists by category"""
        return self.db.query(Wishlist).filter(
            Wishlist.category == category,
            Wishlist.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def get_active_wishlists(self, skip: int = 0, limit: int = 100) -> List[Wishlist]:
        """Get active wishlists (not expired, active status)"""
        return self.db.query(Wishlist).filter(
            Wishlist.is_active == True,
            Wishlist.is_deleted == False,
            Wishlist.status == "active"
        ).offset(skip).limit(limit).all()
