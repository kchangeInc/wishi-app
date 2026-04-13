-- ============================================================
-- WISHI Database DML - 04: Marketplace Sources
-- ============================================================
-- Source: frontend-nextjs/features/wishlist/mockMatches.js → MARKETPLACE_SOURCES
-- 19 unique sources across 5 categories (some shared: OLX, Amazon, Flipkart)

-- ======================== Marketplace Sources ========================

INSERT INTO core.marketplace_sources (name, slug, url_template, color) VALUES
  ('OLX',              'olx',              'https://www.olx.in/items/q-{q}',                                 '#002f34'),
  ('CarDekho',         'cardekho',         'https://www.cardekho.com/used-cars+{q}',                         '#e23744'),
  ('Cars24',           'cars24',           'https://www.cars24.com/buy-used-cars-{q}',                       '#f5a623'),
  ('CarWale',          'carwale',          'https://www.carwale.com/used/cars-in-{q}',                       '#00b0ff'),
  ('Droom',            'droom',            'https://droom.in/used-{q}',                                      '#43a047'),
  ('Amazon',           'amazon',           'https://www.amazon.in/s?k={q}',                                  '#ff9900'),
  ('Flipkart',         'flipkart',         'https://www.flipkart.com/search?q={q}',                         '#2874f0'),
  ('Croma',            'croma',            'https://www.croma.com/searchB?q={q}',                            '#00b050'),
  ('Reliance Digital', 'reliance-digital', 'https://www.reliancedigital.in/search?q={q}',                   '#003399'),
  ('99acres',          '99acres',          'https://www.99acres.com/search/property/buy/{q}',                '#d92228'),
  ('MagicBricks',      'magicbricks',      'https://www.magicbricks.com/property-for-sale-in-{q}',          '#e44d26'),
  ('Housing.com',      'housing-com',      'https://housing.com/in/buy/{q}',                                 '#00c1a2'),
  ('NoBroker',         'nobroker',         'https://www.nobroker.in/property/sale/{q}',                      '#e53935'),
  ('Myntra',           'myntra',           'https://www.myntra.com/{q}',                                     '#ff3e6c'),
  ('Ajio',             'ajio',             'https://www.ajio.com/search/?text={q}',                          '#3b3b3b'),
  ('Tata CLiQ',        'tata-cliq',        'https://www.tatacliq.com/search/?searchCategory=all&text={q}',  '#434ba1'),
  ('Pepperfry',        'pepperfry',        'https://www.pepperfry.com/search?q={q}',                        '#f16522'),
  ('Urban Ladder',     'urban-ladder',     'https://www.urbanladder.com/search?q={q}',                      '#ff7043'),
  ('HomeTown',         'hometown',         'https://www.hometown.in/search?q={q}',                           '#c62828');

-- ======================== Marketplace ↔ Category mapping ========================
-- Maps which marketplaces serve which categories
-- category_id: 1=Automobile, 2=Electronics, 3=Real Estate, 4=Fashion, 5=Home & Living

-- Automobile sources
INSERT INTO core.marketplace_source_categories (marketplace_source_id, category_id)
SELECT ms.id, 1 FROM core.marketplace_sources ms
WHERE ms.slug IN ('olx', 'cardekho', 'cars24', 'carwale', 'droom');

-- Electronics sources
INSERT INTO core.marketplace_source_categories (marketplace_source_id, category_id)
SELECT ms.id, 2 FROM core.marketplace_sources ms
WHERE ms.slug IN ('amazon', 'flipkart', 'olx', 'croma', 'reliance-digital');

-- Real Estate sources
INSERT INTO core.marketplace_source_categories (marketplace_source_id, category_id)
SELECT ms.id, 3 FROM core.marketplace_sources ms
WHERE ms.slug IN ('99acres', 'magicbricks', 'housing-com', 'nobroker', 'olx');

-- Fashion sources
INSERT INTO core.marketplace_source_categories (marketplace_source_id, category_id)
SELECT ms.id, 4 FROM core.marketplace_sources ms
WHERE ms.slug IN ('myntra', 'ajio', 'amazon', 'flipkart', 'tata-cliq');

-- Home & Living sources
INSERT INTO core.marketplace_source_categories (marketplace_source_id, category_id)
SELECT ms.id, 5 FROM core.marketplace_sources ms
WHERE ms.slug IN ('pepperfry', 'urban-ladder', 'amazon', 'flipkart', 'hometown');
