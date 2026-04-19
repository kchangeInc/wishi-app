# shared/repository/firestore/banner_idea.py
"""Firestore Banner Ideas repository."""

import logging
from datetime import datetime
from typing import List
from shared.dto import BannerIdeaDTO

logger = logging.getLogger(__name__)


class FsBannerIdeaRepository:
    COLLECTION = "banner_ideas"

    def __init__(self, db):
        self.db = db

    def _to_dto(self, doc) -> BannerIdeaDTO:
        d = doc.to_dict()
        return BannerIdeaDTO(
            id=int(doc.id),
            emoji=d.get("emoji", ""),
            text=d.get("text", ""),
            color_bg=d.get("color_bg", "bg-gray-50"),
            color_border=d.get("color_border", "border-gray-100"),
            color_text=d.get("color_text", "text-gray-600"),
            category_id=d.get("category_id"),
            display_order=d.get("display_order", 0),
            is_active=d.get("is_active", True),
            created_at=d.get("created_at"),
        )

    def get_all_active(self) -> List[BannerIdeaDTO]:
        docs = (
            self.db.collection(self.COLLECTION)
            .where("is_active", "==", True)
            .order_by("display_order")
            .stream()
        )
        return [self._to_dto(doc) for doc in docs]

    def get_by_category(self, category_id: int) -> List[BannerIdeaDTO]:
        docs = (
            self.db.collection(self.COLLECTION)
            .where("category_id", "==", category_id)
            .where("is_active", "==", True)
            .order_by("display_order")
            .stream()
        )
        return [self._to_dto(doc) for doc in docs]

    def create(self, emoji: str, text: str, color_bg: str, color_border: str,
               color_text: str, category_id: int = None, display_order: int = 0) -> BannerIdeaDTO:
        data = {
            "emoji": emoji,
            "text": text,
            "color_bg": color_bg,
            "color_border": color_border,
            "color_text": color_text,
            "category_id": category_id,
            "display_order": display_order,
            "is_active": True,
            "created_at": datetime.utcnow(),
        }
        ref = self.db.collection(self.COLLECTION).add(data)
        doc_id = ref[1].id
        return BannerIdeaDTO(id=int(doc_id) if doc_id.isdigit() else 0, **{k: v for k, v in data.items() if k != "created_at"}, created_at=data["created_at"])

    def delete(self, idea_id: int) -> bool:
        doc_ref = self.db.collection(self.COLLECTION).document(str(idea_id))
        doc = doc_ref.get()
        if not doc.exists:
            return False
        doc_ref.update({"is_active": False})
        return True
