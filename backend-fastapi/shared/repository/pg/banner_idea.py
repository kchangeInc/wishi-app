# shared/repository/pg/banner_idea.py
"""PostgreSQL Banner Ideas repository."""

import logging
from sqlalchemy.orm import Session
from shared.models import BannerIdea
from typing import List, Optional

logger = logging.getLogger(__name__)


class PgBannerIdeaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_active(self) -> List[BannerIdea]:
        return (
            self.db.query(BannerIdea)
            .filter(BannerIdea.is_active == True)
            .order_by(BannerIdea.display_order)
            .all()
        )

    def get_by_category(self, category_id: int) -> List[BannerIdea]:
        return (
            self.db.query(BannerIdea)
            .filter(BannerIdea.category_id == category_id, BannerIdea.is_active == True)
            .order_by(BannerIdea.display_order)
            .all()
        )

    def create(self, emoji: str, text: str, color_bg: str, color_border: str,
               color_text: str, category_id: int = None, display_order: int = 0) -> BannerIdea:
        idea = BannerIdea(
            emoji=emoji,
            text=text,
            color_bg=color_bg,
            color_border=color_border,
            color_text=color_text,
            category_id=category_id,
            display_order=display_order,
        )
        self.db.add(idea)
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def delete(self, idea_id: int) -> bool:
        idea = self.db.query(BannerIdea).filter(BannerIdea.id == idea_id).first()
        if not idea:
            return False
        idea.is_active = False
        self.db.commit()
        return True
