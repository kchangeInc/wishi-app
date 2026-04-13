-- ============================================================
-- WISHI Database DDL - 07: Analytics Schema Tables
-- ============================================================

-- Match history (records when matches are surfaced/interacted with)
CREATE TABLE analytics.match_history (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES core.users(id) ON DELETE SET NULL,
    wishlist_id INTEGER REFERENCES core.wishlists(id) ON DELETE SET NULL,
    match_id    INTEGER REFERENCES ai.matches(id) ON DELETE SET NULL,
    action      VARCHAR(50) NOT NULL,                -- viewed, clicked, favourited, dismissed
    metadata    JSONB,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Click tracking (outbound clicks to marketplace URLs)
CREATE TABLE analytics.clicks (
    id          SERIAL PRIMARY KEY,
    match_id    INTEGER REFERENCES ai.matches(id) ON DELETE SET NULL,
    user_id     INTEGER REFERENCES core.users(id) ON DELETE SET NULL,
    wishlist_id INTEGER REFERENCES core.wishlists(id) ON DELETE SET NULL,
    ip_address  VARCHAR(45),
    user_agent  TEXT,
    referrer    TEXT,
    timestamp   TIMESTAMPTZ DEFAULT NOW()
);

-- Generic event tracking
CREATE TABLE analytics.events (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES core.users(id) ON DELETE SET NULL,
    event_type  VARCHAR(100) NOT NULL,               -- page_view, search, wishlist_create, match_click, etc.
    event_data  JSONB,                               -- event-specific payload
    page        VARCHAR(255),
    session_id  VARCHAR(255),
    ip_address  VARCHAR(45),
    user_agent  TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Product demand aggregation
CREATE TABLE analytics.product_demand (
    id              SERIAL PRIMARY KEY,
    category_id     INTEGER REFERENCES public.categories(id),
    subcategory_id  INTEGER REFERENCES public.subcategories(id),
    city_id         INTEGER REFERENCES public.cities(id),
    search_count    INTEGER DEFAULT 0,
    wishlist_count  INTEGER DEFAULT 0,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- SEO performance metrics (from Search Console / analytics)
CREATE TABLE analytics.seo_performance (
    id            SERIAL PRIMARY KEY,
    page_path     VARCHAR(500) NOT NULL,
    page_title    VARCHAR(300),
    impressions   INTEGER DEFAULT 0,
    clicks        INTEGER DEFAULT 0,
    avg_position  DECIMAL(5,2),
    period_start  DATE NOT NULL,
    period_end    DATE NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
