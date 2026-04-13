-- ============================================================
-- WISHI Database DDL - 08: Automation Schema Tables
-- ============================================================

-- Notifications (actual notification records sent to users)
CREATE TABLE automation.notifications (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    type        VARCHAR(50) NOT NULL,                -- match, price_drop, expiry, favourite, promo
    title       VARCHAR(500) NOT NULL,
    description TEXT,
    wishlist_id INTEGER REFERENCES core.wishlists(id) ON DELETE SET NULL,
    match_id    INTEGER REFERENCES ai.matches(id) ON DELETE SET NULL,
    action_url  TEXT,                                -- deep link for notification click
    is_read     BOOLEAN DEFAULT FALSE,
    read_at     TIMESTAMPTZ,
    is_deleted  BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Schedulers (tracks background jobs)
CREATE TABLE automation.schedulers (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    task_type     VARCHAR(100) NOT NULL,             -- wishlist_expiry_check, match_refresh, notification_digest
    schedule_cron VARCHAR(100),                      -- cron expression
    last_run_at   TIMESTAMPTZ,
    next_run_at   TIMESTAMPTZ,
    status        VARCHAR(50) DEFAULT 'active',      -- active, paused, disabled
    config        JSONB,                             -- task-specific configuration
    error_count   INTEGER DEFAULT 0,
    last_error    TEXT,
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);
