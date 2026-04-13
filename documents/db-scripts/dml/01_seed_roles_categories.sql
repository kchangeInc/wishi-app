-- ============================================================
-- WISHI Database DML - 01: Roles, Categories & Subcategories
-- ============================================================

-- ======================== Roles ========================

INSERT INTO public.roles (name, description) VALUES
  ('buyer',  'End-user who creates wishlists and receives matches'),
  ('seller', 'Marketplace seller or business user'),
  ('admin',  'Internal company admin with full access');

-- ======================== Categories ========================

INSERT INTO public.categories (name, slug, icon, display_order) VALUES
  ('Automobile',    'automobile',    'Car',        1),
  ('Electronics',   'electronics',   'Smartphone', 2),
  ('Real Estate',   'real-estate',   'Home',       3),
  ('Fashion',       'fashion',       'Shirt',      4),
  ('Home & Living', 'home-living',   'Sofa',       5);

-- ======================== Subcategories ========================

-- Automobile (category_id = 1)
INSERT INTO public.subcategories (category_id, name, slug, display_order) VALUES
  (1, 'Car',     'car',     1),
  (1, 'Bike',    'bike',    2),
  (1, 'Scooter', 'scooter', 3),
  (1, 'Truck',   'truck',   4),
  (1, 'Bus',     'bus',     5);

-- Electronics (category_id = 2)
INSERT INTO public.subcategories (category_id, name, slug, display_order) VALUES
  (2, 'Mobile', 'mobile', 1),
  (2, 'Laptop', 'laptop', 2),
  (2, 'TV',     'tv',     3),
  (2, 'Camera', 'camera', 4);

-- Real Estate (category_id = 3)
INSERT INTO public.subcategories (category_id, name, slug, display_order) VALUES
  (3, 'Rent',      'rent',      1),
  (3, 'Buy',       'buy',       2),
  (3, 'PG/Hostel', 'pg-hostel', 3),
  (3, 'Plot',      'plot',      4);

-- Fashion (category_id = 4)
INSERT INTO public.subcategories (category_id, name, slug, display_order) VALUES
  (4, 'Men',   'men',   1),
  (4, 'Women', 'women', 2),
  (4, 'Kids',  'kids',  3);

-- Home & Living (category_id = 5)
INSERT INTO public.subcategories (category_id, name, slug, display_order) VALUES
  (5, 'Furniture',  'furniture',  1),
  (5, 'Appliances', 'appliances', 2),
  (5, 'Decor',      'decor',      3);
