# shared/repository/pg/favourite.py
"""PostgreSQL Favourite + RemovedMatch repository"""

import logging
from sqlalchemy.orm import Session
from shared.models import Favourite, RemovedMatch
from shared.repository.interfaces.favourite import IFavouriteRepository
from typing import List, Optional, Set
from datetime import datetime

logger = logging.getLogger(__name__)


class PgFavouriteRepository(IFavouriteRepository):
    def __init__(self, db: Session):
        self.db = db

    # ---------- favourites ----------

    def add_favourite(self, user_id: int, match_id: int, wishlist_id: int = None) -> Favourite:
        fav = Favourite(user_id=user_id, match_id=match_id, wishlist_id=wishlist_id)
        self.db.add(fav)
        self.db.commit()
        self.db.refresh(fav)
        return fav

    def remove_favourite(self, user_id: int, match_id: int) -> bool:
        fav = self.db.query(Favourite).filter(
            Favourite.user_id == user_id, Favourite.match_id == match_id
        ).first()
        if fav:
            self.db.delete(fav)
            self.db.commit()
            return True
        return False

    def get_user_favourites(self, user_id: int, wishlist_id: int = None) -> List[Favourite]:
        q = self.db.query(Favourite).filter(Favourite.user_id == user_id)
        if wishlist_id:
            q = q.filter(Favourite.wishlist_id == wishlist_id)
        return q.order_by(Favourite.created_at.desc()).all()

    def get_favourite_match_ids(self, user_id: int, wishlist_id: int = None) -> Set[int]:
        q = self.db.query(Favourite.match_id).filter(Favourite.user_id == user_id)
        if wishlist_id:
            q = q.filter(Favourite.wishlist_id == wishlist_id)
        return {row[0] for row in q.all()}

    # ---------- removed / dismissed ----------

    def dismiss_match(self, user_id: int, match_id: int, wishlist_id: int = None, reason: str = None) -> RemovedMatch:
        rm = RemovedMatch(user_id=user_id, match_id=match_id, wishlist_id=wishlist_id, reason=reason)
        self.db.add(rm)
        self.db.commit()
        self.db.refresh(rm)
        return rm

    def get_dismissed_match_ids(self, user_id: int, wishlist_id: int = None) -> Set[int]:
        q = self.db.query(RemovedMatch.match_id).filter(RemovedMatch.user_id == user_id)
        if wishlist_id:
            q = q.filter(RemovedMatch.wishlist_id == wishlist_id)
        return {row[0] for row in q.all()}
