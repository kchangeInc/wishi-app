# shared/repository/cluster.py
"""Cluster repository - handles cluster CRUD operations"""

import logging
from sqlalchemy.orm import Session
from shared.models import Cluster
from shared.repository.base import BaseRepository
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ClusterRepository(BaseRepository[Cluster]):
    """Cluster-specific repository"""
    
    def __init__(self, db: Session):
        super().__init__(Cluster, db)
    
    def get_or_create(self, normalized_filters: str, user_id: int = None) -> Cluster:
        """Get existing cluster or create new one"""
        cluster = self.db.query(Cluster).filter(
            Cluster.normalized_filters == normalized_filters,
            Cluster.is_deleted == False
        ).first()
        
        if cluster:
            # Increment buyer count
            cluster.buyer_count = (cluster.buyer_count or 0) + 1
            cluster.updated_at = datetime.utcnow()
            cluster.updated_by = user_id
            self.db.commit()
            self.db.refresh(cluster)
            return cluster
        
        # Create new cluster
        cluster = Cluster(
            normalized_filters=normalized_filters,
            buyer_count=1,
            created_by=user_id,
            updated_by=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(cluster)
        self.db.commit()
        self.db.refresh(cluster)
        return cluster
    
    def get_by_normalized_filters(self, normalized_filters: str) -> Optional[Cluster]:
        """Get cluster by normalized filters"""
        return self.db.query(Cluster).filter(
            Cluster.normalized_filters == normalized_filters,
            Cluster.is_deleted == False
        ).first()
    
    def get_not_deleted(self, id: int) -> Optional[Cluster]:
        """Get cluster by ID, excluding deleted ones"""
        return self.db.query(Cluster).filter(
            Cluster.id == id,
            Cluster.is_deleted == False
        ).first()
    
    def get_active_clusters(self, skip: int = 0, limit: int = 100) -> List[Cluster]:
        """Get active clusters with highest buyer count"""
        return self.db.query(Cluster).filter(
            Cluster.is_active == True,
            Cluster.is_deleted == False
        ).order_by(Cluster.buyer_count.desc()).offset(skip).limit(limit).all()
    
    def update_cluster(self, id: int, user_id: int, **kwargs) -> Optional[Cluster]:
        """Update cluster with user tracking"""
        cluster = self.get_not_deleted(id)
        if cluster:
            kwargs['updated_by'] = user_id
            kwargs['updated_at'] = datetime.utcnow()
            kwargs['version'] = (cluster.version or 0) + 1
            for key, value in kwargs.items():
                setattr(cluster, key, value)
            self.db.commit()
            self.db.refresh(cluster)
        return cluster
    
    def soft_delete_cluster(self, id: int, user_id: int) -> Optional[Cluster]:
        """Soft delete cluster"""
        cluster = self.get_not_deleted(id)
        if cluster:
            cluster.is_deleted = True
            cluster.updated_by = user_id
            cluster.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(cluster)
        return cluster
