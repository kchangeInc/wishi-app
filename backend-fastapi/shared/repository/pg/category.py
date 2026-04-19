# shared/repository/pg/category.py
"""PostgreSQL Category / Subcategory / FieldDefinition / City / MarketplaceSource read repos"""

import logging
from sqlalchemy.orm import Session
from shared.models import Category, Subcategory, FieldDefinition, City, MarketplaceSource, MarketplaceSourceCategory
from shared.repository.interfaces.category import ICategoryRepository
from typing import List, Optional

logger = logging.getLogger(__name__)


class PgCategoryRepository(ICategoryRepository):
    def __init__(self, db: Session):
        self.db = db

    # ---------- categories ----------

    def get_all_categories(self) -> List[Category]:
        return (
            self.db.query(Category)
            .filter(Category.is_active == True)
            .order_by(Category.display_order)
            .all()
        )

    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.slug == slug, Category.is_active == True).first()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    # ---------- subcategories ----------

    def get_subcategories(self, category_id: int) -> List[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.category_id == category_id, Subcategory.is_active == True)
            .order_by(Subcategory.display_order)
            .all()
        )

    def get_subcategory_by_slug(self, category_id: int, slug: str) -> Optional[Subcategory]:
        return (
            self.db.query(Subcategory)
            .filter(Subcategory.category_id == category_id, Subcategory.slug == slug, Subcategory.is_active == True)
            .first()
        )

    # ---------- field definitions ----------

    def get_fields(self, subcategory_id: int) -> List[FieldDefinition]:
        return (
            self.db.query(FieldDefinition)
            .filter(FieldDefinition.subcategory_id == subcategory_id, FieldDefinition.is_active == True)
            .order_by(FieldDefinition.display_order)
            .all()
        )

    # ---------- cities ----------

    def get_all_cities(self, search: str = None, metro_only: bool = False) -> List[City]:
        q = self.db.query(City).filter(City.is_active == True)
        if metro_only:
            q = q.filter(City.is_metro == True)
        if search:
            q = q.filter(City.name.ilike(f"%{search}%"))
        return q.order_by(City.display_order).all()

    # ---------- marketplace sources ----------

    def get_marketplace_sources(self, category_id: int = None) -> List[MarketplaceSource]:
        if category_id:
            return (
                self.db.query(MarketplaceSource)
                .join(MarketplaceSourceCategory)
                .filter(
                    MarketplaceSourceCategory.category_id == category_id,
                    MarketplaceSource.is_active == True,
                )
                .all()
            )
        return self.db.query(MarketplaceSource).filter(MarketplaceSource.is_active == True).all()
