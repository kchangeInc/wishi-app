# shared/repository/match.py
"""Match repository - handles match CRUD operations"""

import logging
from sqlalchemy.orm import Session
from shared.models import Match
from shared.repository.base import BaseRepository
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MatchRepository(BaseRepository[Match]):
    """Match-specific repository"""
    
    def __init__(self, db: Session):
        super().__init__(Match, db)
    
    def create_match(self, cluster_id: int, url: str, source: str, 
                     score: int = 0, status: str = "pending", user_id: int = None) -> Match:
        """Create a new match"""
        match = Match(
            cluster_id=cluster_id,
            url=url,
            source=source,
            score=score,
            status=status,
            created_by=user_id,
            updated_by=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_validated_at=datetime.utcnow()
        )
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        return match
    
    def get_by_url(self, url: str) -> Optional[Match]:
        """Get match by URL"""
        return self.db.query(Match).filter(
            Match.url == url,
            Match.is_deleted == False
        ).first()
    
    def get_by_cluster(self, cluster_id: int, skip: int = 0, limit: int = 100) -> List[Match]:
        """Get matches for a cluster"""
        return self.db.query(Match).filter(
            Match.cluster_id == cluster_id,
            Match.is_deleted == False
        ).order_by(Match.score.desc()).offset(skip).limit(limit).all()
    
    def get_pending_validation(self, limit: int = 50) -> List[Match]:
        """Get matches pending validation"""
        return self.db.query(Match).filter(
            Match.status.in_(["auto_publish", "admin_review", "new"]),
            Match.is_deleted == False
        ).order_by(Match.last_validated_at.asc()).limit(limit).all()
    
    def update_match(self, id: int, user_id: int = None, **kwargs) -> Optional[Match]:
        """Update match with user tracking"""
        match = self.get_by_id(id)
        if match:
            kwargs['updated_by'] = user_id
            kwargs['updated_at'] = datetime.utcnow()
            kwargs['version'] = (match.version or 0) + 1
            for key, value in kwargs.items():
                setattr(match, key, value)
            self.db.commit()
            self.db.refresh(match)
        return match
    
    def soft_delete_match(self, id: int, user_id: int) -> Optional[Match]:
        """Soft delete match"""
        match = self.get_by_id(id)
        if match:
            match.is_deleted = True
            match.updated_by = user_id
            match.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(match)
        return match
    
    def get_by_wishlist(self, wishlist_id: int, skip: int = 0, limit: int = 50) -> List[Match]:
        """Get matches for a specific wishlist"""
        return self.db.query(Match).filter(
            Match.wishlist_id == wishlist_id,
            Match.is_deleted == False,
            Match.status.in_(["published", "auto_publish"]),
        ).order_by(Match.score.desc()).offset(skip).limit(limit).all()

    def get_active_matches(self, skip: int = 0, limit: int = 100) -> List[Match]:
        """Get active published matches"""
        return self.db.query(Match).filter(
            Match.status == "published",
            Match.is_active == True,
            Match.is_deleted == False
        ).order_by(Match.score.desc()).offset(skip).limit(limit).all()
