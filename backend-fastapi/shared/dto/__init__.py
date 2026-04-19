"""Data Transfer Objects shared across all database backends."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Any


@dataclass
class UserDTO:
    id: int
    email: str
    name: Optional[str] = None
    display_name: Optional[str] = None
    google_id: Optional[str] = None
    password_hash: Optional[str] = None
    role: str = "buyer"
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    website: Optional[str] = None
    instagram: Optional[str] = None
    twitter: Optional[str] = None
    is_active: bool = True
    is_deleted: bool = False
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int = 1


@dataclass
class RefreshTokenDTO:
    id: int
    user_id: int
    token: str
    expires_at: datetime
    revoked: bool = False
    revoked_at: Optional[datetime] = None
    revoked_by: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class WishlistFieldValueDTO:
    id: int
    wishlist_id: int
    field_definition_id: int
    value_text: Optional[str] = None
    value_numeric: Optional[float] = None
    created_at: Optional[datetime] = None


@dataclass
class WishlistDTO:
    id: int
    user_id: int
    title: str
    user_email: Optional[str] = None
    display_title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    filters_json: Optional[dict] = None
    notes: Optional[str] = None
    expiry_date: Optional[datetime] = None
    status: str = "active"
    priority: str = "medium"
    is_active: bool = True
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int = 1
    field_values: List[WishlistFieldValueDTO] = field(default_factory=list)


@dataclass
class ClusterDTO:
    id: int
    normalized_filters: str
    buyer_count: int = 0
    display_name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    is_active: bool = True
    is_deleted: bool = False
    last_matched_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int = 1


@dataclass
class MatchDTO:
    id: int
    url: str
    cluster_id: Optional[int] = None
    wishlist_id: Optional[int] = None
    marketplace_source_id: Optional[int] = None
    source: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    formatted_price: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    score: Optional[int] = None
    status: str = "pending"
    validation_attempts: int = 0
    last_validation_error: Optional[str] = None
    validation_details: Optional[dict] = None
    specs: Optional[dict] = None
    seller_tag: Optional[str] = None
    is_featured: bool = False
    posted_at: Optional[datetime] = None
    is_active: bool = True
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_validated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    version: int = 1


@dataclass
class FieldDefinitionDTO:
    id: int
    subcategory_id: int
    name: str
    label: str
    field_type: str
    display_order: int = 0
    is_required: bool = False
    placeholder: Optional[str] = None
    options: Optional[Any] = None
    depends_on: Optional[str] = None
    options_by_parent: Optional[Any] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None
    unit: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None


@dataclass
class SubcategoryDTO:
    id: int
    category_id: int
    name: str
    slug: str
    icon: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    field_definitions: List[FieldDefinitionDTO] = field(default_factory=list)


@dataclass
class CategoryDTO:
    id: int
    name: str
    slug: str
    icon: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    subcategories: List[SubcategoryDTO] = field(default_factory=list)


@dataclass
class CityDTO:
    id: int
    name: str
    slug: Optional[str] = None
    state: Optional[str] = None
    state_id: Optional[int] = None
    state_code: Optional[str] = None
    country_id: Optional[int] = None
    country_code: Optional[str] = None
    is_metro: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: Optional[datetime] = None


@dataclass
class MarketplaceSourceDTO:
    id: int
    name: str
    slug: str
    url_template: Optional[str] = None
    color: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    category_ids: List[int] = field(default_factory=list)


@dataclass
class FavouriteDTO:
    id: int
    user_id: int
    match_id: int
    wishlist_id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class RemovedMatchDTO:
    id: int
    user_id: int
    match_id: int
    wishlist_id: Optional[int] = None
    reason: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class SavedListingDTO:
    id: int
    user_id: int
    url: str
    title: Optional[str] = None
    price: Optional[str] = None
    price_numeric: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    source: Optional[str] = None
    saved_at: Optional[datetime] = None
    is_deleted: bool = False


@dataclass
class NotificationDTO:
    id: int
    user_id: int
    type: str
    title: str
    description: Optional[str] = None
    wishlist_id: Optional[int] = None
    match_id: Optional[int] = None
    action_url: Optional[str] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    is_deleted: bool = False
    created_at: Optional[datetime] = None


@dataclass
class NotificationSettingDTO:
    id: int
    user_id: int
    email_matches: bool = True
    email_price_drops: bool = True
    email_newsletter: bool = False
    push_matches: bool = True
    push_messages: bool = True
    push_promotions: bool = False
    updated_at: Optional[datetime] = None


@dataclass
class FeedbackDTO:
    id: int
    user_id: int
    rating: int
    message: Optional[str] = None
    created_at: Optional[datetime] = None
