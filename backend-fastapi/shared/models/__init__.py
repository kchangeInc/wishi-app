# shared/models/__init__.py
"""Database models using SQLAlchemy ORM — multi-schema layout"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey,
    Numeric, Date, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# ======================== public (lookup / reference) ========================

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50))
    emoji = Column(String(10))
    color_bg = Column(String(60))
    color_border = Column(String(60))
    color_text = Column(String(60))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subcategories = relationship("Subcategory", back_populates="category", lazy="selectin")


class BannerIdea(Base):
    __tablename__ = "banner_ideas"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("public.categories.id"))
    emoji = Column(String(10), nullable=False)
    text = Column(String(200), nullable=False)
    color_bg = Column(String(60), nullable=False, default="bg-gray-50")
    color_border = Column(String(60), nullable=False, default="border-gray-100")
    color_text = Column(String(60), nullable=False, default="text-gray-600")
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category")


class Subcategory(Base):
    __tablename__ = "subcategories"
    __table_args__ = (
        UniqueConstraint("category_id", "slug"),
        {"schema": "public"},
    )

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("public.categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    icon = Column(String(50))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="subcategories")
    field_definitions = relationship("FieldDefinition", back_populates="subcategory", lazy="selectin")


class FieldDefinition(Base):
    __tablename__ = "field_definitions"
    __table_args__ = (
        UniqueConstraint("subcategory_id", "name"),
        {"schema": "public"},
    )

    id = Column(Integer, primary_key=True)
    subcategory_id = Column(Integer, ForeignKey("public.subcategories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    label = Column(String(100), nullable=False)
    field_type = Column(String(50), nullable=False)
    display_order = Column(Integer, default=0)
    is_required = Column(Boolean, default=False)
    placeholder = Column(String(255))
    options = Column(JSON)
    depends_on = Column(String(100))
    options_by_parent = Column(JSON)
    min_value = Column(Numeric(14, 2))
    max_value = Column(Numeric(14, 2))
    step = Column(Numeric(14, 2))
    unit = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subcategory = relationship("Subcategory", back_populates="field_definitions")


class Country(Base):
    __tablename__ = "countries"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    iso2 = Column(String(2), unique=True)
    iso3 = Column(String(3), unique=True)
    phone_code = Column(String(10))
    currency = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Region(Base):
    __tablename__ = "regions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("public.countries.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class State(Base):
    __tablename__ = "states"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("public.countries.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("public.regions.id"))
    state_code = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Subregion(Base):
    __tablename__ = "subregions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("public.states.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class City(Base):
    __tablename__ = "cities"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=False)
    state_id = Column(Integer, nullable=False)
    state_code = Column(String(255), nullable=False)
    country_id = Column(Integer, nullable=False)
    country_code = Column(String(2), nullable=False)
    type = Column(String(191))
    level = Column(Integer)
    parent_id = Column(Integer)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    native = Column(String(255))
    population = Column(Integer)
    timezone = Column(String(255))
    translations = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    flag = Column(Integer, default=1)
    wikiDataId = Column(String(255))


# ======================== core ========================

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_google_id", "google_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    display_name = Column(String(255))
    google_id = Column(String(255), unique=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(50), ForeignKey("public.roles.name"), default="buyer")
    phone = Column(String(20))
    location = Column(String(255))
    bio = Column(Text)
    avatar_url = Column(Text)
    website = Column(String(255))
    instagram = Column(String(100))
    twitter = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("core.users.id"))
    updated_by = Column(Integer, ForeignKey("core.users.id"))
    version = Column(Integer, default=1)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id"))
    token = Column(String(512), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime)
    revoked_by = Column(Integer, ForeignKey("core.users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarketplaceSource(Base):
    __tablename__ = "marketplace_sources"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    url_template = Column(Text)
    color = Column(String(20))
    logo_url = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MarketplaceSourceCategory(Base):
    __tablename__ = "marketplace_source_categories"
    __table_args__ = (
        UniqueConstraint("marketplace_source_id", "category_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    marketplace_source_id = Column(Integer, ForeignKey("core.marketplace_sources.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("public.categories.id", ondelete="CASCADE"), nullable=False)


class Wishlist(Base):
    __tablename__ = "wishlists"
    __table_args__ = (
        Index("idx_wishlists_user", "user_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id"))
    user_email = Column(String(255))
    title = Column(String(255), nullable=False)
    display_title = Column(String(255))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("public.categories.id"))
    subcategory_id = Column(Integer, ForeignKey("public.subcategories.id"))
    filters_json = Column(JSON)
    notes = Column(Text)
    expiry_date = Column(DateTime)
    status = Column(String(50), default="active")
    priority = Column(String(50), default="medium")
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("core.users.id"))
    updated_by = Column(Integer, ForeignKey("core.users.id"))
    version = Column(Integer, default=1)

    field_values = relationship("WishlistFieldValue", back_populates="wishlist", lazy="selectin")


class WishlistFieldValue(Base):
    __tablename__ = "wishlist_field_values"
    __table_args__ = (
        UniqueConstraint("wishlist_id", "field_definition_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="CASCADE"), nullable=False)
    field_definition_id = Column(Integer, ForeignKey("public.field_definitions.id"), nullable=False)
    value_text = Column(Text)
    value_numeric = Column(Numeric(14, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    wishlist = relationship("Wishlist", back_populates="field_values")


class WishlistPreferredMarketplace(Base):
    __tablename__ = "wishlist_preferred_marketplaces"
    __table_args__ = (
        UniqueConstraint("wishlist_id", "marketplace_source_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="CASCADE"), nullable=False)
    marketplace_source_id = Column(Integer, ForeignKey("core.marketplace_sources.id"), nullable=False)


class Favourite(Base):
    __tablename__ = "favourites"
    __table_args__ = (
        UniqueConstraint("user_id", "match_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(Integer, ForeignKey("ai.matches.id", ondelete="CASCADE"), nullable=False)
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)


class RemovedMatch(Base):
    __tablename__ = "removed_matches"
    __table_args__ = (
        UniqueConstraint("user_id", "match_id"),
        {"schema": "core"},
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    match_id = Column(Integer, ForeignKey("ai.matches.id", ondelete="CASCADE"), nullable=False)
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="SET NULL"))
    reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class SavedListing(Base):
    __tablename__ = "saved_listings"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500))
    url = Column(Text, nullable=False)
    price = Column(String(100))
    price_numeric = Column(Numeric(12, 2))
    location = Column(String(255))
    category = Column(String(100))
    image_url = Column(Text)
    source = Column(String(100))
    saved_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


class NotificationSetting(Base):
    __tablename__ = "notification_settings"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), unique=True, nullable=False)
    email_matches = Column(Boolean, default=True)
    email_price_drops = Column(Boolean, default=True)
    email_newsletter = Column(Boolean, default=False)
    push_matches = Column(Boolean, default=True)
    push_messages = Column(Boolean, default=True)
    push_promotions = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedback"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Offer(Base):
    __tablename__ = "offers"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    seller_user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("public.categories.id"))
    subcategory_id = Column(Integer, ForeignKey("public.subcategories.id"))
    title = Column(String(500), nullable=False)
    description = Column(Text)
    price = Column(Numeric(12, 2))
    location = Column(String(255))
    url = Column(Text)
    image_url = Column(Text)
    status = Column(String(50), default="active")
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = {"schema": "core"}

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("core.offers.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, default=1)
    available = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ======================== ai ========================

class Cluster(Base):
    __tablename__ = "clusters"
    __table_args__ = (
        Index("idx_clusters_normalized_filters", "normalized_filters"),
        {"schema": "ai"},
    )

    id = Column(Integer, primary_key=True)
    normalized_filters = Column(String(512), unique=True, nullable=False)
    display_name = Column(String(255))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("public.categories.id"))
    subcategory_id = Column(Integer, ForeignKey("public.subcategories.id"))
    buyer_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    last_matched_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("core.users.id"))
    updated_by = Column(Integer, ForeignKey("core.users.id"))
    version = Column(Integer, default=1)


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        Index("idx_matches_cluster_id", "cluster_id"),
        Index("idx_matches_status", "status"),
        {"schema": "ai"},
    )

    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey("ai.clusters.id"))
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="SET NULL"))
    marketplace_source_id = Column(Integer, ForeignKey("core.marketplace_sources.id"))
    url = Column(Text, nullable=False)
    source = Column(String(100))
    title = Column(String(500))
    description = Column(Text)
    price = Column(Numeric(12, 2))
    formatted_price = Column(String(100))
    location = Column(String(255))
    image_url = Column(Text)
    score = Column(Integer)
    status = Column(String(50), default="pending")
    validation_attempts = Column(Integer, default=0)
    last_validation_error = Column(Text)
    validation_details = Column(JSON)
    specs = Column(JSON)
    seller_tag = Column(String(100))
    is_featured = Column(Boolean, default=False)
    posted_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_validated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey("core.users.id"))
    updated_by = Column(Integer, ForeignKey("core.users.id"))
    version = Column(Integer, default=1)


# ======================== company ========================

class CompanyUser(Base):
    __tablename__ = "company_users"
    __table_args__ = {"schema": "company"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    department = Column(String(100))
    designation = Column(String(100))
    permissions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("idx_audit_log_table_record", "table_name", "record_id"),
        {"schema": "company"},
    )

    id = Column(Integer, primary_key=True)
    schema_name = Column(String(100))
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    old_values = Column(JSON)
    new_values = Column(JSON)
    user_id = Column(Integer, ForeignKey("core.users.id"))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ======================== analytics ========================

class MatchHistory(Base):
    __tablename__ = "match_history"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="SET NULL"))
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="SET NULL"))
    match_id = Column(Integer, ForeignKey("ai.matches.id", ondelete="SET NULL"))
    action = Column(String(50), nullable=False)
    metadata_ = Column("metadata", JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Click(Base):
    __tablename__ = "clicks"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("ai.matches.id", ondelete="SET NULL"))
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="SET NULL"))
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="SET NULL"))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    referrer = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="SET NULL"))
    event_type = Column(String(100), nullable=False)
    event_data = Column(JSON)
    page = Column(String(255))
    session_id = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProductDemand(Base):
    __tablename__ = "product_demand"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("public.categories.id"))
    subcategory_id = Column(Integer, ForeignKey("public.subcategories.id"))
    city_id = Column(Integer, ForeignKey("public.cities.id"))
    search_count = Column(Integer, default=0)
    wishlist_count = Column(Integer, default=0)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SeoPerformance(Base):
    __tablename__ = "seo_performance"
    __table_args__ = {"schema": "analytics"}

    id = Column(Integer, primary_key=True)
    page_path = Column(String(500), nullable=False)
    page_title = Column(String(300))
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    avg_position = Column(Numeric(5, 2))
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ======================== automation ========================

class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = {"schema": "automation"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    wishlist_id = Column(Integer, ForeignKey("core.wishlists.id", ondelete="SET NULL"))
    match_id = Column(Integer, ForeignKey("ai.matches.id", ondelete="SET NULL"))
    action_url = Column(Text)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Scheduler(Base):
    __tablename__ = "schedulers"
    __table_args__ = {"schema": "automation"}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    task_type = Column(String(100), nullable=False)
    schedule_cron = Column(String(100))
    last_run_at = Column(DateTime)
    next_run_at = Column(DateTime)
    status = Column(String(50), default="active")
    config = Column(JSON)
    error_count = Column(Integer, default=0)
    last_error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ======================== seo ========================

class SeoPage(Base):
    __tablename__ = "seo_pages"
    __table_args__ = {"schema": "seo"}

    id = Column(Integer, primary_key=True)
    slug = Column(String(300), unique=True, nullable=False)
    title = Column(String(300))
    meta_description = Column(Text)
    h1 = Column(String(300))
    content = Column(Text)
    page_type = Column(String(50))
    category_id = Column(Integer, ForeignKey("public.categories.id"))
    city_id = Column(Integer, ForeignKey("public.cities.id"))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeoTracking(Base):
    __tablename__ = "seo_tracking"
    __table_args__ = {"schema": "seo"}

    id = Column(Integer, primary_key=True)
    seo_page_id = Column(Integer, ForeignKey("seo.seo_pages.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)
    referrer = Column(String(500))
    user_agent = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
