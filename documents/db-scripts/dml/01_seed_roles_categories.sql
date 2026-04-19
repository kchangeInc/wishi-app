-- ============================================================
-- WISHI Database DML - 01: Roles, Categories & Subcategories
-- ============================================================

-- ======================== Roles ========================

INSERT INTO public.roles (name, description) VALUES
  ('buyer',  'End-user who creates wishlists and receives matches'),
  ('seller', 'Marketplace seller or business user'),
  ('admin',  'Internal company admin with full access');

-- ======================== Categories ========================

INSERT INTO public.categories (name, slug, icon, emoji, color_bg, color_border, color_text, display_order) VALUES
  ('Automobile',    'automobile',    'Car',        '🚗', 'bg-blue-50',    'border-blue-100',    'text-blue-600',    1),
  ('Electronics',   'electronics',   'Smartphone', '📱', 'bg-violet-50',  'border-violet-100',  'text-violet-600',  2),
  ('Real Estate',   'real-estate',   'Home',       '🏠', 'bg-emerald-50', 'border-emerald-100', 'text-emerald-600', 3),
  ('Fashion',       'fashion',       'Shirt',      '👗', 'bg-pink-50',    'border-pink-100',    'text-pink-600',    4),
  ('Home & Living', 'home-living',   'Sofa',       '🛋️', 'bg-amber-50',   'border-amber-100',   'text-amber-600',   5);

-- ======================== Banner Ideas ========================

INSERT INTO public.banner_ideas (category_id, emoji, text, color_bg, color_border, color_text, display_order) VALUES
  (1, '🚗', 'Honda City under ₹8L',        'bg-blue-50',    'border-blue-100',    'text-blue-600',    1),
  (1, '🏍️', 'Royal Enfield Classic 350',    'bg-blue-50',    'border-blue-100',    'text-blue-600',    2),
  (1, '🛵', 'Scooter under ₹70K',          'bg-blue-50',    'border-blue-100',    'text-blue-600',    3),
  (2, '📱', 'iPhone 15 Pro in Budget',      'bg-violet-50',  'border-violet-100',  'text-violet-600',  4),
  (2, '💻', 'MacBook Pro M3 under ₹2L',    'bg-violet-50',  'border-violet-100',  'text-violet-600',  5),
  (2, '📺', 'Samsung 65" QLED TV',          'bg-violet-50',  'border-violet-100',  'text-violet-600',  6),
  (3, '🏠', '2BHK for Rent in Mumbai',      'bg-emerald-50', 'border-emerald-100', 'text-emerald-600', 7),
  (3, '🏡', '3BHK in Pune under ₹90L',     'bg-emerald-50', 'border-emerald-100', 'text-emerald-600', 8),
  (4, '👗', 'Designer Saree under ₹5K',     'bg-pink-50',    'border-pink-100',    'text-pink-600',    9),
  (5, '🛋️', 'L-shape Sofa under ₹40K',     'bg-amber-50',   'border-amber-100',   'text-amber-600',   10);

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
