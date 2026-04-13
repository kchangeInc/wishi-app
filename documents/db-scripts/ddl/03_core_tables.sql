-- ============================================================
-- WISHI Database DDL - 03: Core Schema Tables
-- ============================================================
-- Combines: users + refresh_tokens (from shared) + all buyer + all seller tables

-- Users
CREATE TABLE core.users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    name            VARCHAR(255),
    display_name    VARCHAR(255),
    google_id       VARCHAR(255) UNIQUE,
    password_hash   VARCHAR(255),
    role            VARCHAR(50) DEFAULT 'buyer' REFERENCES public.roles(name),
    phone           VARCHAR(20),
    location        VARCHAR(255),
    bio             TEXT,
    avatar_url      TEXT,
    website         VARCHAR(512),
    instagram       VARCHAR(255),
    twitter         VARCHAR(255),
    is_active       BOOLEAN DEFAULT TRUE,
    is_deleted      BOOLEAN DEFAULT FALSE,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    created_by      INTEGER,
    updated_by      INTEGER,
    version         INTEGER DEFAULT 1
);

-- Refresh tokens
CREATE TABLE core.refresh_tokens (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    token       VARCHAR(512) UNIQUE NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    revoked     BOOLEAN DEFAULT FALSE,
    revoked_at  TIMESTAMPTZ,
    revoked_by  INTEGER REFERENCES core.users(id),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Marketplace sources (external platforms we scrape)
CREATE TABLE core.marketplace_sources (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    slug          VARCHAR(100) NOT NULL,
    url_template  TEXT,                              -- e.g. 'https://www.olx.in/items/q-{q}'
    color         VARCHAR(10),                       -- hex color for UI badges
    logo_url      TEXT,
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(slug)
);

-- Marketplace sources ↔ categories (many-to-many)
CREATE TABLE core.marketplace_source_categories (
    id                     SERIAL PRIMARY KEY,
    marketplace_source_id  INTEGER NOT NULL REFERENCES core.marketplace_sources(id) ON DELETE CASCADE,
    category_id            INTEGER NOT NULL REFERENCES public.categories(id) ON DELETE CASCADE,
    UNIQUE(marketplace_source_id, category_id)
);

-- Wishlists
CREATE TABLE core.wishlists (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    user_email        VARCHAR(255),
    title             VARCHAR(255),
    display_title     VARCHAR(255),
    description       TEXT,
    category_id       INTEGER NOT NULL REFERENCES public.categories(id),
    subcategory_id    INTEGER NOT NULL REFERENCES public.subcategories(id),
    filters_json      JSONB,                        -- denormalized cache of field values
    notes             TEXT,
    expiry_date       TIMESTAMPTZ,
    status            VARCHAR(50) DEFAULT 'active',  -- active, expired, paused, deleted
    priority          VARCHAR(50) DEFAULT 'medium',  -- low, medium, high
    is_active         BOOLEAN DEFAULT TRUE,
    is_deleted        BOOLEAN DEFAULT FALSE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW(),
    created_by        INTEGER REFERENCES core.users(id),
    updated_by        INTEGER REFERENCES core.users(id),
    version           INTEGER DEFAULT 1
);

-- Wishlist field values (EAV for dynamic fields)
CREATE TABLE core.wishlist_field_values (
    id                  SERIAL PRIMARY KEY,
    wishlist_id         INTEGER NOT NULL REFERENCES core.wishlists(id) ON DELETE CASCADE,
    field_definition_id INTEGER NOT NULL REFERENCES public.field_definitions(id),
    value_text          TEXT,                         -- string value (all types serialized as text)
    value_numeric       NUMERIC,                     -- numeric value for sliders/numbers (enables range queries)
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(wishlist_id, field_definition_id)
);

-- Wishlist preferred marketplaces (many-to-many)
CREATE TABLE core.wishlist_preferred_marketplaces (
    id                     SERIAL PRIMARY KEY,
    wishlist_id            INTEGER NOT NULL REFERENCES core.wishlists(id) ON DELETE CASCADE,
    marketplace_source_id  INTEGER NOT NULL REFERENCES core.marketplace_sources(id),
    UNIQUE(wishlist_id, marketplace_source_id)
);

-- Favourites (user favourites a match)
CREATE TABLE core.favourites (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    match_id    INTEGER NOT NULL REFERENCES ai.matches(id) ON DELETE CASCADE,
    wishlist_id INTEGER REFERENCES core.wishlists(id) ON DELETE SET NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, match_id)
);

-- Removed/dismissed matches
CREATE TABLE core.removed_matches (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    match_id    INTEGER NOT NULL REFERENCES ai.matches(id) ON DELETE CASCADE,
    wishlist_id INTEGER REFERENCES core.wishlists(id) ON DELETE SET NULL,
    reason      VARCHAR(255),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, match_id)
);

-- Saved external listings (bookmarked by user)
CREATE TABLE core.saved_listings (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    title       VARCHAR(500) NOT NULL,
    url         TEXT,
    price       VARCHAR(100),
    price_numeric NUMERIC,
    location    VARCHAR(255),
    category    VARCHAR(100),
    image_url   TEXT,
    source      VARCHAR(100),
    saved_at    TIMESTAMPTZ DEFAULT NOW(),
    is_deleted  BOOLEAN DEFAULT FALSE
);

-- Per-user notification preferences
CREATE TABLE core.notification_settings (
    id                SERIAL PRIMARY KEY,
    user_id           INTEGER UNIQUE NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    email_matches     BOOLEAN DEFAULT TRUE,
    email_price_drops BOOLEAN DEFAULT TRUE,
    email_newsletter  BOOLEAN DEFAULT FALSE,
    push_matches      BOOLEAN DEFAULT TRUE,
    push_messages     BOOLEAN DEFAULT TRUE,
    push_promotions   BOOLEAN DEFAULT FALSE,
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);

-- User feedback
CREATE TABLE core.feedback (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    rating     INTEGER CHECK (rating BETWEEN 1 AND 5),
    message    TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seller offers (future: seller-pushed listings)
CREATE TABLE core.offers (
    id              SERIAL PRIMARY KEY,
    seller_user_id  INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    url             TEXT,
    price           NUMERIC(12,2),
    category_id     INTEGER REFERENCES public.categories(id),
    subcategory_id  INTEGER REFERENCES public.subcategories(id),
    location        VARCHAR(255),
    image_url       TEXT,
    status          VARCHAR(50) DEFAULT 'draft',      -- draft, active, paused, expired
    is_active       BOOLEAN DEFAULT TRUE,
    is_deleted      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    created_by      INTEGER REFERENCES core.users(id),
    updated_by      INTEGER REFERENCES core.users(id),
    version         INTEGER DEFAULT 1
);

-- Seller inventory (future)
CREATE TABLE core.inventory (
    id          SERIAL PRIMARY KEY,
    offer_id    INTEGER NOT NULL REFERENCES core.offers(id) ON DELETE CASCADE,
    quantity    INTEGER DEFAULT 1,
    available   BOOLEAN DEFAULT TRUE,
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
