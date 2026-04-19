"""Firestore Category repository implementation."""

import logging
from typing import Optional, List

from shared.dto import (
    CategoryDTO, SubcategoryDTO, FieldDefinitionDTO,
    CityDTO, MarketplaceSourceDTO,
)
from shared.repository.firestore import collections as col
from shared.repository.interfaces.category import ICategoryRepository

logger = logging.getLogger(__name__)


def _field_def_to_dto(data: dict) -> FieldDefinitionDTO:
    return FieldDefinitionDTO(
        id=data.get("id", 0),
        subcategory_id=data.get("subcategory_id", 0),
        name=data.get("name", ""),
        label=data.get("label", ""),
        field_type=data.get("field_type", "text"),
        display_order=data.get("display_order", 0),
        is_required=data.get("is_required", False),
        placeholder=data.get("placeholder"),
        options=data.get("options"),
        depends_on=data.get("depends_on"),
        options_by_parent=data.get("options_by_parent"),
        min_value=data.get("min_value"),
        max_value=data.get("max_value"),
        step=data.get("step"),
        unit=data.get("unit"),
        is_active=data.get("is_active", True),
        created_at=data.get("created_at"),
    )


def _subcategory_to_dto(data: dict, field_defs: List[FieldDefinitionDTO] = None) -> SubcategoryDTO:
    return SubcategoryDTO(
        id=data.get("id", 0),
        category_id=data.get("category_id", 0),
        name=data.get("name", ""),
        slug=data.get("slug", ""),
        icon=data.get("icon"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
        created_at=data.get("created_at"),
        field_definitions=field_defs or [],
    )


def _category_to_dto(data: dict, subcategories: List[SubcategoryDTO] = None) -> CategoryDTO:
    return CategoryDTO(
        id=data.get("id", 0),
        name=data.get("name", ""),
        slug=data.get("slug", ""),
        icon=data.get("icon"),
        display_order=data.get("display_order", 0),
        is_active=data.get("is_active", True),
        created_at=data.get("created_at"),
        subcategories=subcategories or [],
    )


def _city_to_dto(data: dict) -> CityDTO:
    return CityDTO(
        id=data.get("id", 0),
        name=data.get("name", ""),
        slug=data.get("slug"),
        state=data.get("state"),
        state_id=data.get("state_id"),
        state_code=data.get("state_code"),
        country_id=data.get("country_id"),
        country_code=data.get("country_code"),
        is_metro=data.get("is_metro", False),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        created_at=data.get("created_at"),
    )


def _marketplace_to_dto(data: dict) -> MarketplaceSourceDTO:
    return MarketplaceSourceDTO(
        id=data.get("id", 0),
        name=data.get("name", ""),
        slug=data.get("slug", ""),
        url_template=data.get("url_template"),
        color=data.get("color"),
        logo_url=data.get("logo_url"),
        is_active=data.get("is_active", True),
        created_at=data.get("created_at"),
        category_ids=data.get("category_ids", []),
    )


class FsCategoryRepository(ICategoryRepository):
    """Firestore implementation of category repository with in-memory caching."""

    def __init__(self, client):
        self.client = client
        self._categories_cache: Optional[List[CategoryDTO]] = None

    def _invalidate_cache(self):
        self._categories_cache = None

    def get_all_categories(self) -> List[CategoryDTO]:
        """Read all categories with nested subcategories and field definitions."""
        if self._categories_cache is not None:
            return self._categories_cache

        cat_col = self.client.collection(col.CATEGORIES)
        cat_docs = list(
            cat_col.where("is_active", "==", True)
            .order_by("display_order")
            .stream()
        )

        categories = []
        for cat_doc in cat_docs:
            cat_data = cat_doc.to_dict()

            # Read subcategories subcollection
            sub_col = cat_doc.reference.collection(col.SUBCATEGORIES)
            sub_docs = list(
                sub_col.where("is_active", "==", True)
                .order_by("display_order")
                .stream()
            )

            subcategories = []
            for sub_doc in sub_docs:
                sub_data = sub_doc.to_dict()

                # Read field_definitions subcollection
                fd_col = sub_doc.reference.collection(col.FIELD_DEFINITIONS)
                fd_docs = list(
                    fd_col.where("is_active", "==", True)
                    .order_by("display_order")
                    .stream()
                )
                field_defs = [_field_def_to_dto(fd.to_dict()) for fd in fd_docs]

                subcategories.append(_subcategory_to_dto(sub_data, field_defs))

            categories.append(_category_to_dto(cat_data, subcategories))

        self._categories_cache = categories
        return categories

    def get_category_by_slug(self, slug: str) -> Optional[CategoryDTO]:
        cat_col = self.client.collection(col.CATEGORIES)
        docs = list(
            cat_col.where("slug", "==", slug)
            .where("is_active", "==", True)
            .limit(1)
            .stream()
        )
        if not docs:
            return None
        return _category_to_dto(docs[0].to_dict())

    def get_category_by_id(self, category_id: int) -> Optional[CategoryDTO]:
        doc = self.client.collection(col.CATEGORIES).document(str(category_id)).get()
        if not doc.exists:
            return None
        return _category_to_dto(doc.to_dict())

    def get_subcategories(self, category_id: int) -> List[SubcategoryDTO]:
        sub_col = (
            self.client.collection(col.CATEGORIES)
            .document(str(category_id))
            .collection(col.SUBCATEGORIES)
        )
        docs = list(
            sub_col.where("is_active", "==", True)
            .order_by("display_order")
            .stream()
        )
        return [_subcategory_to_dto(doc.to_dict()) for doc in docs]

    def get_subcategory_by_slug(self, category_id: int, slug: str) -> Optional[SubcategoryDTO]:
        sub_col = (
            self.client.collection(col.CATEGORIES)
            .document(str(category_id))
            .collection(col.SUBCATEGORIES)
        )
        docs = list(
            sub_col.where("slug", "==", slug)
            .where("is_active", "==", True)
            .limit(1)
            .stream()
        )
        if not docs:
            return None
        return _subcategory_to_dto(docs[0].to_dict())

    def get_fields(self, subcategory_id: int) -> List[FieldDefinitionDTO]:
        """Get field definitions for a subcategory.

        Since field_definitions are stored as subcollections under subcategories,
        we search across all categories to find the matching subcategory.
        """
        # Try to find from cache first
        if self._categories_cache:
            for cat in self._categories_cache:
                for sub in cat.subcategories:
                    if sub.id == subcategory_id:
                        return sub.field_definitions

        # Fall back to querying - iterate category docs to find the subcategory
        cat_col = self.client.collection(col.CATEGORIES)
        cat_docs = list(cat_col.stream())

        for cat_doc in cat_docs:
            sub_ref = cat_doc.reference.collection(col.SUBCATEGORIES).document(str(subcategory_id))
            sub_doc = sub_ref.get()
            if sub_doc.exists:
                fd_col = sub_ref.collection(col.FIELD_DEFINITIONS)
                fd_docs = list(
                    fd_col.where("is_active", "==", True)
                    .order_by("display_order")
                    .stream()
                )
                return [_field_def_to_dto(fd.to_dict()) for fd in fd_docs]

        return []

    def get_all_cities(self, search: str = None, metro_only: bool = False) -> List[CityDTO]:
        """Get cities from the cities collection.

        For case-insensitive search, we use a lowercase stored field 'name_lower'.
        """
        city_col = self.client.collection(col.CITIES)
        query = city_col

        if metro_only:
            query = query.where("is_metro", "==", True)

        if search:
            # Use range query on name_lower for prefix-based case-insensitive search
            search_lower = search.lower()
            query = query.where("name_lower", ">=", search_lower)
            query = query.where("name_lower", "<=", search_lower + "\uf8ff")

        query = query.order_by("name_lower")
        docs = list(query.stream())
        return [_city_to_dto(doc.to_dict()) for doc in docs]

    def get_marketplace_sources(self, category_id: int = None) -> List[MarketplaceSourceDTO]:
        """Get marketplace sources, optionally filtered by category."""
        ms_col = self.client.collection(col.MARKETPLACE_SOURCES)
        query = ms_col.where("is_active", "==", True)

        if category_id:
            query = query.where("category_ids", "array_contains", category_id)

        docs = list(query.stream())
        return [_marketplace_to_dto(doc.to_dict()) for doc in docs]
