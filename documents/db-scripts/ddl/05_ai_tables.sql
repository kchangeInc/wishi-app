-- ============================================================
-- WISHI Database DDL - 05: AI Schema Tables
-- ============================================================

-- Clusters (demand clusters from normalized wishlist filters)
CREATE TABLE ai.clusters (
    id                  SERIAL PRIMARY KEY,
    normalized_filters  VARCHAR(512) UNIQUE NOT NULL,
    display_name        VARCHAR(255),
    description         TEXT,
    category_id         INTEGER REFERENCES public.categories(id),
    subcategory_id      INTEGER REFERENCES public.subcategories(id),
    buyer_count         INTEGER DEFAULT 0,
    is_active           BOOLEAN DEFAULT TRUE,
    is_deleted          BOOLEAN DEFAULT FALSE,
    last_matched_at     TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    created_by          INTEGER REFERENCES core.users(id),
    updated_by          INTEGER REFERENCES core.users(id),
    version             INTEGER DEFAULT 1
);

-- Matches (scraped/aggregated listings scored against wishlist criteria)
CREATE TABLE ai.matches (
    id                      SERIAL PRIMARY KEY,
    cluster_id              INTEGER REFERENCES ai.clusters(id),
    wishlist_id             INTEGER REFERENCES core.wishlists(id) ON DELETE SET NULL,
    marketplace_source_id   INTEGER REFERENCES core.marketplace_sources(id),
    url                     TEXT NOT NULL,
    source                  VARCHAR(100),             -- marketplace name (denormalized)
    title                   VARCHAR(500),
    description             TEXT,
    price                   NUMERIC(12,2),
    formatted_price         VARCHAR(100),
    location                VARCHAR(255),
    image_url               TEXT,
    score                   INTEGER,                   -- match score 0-100
    status                  VARCHAR(50) DEFAULT 'pending',  -- pending, auto_publish, admin_review, published, rejected
    validation_attempts     INTEGER DEFAULT 0,
    last_validation_error   TEXT,
    validation_details      JSONB,                     -- detailed scoring breakdown
    specs                   JSONB,                     -- array of spec strings for display
    seller_tag              VARCHAR(100),              -- 'Verified Seller', 'Top Rated', etc.
    is_featured             BOOLEAN DEFAULT FALSE,
    posted_at               TIMESTAMPTZ,
    is_active               BOOLEAN DEFAULT TRUE,
    is_deleted              BOOLEAN DEFAULT FALSE,
    created_at              TIMESTAMPTZ DEFAULT NOW(),
    updated_at              TIMESTAMPTZ DEFAULT NOW(),
    last_validated_at       TIMESTAMPTZ,
    created_by              INTEGER REFERENCES core.users(id),
    updated_by              INTEGER REFERENCES core.users(id),
    version                 INTEGER DEFAULT 1
);
