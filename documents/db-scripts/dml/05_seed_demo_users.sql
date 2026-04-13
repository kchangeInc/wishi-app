-- ============================================================
-- WISHI Database DML - 05: Seed Demo Users
-- ============================================================
-- Pre-seeded users for company/demo login (email + password).
-- Passwords hashed with bcrypt (passlib).
-- DO NOT use these credentials in production.

INSERT INTO core.users (email, name, display_name, password_hash, role, is_active)
VALUES
  ('demo@wishi.in',   'Demo Buyer',  'Demo Buyer',  '$2b$12$CyDiocGxgb63rL7uSwromu0cZi70XiJlHdqQEky4ZZFfafpGEJFoC',   'buyer',  TRUE),
  ('seller@wishi.in', 'Demo Seller', 'Demo Seller', '$2b$12$svhjvuLi/lY3ivK2TKv68u4cR6lHVg43OlEuqMStUTV3Q3qlIK3iG', 'seller', TRUE),
  ('admin@wishi.in',  'Demo Admin',  'Demo Admin',  '$2b$12$kEPcxtWTH4WfmWIg2qyRS.oZsB2LIo3Dg2gNaHXl6B7jQnuOwSY9C',  'admin',  TRUE)
ON CONFLICT (email) DO UPDATE SET
  password_hash = EXCLUDED.password_hash,
  role          = EXCLUDED.role;
