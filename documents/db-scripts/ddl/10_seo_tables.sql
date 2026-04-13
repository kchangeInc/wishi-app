-- ============================================================
-- WISHI Database DDL - 10: SEO Schema Tables
-- ============================================================

-- SEO pages (programmatic/static pages for search engine indexing)
CREATE TABLE seo.seo_pages (
    id                SERIAL PRIMARY KEY,
    slug              VARCHAR(300) UNIQUE NOT NULL,
    title             VARCHAR(300),
    meta_description  TEXT,
    h1                VARCHAR(300),
    content           TEXT,
    page_type         VARCHAR(50),                   -- category, city, subcategory, landing, blog
    category_id       INTEGER REFERENCES public.categories(id),
    city_id           INTEGER REFERENCES public.cities(id),
    is_published      BOOLEAN DEFAULT FALSE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);

-- SEO event tracking (page views, clicks from search)
CREATE TABLE seo.seo_tracking (
    id            SERIAL PRIMARY KEY,
    seo_page_id   INTEGER NOT NULL REFERENCES seo.seo_pages(id) ON DELETE CASCADE,
    event_type    VARCHAR(50) NOT NULL,              -- page_view, click, impression
    referrer      VARCHAR(500),
    user_agent    TEXT,
    ip_address    VARCHAR(45),
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
