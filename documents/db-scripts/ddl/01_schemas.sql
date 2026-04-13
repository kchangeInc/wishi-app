-- ============================================================
-- WISHI Database DDL - 01: Schema Creation
-- ============================================================
-- Run this first to create all application schemas.
-- PostgreSQL 14+
-- Note: public schema exists by default in PostgreSQL.

CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS ai;
CREATE SCHEMA IF NOT EXISTS company;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS automation;
CREATE SCHEMA IF NOT EXISTS seo;

-- Set default search path for convenience
ALTER DATABASE wishi SET search_path TO public, core, ai, company, analytics, automation, seo;

COMMENT ON SCHEMA core       IS 'Core entities: users, wishlists, marketplace sources, favourites';
COMMENT ON SCHEMA ai         IS 'AI matching engine: clusters, matches, scoring';
COMMENT ON SCHEMA company    IS 'Company admin: users, audit logs';
COMMENT ON SCHEMA analytics  IS 'Tracking: clicks, events, match history, demand, SEO performance';
COMMENT ON SCHEMA automation IS 'Schedulers, notifications, expiry';
COMMENT ON SCHEMA seo        IS 'SEO pages and tracking';
