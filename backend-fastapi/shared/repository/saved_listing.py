# shared/repository/saved_listing.py
"""SavedListing repository"""

import logging
from sqlalchemy.orm import Session
from shared.models import SavedListing
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SavedListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_listing(self, user_id: int, **kwargs) -> SavedListing:
        listing = SavedListing(user_id=user_id, **kwargs)
        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def get_user_saved(self, user_id: int, skip: int = 0, limit: int = 50) -> List[SavedListing]:
        return (
            self.db.query(SavedListing)
            .filter(SavedListing.user_id == user_id, SavedListing.is_deleted == False)
            .order_by(SavedListing.saved_at.desc())
            .offset(skip).limit(limit)
            .all()
        )

    def delete_saved(self, listing_id: int, user_id: int) -> bool:
        listing = self.db.query(SavedListing).filter(
            SavedListing.id == listing_id, SavedListing.user_id == user_id
        ).first()
        if listing:
            listing.is_deleted = True
            self.db.commit()
            return True
        return False
