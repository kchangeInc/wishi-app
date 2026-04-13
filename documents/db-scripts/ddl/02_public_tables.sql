-- ============================================================
-- WISHI Database DDL - 02: Public Schema Tables (lookup/reference)
-- ============================================================

-- Roles lookup
CREATE TABLE public.roles (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) UNIQUE NOT NULL,   -- buyer, seller, admin
    description TEXT,
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Categories
CREATE TABLE public.categories (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) UNIQUE NOT NULL,
    slug          VARCHAR(100) UNIQUE NOT NULL,
    icon          VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Subcategories
CREATE TABLE public.subcategories (
    id            SERIAL PRIMARY KEY,
    category_id   INTEGER NOT NULL REFERENCES public.categories(id) ON DELETE CASCADE,
    name          VARCHAR(100) NOT NULL,
    slug          VARCHAR(100) NOT NULL,
    icon          VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(category_id, slug)
);

-- Dynamic field definitions (meta-schema for wishlist forms)
CREATE TABLE public.field_definitions (
    id                SERIAL PRIMARY KEY,
    subcategory_id    INTEGER NOT NULL REFERENCES public.subcategories(id) ON DELETE CASCADE,
    name              VARCHAR(100) NOT NULL,       -- e.g. 'brand', 'price', 'location'
    label             VARCHAR(255) NOT NULL,        -- e.g. 'Brand', 'Price (up to)'
    field_type        VARCHAR(50) NOT NULL,          -- select, slider, text, number, toggle, autocomplete
    display_order     INTEGER DEFAULT 0,
    is_required       BOOLEAN DEFAULT FALSE,
    placeholder       VARCHAR(255),
    options           JSONB,                         -- array of string options for select/autocomplete
    depends_on        VARCHAR(100),                  -- name of parent field (e.g. 'brand' for model)
    options_by_parent JSONB,                         -- { "parent_value": ["child_option", ...] }
    min_value         NUMERIC,                       -- for slider type
    max_value         NUMERIC,                       -- for slider type
    step              NUMERIC,                       -- for slider type
    unit              VARCHAR(20),                   -- e.g. '₹', '₹/mo'
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(subcategory_id, name)
);

-- Countries
CREATE TABLE public.countries (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    iso2        CHAR(2) UNIQUE,
    iso3        CHAR(3) UNIQUE,
    phone_code  VARCHAR(10),
    currency    VARCHAR(10),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Regions (geographic grouping within a country)
CREATE TABLE public.regions (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    country_id  INTEGER NOT NULL REFERENCES public.countries(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- States
CREATE TABLE public.states (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    country_id  INTEGER NOT NULL REFERENCES public.countries(id) ON DELETE CASCADE,
    region_id   INTEGER REFERENCES public.regions(id) ON DELETE SET NULL,
    state_code  VARCHAR(10),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Subregions (districts / zones within a state)
CREATE TABLE public.subregions (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    state_id    INTEGER NOT NULL REFERENCES public.states(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Cities
CREATE TABLE public.cities (
    id            BIGINT NOT NULL PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    state_id      BIGINT NOT NULL,
    state_code    VARCHAR(255) NOT NULL,
    country_id    BIGINT NOT NULL,
    country_code  CHAR(2) NOT NULL,
    type          VARCHAR(191),
    level         INTEGER,
    parent_id     BIGINT,
    latitude      NUMERIC(10,8) NOT NULL,
    longitude     NUMERIC(11,8) NOT NULL,
    native        VARCHAR(255),
    population    BIGINT,
    timezone      VARCHAR(255),
    translations  TEXT,
    created_at    TIMESTAMP WITHOUT TIME ZONE DEFAULT '2014-01-01 12:01:01' NOT NULL,
    updated_at    TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    flag          SMALLINT DEFAULT 1 NOT NULL,
    "wikiDataId"  VARCHAR(255)
);
