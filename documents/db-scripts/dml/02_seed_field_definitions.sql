-- ============================================================
-- WISHI Database DML - 02: Field Definitions
-- ============================================================
-- Source: frontend-nextjs/features/wishlist/wishlistFieldConfig.js
-- subcategory_id references match the order seeded in 01_seed_roles_categories.sql:
--   1=Car, 2=Bike, 3=Scooter, 4=Truck, 5=Bus,
--   6=Mobile, 7=Laptop, 8=TV, 9=Camera,
--   10=Rent, 11=Buy, 12=PG/Hostel, 13=Plot,
--   14=Men, 15=Women, 16=Kids,
--   17=Furniture, 18=Appliances, 19=Decor

-- ======================== Automobile > Car (subcat 1) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(1, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Maruti Suzuki","Hyundai","Tata","Honda","Toyota","Mahindra","Kia","MG","Skoda","Volkswagen","BMW","Mercedes-Benz","Audi","Ford","Renault","Nissan","Jeep"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(1, 'model', 'Model', 'select', 2, FALSE, NULL, NULL, 'brand',
 '{
   "Maruti Suzuki":["Swift","Baleno","Dzire","Brezza","Ertiga","Alto","WagonR","Celerio","Ignis","Ciaz","XL6","Grand Vitara","Jimny","Fronx","Invicto"],
   "Hyundai":["i20","Creta","Venue","Verna","i10 Nios","Tucson","Alcazar","Aura","Exter","Ioniq 5"],
   "Tata":["Nexon","Punch","Harrier","Safari","Altroz","Tiago","Tigor","Nexon EV","Tiago EV","Curvv"],
   "Honda":["City","Amaze","Elevate","WR-V"],
   "Toyota":["Innova Crysta","Innova Hycross","Fortuner","Glanza","Urban Cruiser Hyryder","Camry","Hilux","Vellfire"],
   "Mahindra":["XUV700","Thar","Scorpio N","XUV400","XUV300","Bolero","Bolero Neo","Marazzo","XUV 3XO"],
   "Kia":["Seltos","Sonet","Carens","EV6","Carnival"],
   "MG":["Hector","Hector Plus","Astor","Gloster","ZS EV","Comet EV"],
   "Skoda":["Kushaq","Slavia","Kodiaq","Superb","Octavia"],
   "Volkswagen":["Virtus","Taigun","Tiguan"],
   "BMW":["3 Series","5 Series","X1","X3","X5","X7","2 Series Gran Coupe","iX1"],
   "Mercedes-Benz":["C-Class","E-Class","S-Class","GLA","GLC","GLE","A-Class Limousine","EQS"],
   "Audi":["A4","A6","Q3","Q5","Q7","Q8","e-tron"],
   "Ford":["Endeavour","EcoSport","Figo"],
   "Renault":["Kwid","Triber","Kiger"],
   "Nissan":["Magnite","X-Trail","Kicks"],
   "Jeep":["Compass","Meridian","Wrangler","Grand Cherokee"]
 }', NULL, NULL, NULL, NULL),

(1, 'year', 'Year', 'select', 3, FALSE, NULL,
 '["2026","2025","2024","2023","2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(1, 'fuelType', 'Fuel Type', 'select', 4, FALSE, NULL,
 '["Petrol","Diesel","Electric","CNG","Hybrid"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(1, 'owners', 'Owners', 'select', 5, FALSE, NULL,
 '["1st Owner","2nd Owner","3rd Owner","4th+"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(1, 'price', 'Price (up to)', 'slider', 6, FALSE, NULL, NULL, NULL, NULL, 50000, 5000000, 50000, '₹'),

(1, 'location', 'Location', 'autocomplete', 7, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Automobile > Bike (subcat 2) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(2, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Royal Enfield","Honda","Hero","Bajaj","TVS","Yamaha","KTM","Suzuki","Kawasaki","BMW","Ducati","Harley-Davidson","Jawa"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(2, 'model', 'Model', 'select', 2, FALSE, NULL, NULL, 'brand',
 '{
   "Royal Enfield":["Classic 350","Bullet 350","Hunter 350","Meteor 350","Himalayan","Continental GT 650","Interceptor 650","Super Meteor 650","Shotgun 650"],
   "Honda":["CB Hornet 160R","Unicorn","Shine","SP 125","CB200X","CB300R","H''ness CB350","CB350RS"],
   "Hero":["Splendor Plus","HF Deluxe","Glamour","Xtreme 160R","Xpulse 200","Passion Pro","Super Splendor","Karizma XMR"],
   "Bajaj":["Pulsar 150","Pulsar NS200","Pulsar RS200","Dominar 400","Avenger","Platina","CT110","Pulsar N250","Pulsar F250"],
   "TVS":["Apache RTR 160","Apache RTR 200","Apache RR 310","Raider","Star City Plus","Sport","Ronin"],
   "Yamaha":["FZ-S","FZ-X","R15 V4","R15M","MT-15 V2","FZ 25","Aerox 155"],
   "KTM":["Duke 125","Duke 200","Duke 250","Duke 390","RC 200","RC 390","Adventure 250","Adventure 390"],
   "Suzuki":["Gixxer SF","Gixxer 250","V-Strom SX","Hayabusa","Intruder"],
   "Kawasaki":["Ninja 300","Ninja 400","Ninja 650","Z650","Z900","Versys 650","W800"],
   "BMW":["G 310 R","G 310 GS","F 850 GS","R 1250 GS","S 1000 RR"],
   "Ducati":["Scrambler","Monster","Panigale V2","Panigale V4","Multistrada V4"],
   "Harley-Davidson":["X440","Nightster","Fat Boy","Road King","Street Glide","Pan America"],
   "Jawa":["Jawa 350","Jawa 42","Perak","Yezdi Roadster","Yezdi Adventure"]
 }', NULL, NULL, NULL, NULL),

(2, 'year', 'Year', 'select', 3, FALSE, NULL,
 '["2026","2025","2024","2023","2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(2, 'engineCC', 'Engine (CC)', 'select', 4, FALSE, NULL,
 '["100-150","150-250","250-500","500+"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(2, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 20000, 1000000, 10000, '₹'),

(2, 'location', 'Location', 'autocomplete', 6, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Automobile > Scooter (subcat 3) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(3, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Honda","TVS","Suzuki","Hero","Bajaj","Ola","Ather","Vespa","Aprilia","Yamaha"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(3, 'model', 'Model', 'select', 2, FALSE, NULL, NULL, 'brand',
 '{
   "Honda":["Activa 6G","Dio","Grazia","Activa 125"],
   "TVS":["Jupiter","Ntorq 125","iQube","Scooty Pep Plus","Scooty Zest"],
   "Suzuki":["Access 125","Burgman Street","Avenis"],
   "Hero":["Pleasure Plus","Destini 125","Maestro Edge"],
   "Bajaj":["Chetak"],
   "Ola":["S1 Pro","S1 Air","S1 X+"],
   "Ather":["450X","450S","450 Apex"],
   "Vespa":["VXL 125","VXL 150","SXL 150","Elegante 150"],
   "Aprilia":["SR 125","SR 160","SXR 160","Storm 125"],
   "Yamaha":["Fascino 125","Ray ZR 125","Aerox 155"]
 }', NULL, NULL, NULL, NULL),

(3, 'year', 'Year', 'select', 3, FALSE, NULL,
 '["2026","2025","2024","2023","2022","2021","2020","2019","2018","2017","2016","2015"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(3, 'price', 'Price (up to)', 'slider', 4, FALSE, NULL, NULL, NULL, NULL, 20000, 300000, 5000, '₹'),

(3, 'location', 'Location', 'autocomplete', 5, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Automobile > Truck (subcat 4) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(4, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Tata","Ashok Leyland","Mahindra","Eicher","BharatBenz","Volvo","Scania","Isuzu","Force"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(4, 'tonnage', 'Tonnage', 'select', 2, FALSE, NULL,
 '["Mini (<3.5T)","Light (3.5-7.5T)","Medium (7.5-16T)","Heavy (16T+)"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(4, 'fuelType', 'Fuel Type', 'select', 3, FALSE, NULL,
 '["Diesel","CNG","Electric"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(4, 'year', 'Year', 'select', 4, FALSE, NULL,
 '["2026","2025","2024","2023","2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(4, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 200000, 5000000, 100000, '₹'),

(4, 'location', 'Location', 'autocomplete', 6, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Automobile > Bus (subcat 5) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(5, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Tata","Ashok Leyland","Eicher","BharatBenz","Volvo","Scania","Force","SML Isuzu"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(5, 'seating', 'Seating Capacity', 'select', 2, FALSE, NULL,
 '["12-20","20-35","35-50","50+"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(5, 'fuelType', 'Fuel Type', 'select', 3, FALSE, NULL,
 '["Diesel","CNG","Electric"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(5, 'price', 'Price (up to)', 'slider', 4, FALSE, NULL, NULL, NULL, NULL, 500000, 10000000, 500000, '₹'),

(5, 'location', 'Location', 'autocomplete', 5, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Electronics > Mobile (subcat 6) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(6, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Apple","Samsung","OnePlus","Xiaomi","Realme","Vivo","Oppo","Google","Nothing","Motorola","iQOO","Poco"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(6, 'storage', 'Storage', 'select', 2, FALSE, NULL,
 '["64GB","128GB","256GB","512GB","1TB"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(6, 'ram', 'RAM', 'select', 3, FALSE, NULL,
 '["4GB","6GB","8GB","12GB","16GB"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(6, 'condition', 'Condition', 'select', 4, FALSE, NULL,
 '["New","Like New","Good","Fair"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(6, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 5000, 200000, 1000, '₹');

-- ======================== Electronics > Laptop (subcat 7) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(7, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Apple","Dell","HP","Lenovo","Asus","Acer","MSI","Samsung","Microsoft","LG","Razer"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(7, 'processor', 'Processor', 'select', 2, FALSE, NULL,
 '["Intel i3","Intel i5","Intel i7","Intel i9","Apple M1","Apple M2","Apple M3","AMD Ryzen 5","AMD Ryzen 7"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(7, 'ram', 'RAM', 'select', 3, FALSE, NULL,
 '["4GB","8GB","16GB","32GB","64GB"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(7, 'storage', 'Storage', 'select', 4, FALSE, NULL,
 '["256GB SSD","512GB SSD","1TB SSD","2TB SSD"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(7, 'screenSize', 'Screen Size', 'select', 5, FALSE, NULL,
 '["13\"","14\"","15.6\"","16\"","17\""]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(7, 'condition', 'Condition', 'select', 6, FALSE, NULL,
 '["New","Like New","Good","Fair"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(7, 'price', 'Price (up to)', 'slider', 7, FALSE, NULL, NULL, NULL, NULL, 15000, 500000, 5000, '₹');

-- ======================== Electronics > TV (subcat 8) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(8, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Samsung","LG","Sony","TCL","Mi","OnePlus","Vu","Hisense","Panasonic","Toshiba"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(8, 'screenSize', 'Screen Size', 'select', 2, FALSE, NULL,
 '["32\"","43\"","50\"","55\"","65\"","75\"","85\""]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(8, 'displayType', 'Type', 'select', 3, FALSE, NULL,
 '["LED","OLED","QLED","Neo QLED"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(8, 'smartTV', 'Smart TV', 'toggle', 4, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(8, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 10000, 500000, 5000, '₹');

-- ======================== Electronics > Camera (subcat 9) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(9, 'brand', 'Brand', 'select', 1, TRUE, NULL,
 '["Canon","Sony","Nikon","Fujifilm","Panasonic","GoPro","DJI","Olympus","Leica"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(9, 'cameraType', 'Type', 'select', 2, FALSE, NULL,
 '["DSLR","Mirrorless","Point & Shoot","Action Camera"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(9, 'megapixels', 'Megapixels', 'select', 3, FALSE, NULL,
 '["12-20MP","20-30MP","30-50MP","50MP+"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(9, 'condition', 'Condition', 'select', 4, FALSE, NULL,
 '["New","Like New","Good"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(9, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 10000, 500000, 5000, '₹');

-- ======================== Real Estate > Rent (subcat 10) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(10, 'city', 'City', 'autocomplete', 1, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(10, 'pincode', 'Pincode', 'text', 2, FALSE, '400001', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(10, 'bhk', 'BHK', 'select', 3, FALSE, NULL,
 '["1 BHK","2 BHK","3 BHK","4 BHK","4+ BHK"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(10, 'furnished', 'Furnished', 'select', 4, FALSE, NULL,
 '["Unfurnished","Semi-furnished","Fully Furnished"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(10, 'price', 'Rent (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 5000, 200000, 1000, '₹/mo'),

(10, 'parking', 'Parking', 'toggle', 6, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(10, 'lift', 'Lift', 'toggle', 7, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Real Estate > Buy (subcat 11) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(11, 'city', 'City', 'autocomplete', 1, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(11, 'pincode', 'Pincode', 'text', 2, FALSE, '400001', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(11, 'bhk', 'BHK', 'select', 3, FALSE, NULL,
 '["1 BHK","2 BHK","3 BHK","4 BHK","4+ BHK"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(11, 'propertyType', 'Property Type', 'select', 4, FALSE, NULL,
 '["Apartment","Villa","Independent House","Penthouse"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(11, 'price', 'Budget (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 1000000, 100000000, 500000, '₹'),

(11, 'parking', 'Parking', 'toggle', 6, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(11, 'lift', 'Lift', 'toggle', 7, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ======================== Real Estate > PG/Hostel (subcat 12) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(12, 'city', 'City', 'autocomplete', 1, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(12, 'locality', 'Locality', 'text', 2, FALSE, 'Area / Locality', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(12, 'roomType', 'Room Type', 'select', 3, FALSE, NULL,
 '["Single","Double","Triple","Dormitory"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(12, 'gender', 'Gender', 'select', 4, FALSE, NULL,
 '["Male","Female","Unisex"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(12, 'food', 'Food Included', 'toggle', 5, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(12, 'ac', 'AC', 'toggle', 6, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(12, 'price', 'Rent (up to)', 'slider', 7, FALSE, NULL, NULL, NULL, NULL, 3000, 50000, 500, '₹/mo');

-- ======================== Real Estate > Plot (subcat 13) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(13, 'city', 'City', 'autocomplete', 1, TRUE, 'Search city...', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(13, 'plotSize', 'Plot Size (sq ft)', 'number', 2, FALSE, '1000', NULL, NULL, NULL, NULL, NULL, NULL, NULL),

(13, 'plotType', 'Type', 'select', 3, FALSE, NULL,
 '["Residential","Commercial","Agricultural","Industrial"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(13, 'price', 'Budget (up to)', 'slider', 4, FALSE, NULL, NULL, NULL, NULL, 500000, 50000000, 500000, '₹');

-- ======================== Fashion > Men (subcat 14) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(14, 'itemType', 'Item Type', 'select', 1, TRUE, NULL,
 '["Shirts","T-Shirts","Jeans","Trousers","Jackets","Shoes","Watches","Accessories"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(14, 'brand', 'Brand', 'select', 2, FALSE, NULL,
 '["Nike","Adidas","Puma","Zara","H&M","Levi''s","Allen Solly","Peter England","Van Heusen","US Polo","Tommy Hilfiger","Calvin Klein","Woodland","Red Tape"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(14, 'size', 'Size', 'select', 3, FALSE, NULL,
 '["XS","S","M","L","XL","XXL","Free Size"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(14, 'condition', 'Condition', 'select', 4, FALSE, NULL,
 '["New","Like New","Good"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(14, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 200, 50000, 200, '₹');

-- ======================== Fashion > Women (subcat 15) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(15, 'itemType', 'Item Type', 'select', 1, TRUE, NULL,
 '["Dresses","Tops","Jeans","Sarees","Kurtis","Shoes","Bags","Jewelry"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(15, 'brand', 'Brand', 'select', 2, FALSE, NULL,
 '["Zara","H&M","FabIndia","W","Biba","Global Desi","Mango","Forever 21","AND","Vero Moda","Nike","Adidas","Puma"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(15, 'size', 'Size', 'select', 3, FALSE, NULL,
 '["XS","S","M","L","XL","XXL","Free Size"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(15, 'condition', 'Condition', 'select', 4, FALSE, NULL,
 '["New","Like New","Good"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(15, 'price', 'Price (up to)', 'slider', 5, FALSE, NULL, NULL, NULL, NULL, 200, 50000, 200, '₹');

-- ======================== Fashion > Kids (subcat 16) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(16, 'itemType', 'Item Type', 'select', 1, TRUE, NULL,
 '["Clothing","Shoes","Accessories","School Bags"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(16, 'ageGroup', 'Age Group', 'select', 2, FALSE, NULL,
 '["0-2 years","2-5 years","5-10 years","10-15 years"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(16, 'gender', 'Gender', 'select', 3, FALSE, NULL,
 '["Boy","Girl","Unisex"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(16, 'price', 'Price (up to)', 'slider', 4, FALSE, NULL, NULL, NULL, NULL, 100, 10000, 100, '₹');

-- ======================== Home & Living > Furniture (subcat 17) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(17, 'itemType', 'Item', 'select', 1, TRUE, NULL,
 '["Sofa","Bed","Dining Table","Wardrobe","Desk","Bookshelf","Chair"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(17, 'material', 'Material', 'select', 2, FALSE, NULL,
 '["Wood","Metal","Fabric","Leather","Engineered Wood"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(17, 'condition', 'Condition', 'select', 3, FALSE, NULL,
 '["New","Like New","Good","Fair"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(17, 'price', 'Price (up to)', 'slider', 4, FALSE, NULL, NULL, NULL, NULL, 1000, 200000, 1000, '₹');

-- ======================== Home & Living > Appliances (subcat 18) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(18, 'itemType', 'Appliance', 'select', 1, TRUE, NULL,
 '["Refrigerator","Washing Machine","AC","Microwave","Water Purifier","Dishwasher","Geyser"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(18, 'brand', 'Brand', 'select', 2, FALSE, NULL,
 '["LG","Samsung","Whirlpool","Bosch","IFB","Voltas","Daikin","Blue Star","Haier","Godrej","Kent","Aquaguard"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(18, 'condition', 'Condition', 'select', 3, FALSE, NULL,
 '["New","Like New","Good"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(18, 'price', 'Price (up to)', 'slider', 4, FALSE, NULL, NULL, NULL, NULL, 2000, 200000, 1000, '₹');

-- ======================== Home & Living > Decor (subcat 19) ========================

INSERT INTO public.field_definitions (subcategory_id, name, label, field_type, display_order, is_required, placeholder, options, depends_on, options_by_parent, min_value, max_value, step, unit) VALUES
(19, 'itemType', 'Item', 'select', 1, TRUE, NULL,
 '["Wall Art","Rugs","Curtains","Lamps","Vases","Mirrors","Cushions"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(19, 'style', 'Style', 'select', 2, FALSE, NULL,
 '["Modern","Traditional","Minimalist","Bohemian","Industrial"]',
 NULL, NULL, NULL, NULL, NULL, NULL),

(19, 'price', 'Price (up to)', 'slider', 3, FALSE, NULL, NULL, NULL, NULL, 200, 50000, 200, '₹');
