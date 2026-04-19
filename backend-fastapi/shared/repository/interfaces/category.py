"""Category repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from shared.dto import CategoryDTO, SubcategoryDTO, FieldDefinitionDTO, CityDTO, MarketplaceSourceDTO


class ICategoryRepository(ABC):

    @abstractmethod
    def get_all_categories(self) -> List[CategoryDTO]:
        ...

    @abstractmethod
    def get_category_by_slug(self, slug: str) -> Optional[CategoryDTO]:
        ...

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Optional[CategoryDTO]:
        ...

    @abstractmethod
    def get_subcategories(self, category_id: int) -> List[SubcategoryDTO]:
        ...

    @abstractmethod
    def get_subcategory_by_slug(self, category_id: int, slug: str) -> Optional[SubcategoryDTO]:
        ...

    @abstractmethod
    def get_fields(self, subcategory_id: int) -> List[FieldDefinitionDTO]:
        ...

    @abstractmethod
    def get_all_cities(self, search: str = None, metro_only: bool = False) -> List[CityDTO]:
        ...

    @abstractmethod
    def get_marketplace_sources(self, category_id: int = None) -> List[MarketplaceSourceDTO]:
        ...
