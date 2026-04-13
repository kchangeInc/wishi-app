-- ============================================================
-- WISHI Database DDL - 06: Company Schema Tables
-- ============================================================

-- Company / admin users (extended profile for internal users)
CREATE TABLE company.company_users (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    department    VARCHAR(100),
    designation   VARCHAR(100),
    permissions   JSONB,                             -- granular permission flags
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- Audit log (all schema changes across the system)
CREATE TABLE company.audit_log (
    id            SERIAL PRIMARY KEY,
    schema_name   VARCHAR(100),
    table_name    VARCHAR(100) NOT NULL,
    record_id     INTEGER NOT NULL,
    action        VARCHAR(50) NOT NULL,              -- INSERT, UPDATE, DELETE
    old_values    JSONB,
    new_values    JSONB,
    user_id       INTEGER REFERENCES core.users(id),
    ip_address    VARCHAR(45),
    user_agent    TEXT,
    timestamp     TIMESTAMPTZ DEFAULT NOW()
);
