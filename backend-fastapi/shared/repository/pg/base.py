# shared/repository/pg/base.py
"""PostgreSQL base repository class for generic CRUD operations"""

from sqlalchemy.orm import Session
from shared.repository.interfaces.base import IBaseRepository
from typing import TypeVar, Generic, List, Optional
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class PgBaseRepository(IBaseRepository[T]):
    def __init__(self, model: T, db: Session):
        self.model = model
        self.db = db

    def create(self, **kwargs) -> T:
        """Create and save new record"""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        logger.debug(f"Created {self.model.__name__} id={instance.id}")
        return instance

    def get_by_id(self, id: int) -> Optional[T]:
        """Get record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: int, **kwargs) -> Optional[T]:
        """Update record by ID"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
            logger.debug(f"Updated {self.model.__name__} id={id}")
        return instance

    def delete(self, id: int) -> bool:
        """Delete record by ID"""
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            logger.debug(f"Deleted {self.model.__name__} id={id}")
            return True
        return False

    def soft_delete(self, id: int, user_id: int = None) -> Optional[T]:
        """Soft delete (mark as deleted)"""
        instance = self.get_by_id(id)
        if instance:
            instance.is_deleted = True
            instance.updated_by = user_id
            self.db.commit()
            self.db.refresh(instance)
            logger.debug(f"Soft-deleted {self.model.__name__} id={id}")
        return instance
