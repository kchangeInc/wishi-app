function yearOptions(start, end) {
  const years = []
  for (let y = end; y >= start; y--) years.push(String(y))
  return years
}

export const INDIAN_CITIES = [
  'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Pune',
  'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam',
  'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut',
  'Rajkot', 'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Navi Mumbai',
  'Allahabad', 'Ranchi', 'Howrah', 'Coimbatore', 'Jabalpur', 'Gwalior', 'Vijayawada',
  'Jodhpur', 'Madurai', 'Raipur', 'Kota', 'Chandigarh', 'Guwahati', 'Solapur', 'Hubli',
  'Mysore', 'Tiruchirappalli', 'Bareilly', 'Aligarh', 'Tiruppur', 'Moradabad', 'Jalandhar',
  'Bhubaneswar', 'Salem', 'Warangal', 'Guntur', 'Bhiwandi', 'Saharanpur', 'Gorakhpur',
  'Bikaner', 'Amravati', 'Noida', 'Jamshedpur', 'Bhilai', 'Cuttack', 'Firozabad',
  'Kochi', 'Nellore', 'Bhavnagar', 'Dehradun', 'Durgapur', 'Asansol', 'Rourkela',
  'Nanded', 'Kolhapur', 'Ajmer', 'Akola', 'Gulbarga', 'Jamnagar', 'Ujjain', 'Loni',
  'Siliguri', 'Jhansi', 'Ulhasnagar', 'Jammu', 'Sangli', 'Mangalore', 'Erode',
  'Belgaum', 'Ambattur', 'Tirunelveli', 'Malegaon', 'Gaya', 'Udaipur', 'Kakinada',
  'Davanagere', 'Kozhikode', 'Maheshtala', 'Rajpur Sonarpur', 'Bokaro', 'South Dumdum',
  'Bellary', 'Patiala', 'Gopalpur', 'Agartala', 'Bhagalpur', 'Muzaffarnagar', 'Bhatpara',
  'Panihati', 'Latur', 'Dhule', 'Rohtak', 'Sagar', 'Korba', 'Bhilwara', 'Berhampur',
  'Muzaffarpur', 'Ahmednagar', 'Mathura', 'Kollam', 'Avadi', 'Kadapa', 'Kamarhati',
  'Sambalpur', 'Bilaspur', 'Shahjahanpur', 'Satara', 'Bijapur', 'Rampur', 'Shimoga',
  'Chandrapur', 'Junagadh', 'Thrissur', 'Alwar', 'Bardhaman', 'Kulti', 'Nizamabad',
  'Parbhani', 'Tumkur', 'Khammam', 'Ozhukarai', 'Bihar Sharif', 'Panipat', 'Darbhanga',
  'Bally', 'Aizawl', 'Dewas', 'Ichalkaranji', 'Karnal', 'Bathinda', 'Jalna',
  'Eluru', 'Kirari Suleman Nagar', 'Barasat', 'Purnia', 'Satna', 'Mau', 'Sonipat',
  'Farrukhabad', 'Durg', 'Imphal', 'Ratlam', 'Hapur', 'Arrah', 'Anantapur',
  'Karimnagar', 'Etawah', 'Ambarnath', 'Gandhinagar', 'Secunderabad', 'Greater Noida',
  'Gurgaon', 'Thiruvananthapuram', 'Pondicherry', 'Shimla', 'Gangtok', 'Shillong',
]

export const CATEGORIES = {
  Automobile: {
    icon: 'Car',
    subcategories: {
      Car: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Maruti Suzuki', 'Hyundai', 'Tata', 'Honda', 'Toyota', 'Mahindra', 'Kia', 'MG', 'Skoda', 'Volkswagen', 'BMW', 'Mercedes-Benz', 'Audi', 'Ford', 'Renault', 'Nissan', 'Jeep'], required: true },
        { name: 'model', label: 'Model', type: 'select', dependsOn: 'brand', optionsByParent: {
          'Maruti Suzuki': ['Swift', 'Baleno', 'Dzire', 'Brezza', 'Ertiga', 'Alto', 'WagonR', 'Celerio', 'Ignis', 'Ciaz', 'XL6', 'Grand Vitara', 'Jimny', 'Fronx', 'Invicto'],
          'Hyundai': ['i20', 'Creta', 'Venue', 'Verna', 'i10 Nios', 'Tucson', 'Alcazar', 'Aura', 'Exter', 'Ioniq 5'],
          'Tata': ['Nexon', 'Punch', 'Harrier', 'Safari', 'Altroz', 'Tiago', 'Tigor', 'Nexon EV', 'Tiago EV', 'Curvv'],
          'Honda': ['City', 'Amaze', 'Elevate', 'WR-V'],
          'Toyota': ['Innova Crysta', 'Innova Hycross', 'Fortuner', 'Glanza', 'Urban Cruiser Hyryder', 'Camry', 'Hilux', 'Vellfire'],
          'Mahindra': ['XUV700', 'Thar', 'Scorpio N', 'XUV400', 'XUV300', 'Bolero', 'Bolero Neo', 'Marazzo', 'XUV 3XO'],
          'Kia': ['Seltos', 'Sonet', 'Carens', 'EV6', 'Carnival'],
          'MG': ['Hector', 'Hector Plus', 'Astor', 'Gloster', 'ZS EV', 'Comet EV'],
          'Skoda': ['Kushaq', 'Slavia', 'Kodiaq', 'Superb', 'Octavia'],
          'Volkswagen': ['Virtus', 'Taigun', 'Tiguan'],
          'BMW': ['3 Series', '5 Series', 'X1', 'X3', 'X5', 'X7', '2 Series Gran Coupe', 'iX1'],
          'Mercedes-Benz': ['C-Class', 'E-Class', 'S-Class', 'GLA', 'GLC', 'GLE', 'A-Class Limousine', 'EQS'],
          'Audi': ['A4', 'A6', 'Q3', 'Q5', 'Q7', 'Q8', 'e-tron'],
          'Ford': ['Endeavour', 'EcoSport', 'Figo'],
          'Renault': ['Kwid', 'Triber', 'Kiger'],
          'Nissan': ['Magnite', 'X-Trail', 'Kicks'],
          'Jeep': ['Compass', 'Meridian', 'Wrangler', 'Grand Cherokee'],
        }},
        { name: 'year', label: 'Year', type: 'select', options: yearOptions(2010, 2026) },
        { name: 'fuelType', label: 'Fuel Type', type: 'select', options: ['Petrol', 'Diesel', 'Electric', 'CNG', 'Hybrid'] },
        { name: 'owners', label: 'Owners', type: 'select', options: ['1st Owner', '2nd Owner', '3rd Owner', '4th+'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 50000, max: 5000000, step: 50000, unit: '₹' },
        { name: 'location', label: 'Location', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
      ],
      Bike: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Royal Enfield', 'Honda', 'Hero', 'Bajaj', 'TVS', 'Yamaha', 'KTM', 'Suzuki', 'Kawasaki', 'BMW', 'Ducati', 'Harley-Davidson', 'Jawa'], required: true },
        { name: 'model', label: 'Model', type: 'select', dependsOn: 'brand', optionsByParent: {
          'Royal Enfield': ['Classic 350', 'Bullet 350', 'Hunter 350', 'Meteor 350', 'Himalayan', 'Continental GT 650', 'Interceptor 650', 'Super Meteor 650', 'Shotgun 650'],
          'Honda': ['CB Hornet 160R', 'Unicorn', 'Shine', 'SP 125', 'CB200X', 'CB300R', 'H\'ness CB350', 'CB350RS'],
          'Hero': ['Splendor Plus', 'HF Deluxe', 'Glamour', 'Xtreme 160R', 'Xpulse 200', 'Passion Pro', 'Super Splendor', 'Karizma XMR'],
          'Bajaj': ['Pulsar 150', 'Pulsar NS200', 'Pulsar RS200', 'Dominar 400', 'Avenger', 'Platina', 'CT110', 'Pulsar N250', 'Pulsar F250'],
          'TVS': ['Apache RTR 160', 'Apache RTR 200', 'Apache RR 310', 'Raider', 'Star City Plus', 'Sport', 'Ronin'],
          'Yamaha': ['FZ-S', 'FZ-X', 'R15 V4', 'R15M', 'MT-15 V2', 'FZ 25', 'Aerox 155'],
          'KTM': ['Duke 125', 'Duke 200', 'Duke 250', 'Duke 390', 'RC 200', 'RC 390', 'Adventure 250', 'Adventure 390'],
          'Suzuki': ['Gixxer SF', 'Gixxer 250', 'V-Strom SX', 'Hayabusa', 'Intruder'],
          'Kawasaki': ['Ninja 300', 'Ninja 400', 'Ninja 650', 'Z650', 'Z900', 'Versys 650', 'W800'],
          'BMW': ['G 310 R', 'G 310 GS', 'F 850 GS', 'R 1250 GS', 'S 1000 RR'],
          'Ducati': ['Scrambler', 'Monster', 'Panigale V2', 'Panigale V4', 'Multistrada V4'],
          'Harley-Davidson': ['X440', 'Nightster', 'Fat Boy', 'Road King', 'Street Glide', 'Pan America'],
          'Jawa': ['Jawa 350', 'Jawa 42', 'Perak', 'Yezdi Roadster', 'Yezdi Adventure'],
        }},
        { name: 'year', label: 'Year', type: 'select', options: yearOptions(2010, 2026) },
        { name: 'engineCC', label: 'Engine (CC)', type: 'select', options: ['100-150', '150-250', '250-500', '500+'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 20000, max: 1000000, step: 10000, unit: '₹' },
        { name: 'location', label: 'Location', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
      ],
      Scooter: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Honda', 'TVS', 'Suzuki', 'Hero', 'Bajaj', 'Ola', 'Ather', 'Vespa', 'Aprilia', 'Yamaha'], required: true },
        { name: 'model', label: 'Model', type: 'select', dependsOn: 'brand', optionsByParent: {
          'Honda': ['Activa 6G', 'Dio', 'Grazia', 'Activa 125'],
          'TVS': ['Jupiter', 'Ntorq 125', 'iQube', 'Scooty Pep Plus', 'Scooty Zest'],
          'Suzuki': ['Access 125', 'Burgman Street', 'Avenis'],
          'Hero': ['Pleasure Plus', 'Destini 125', 'Maestro Edge'],
          'Bajaj': ['Chetak'],
          'Ola': ['S1 Pro', 'S1 Air', 'S1 X+'],
          'Ather': ['450X', '450S', '450 Apex'],
          'Vespa': ['VXL 125', 'VXL 150', 'SXL 150', 'Elegante 150'],
          'Aprilia': ['SR 125', 'SR 160', 'SXR 160', 'Storm 125'],
          'Yamaha': ['Fascino 125', 'Ray ZR 125', 'Aerox 155'],
        }},
        { name: 'year', label: 'Year', type: 'select', options: yearOptions(2015, 2026) },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 20000, max: 300000, step: 5000, unit: '₹' },
        { name: 'location', label: 'Location', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
      ],
      Truck: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Tata', 'Ashok Leyland', 'Mahindra', 'Eicher', 'BharatBenz', 'Volvo', 'Scania', 'Isuzu', 'Force'], required: true },
        { name: 'tonnage', label: 'Tonnage', type: 'select', options: ['Mini (<3.5T)', 'Light (3.5-7.5T)', 'Medium (7.5-16T)', 'Heavy (16T+)'] },
        { name: 'fuelType', label: 'Fuel Type', type: 'select', options: ['Diesel', 'CNG', 'Electric'] },
        { name: 'year', label: 'Year', type: 'select', options: yearOptions(2010, 2026) },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 200000, max: 5000000, step: 100000, unit: '₹' },
        { name: 'location', label: 'Location', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
      ],
      Bus: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Tata', 'Ashok Leyland', 'Eicher', 'BharatBenz', 'Volvo', 'Scania', 'Force', 'SML Isuzu'], required: true },
        { name: 'seating', label: 'Seating Capacity', type: 'select', options: ['12-20', '20-35', '35-50', '50+'] },
        { name: 'fuelType', label: 'Fuel Type', type: 'select', options: ['Diesel', 'CNG', 'Electric'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 500000, max: 10000000, step: 500000, unit: '₹' },
        { name: 'location', label: 'Location', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
      ],
    },
  },

  Electronics: {
    icon: 'Smartphone',
    subcategories: {
      Mobile: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Apple', 'Samsung', 'OnePlus', 'Xiaomi', 'Realme', 'Vivo', 'Oppo', 'Google', 'Nothing', 'Motorola', 'iQOO', 'Poco'], required: true },
        { name: 'storage', label: 'Storage', type: 'select', options: ['64GB', '128GB', '256GB', '512GB', '1TB'] },
        { name: 'ram', label: 'RAM', type: 'select', options: ['4GB', '6GB', '8GB', '12GB', '16GB'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good', 'Fair'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 5000, max: 200000, step: 1000, unit: '₹' },
      ],
      Laptop: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'MSI', 'Samsung', 'Microsoft', 'LG', 'Razer'], required: true },
        { name: 'processor', label: 'Processor', type: 'select', options: ['Intel i3', 'Intel i5', 'Intel i7', 'Intel i9', 'Apple M1', 'Apple M2', 'Apple M3', 'AMD Ryzen 5', 'AMD Ryzen 7'] },
        { name: 'ram', label: 'RAM', type: 'select', options: ['4GB', '8GB', '16GB', '32GB', '64GB'] },
        { name: 'storage', label: 'Storage', type: 'select', options: ['256GB SSD', '512GB SSD', '1TB SSD', '2TB SSD'] },
        { name: 'screenSize', label: 'Screen Size', type: 'select', options: ['13"', '14"', '15.6"', '16"', '17"'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good', 'Fair'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 15000, max: 500000, step: 5000, unit: '₹' },
      ],
      TV: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Samsung', 'LG', 'Sony', 'TCL', 'Mi', 'OnePlus', 'Vu', 'Hisense', 'Panasonic', 'Toshiba'], required: true },
        { name: 'screenSize', label: 'Screen Size', type: 'select', options: ['32"', '43"', '50"', '55"', '65"', '75"', '85"'] },
        { name: 'displayType', label: 'Type', type: 'select', options: ['LED', 'OLED', 'QLED', 'Neo QLED'] },
        { name: 'smartTV', label: 'Smart TV', type: 'toggle' },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 10000, max: 500000, step: 5000, unit: '₹' },
      ],
      Camera: [
        { name: 'brand', label: 'Brand', type: 'select', options: ['Canon', 'Sony', 'Nikon', 'Fujifilm', 'Panasonic', 'GoPro', 'DJI', 'Olympus', 'Leica'], required: true },
        { name: 'cameraType', label: 'Type', type: 'select', options: ['DSLR', 'Mirrorless', 'Point & Shoot', 'Action Camera'] },
        { name: 'megapixels', label: 'Megapixels', type: 'select', options: ['12-20MP', '20-30MP', '30-50MP', '50MP+'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 10000, max: 500000, step: 5000, unit: '₹' },
      ],
    },
  },

  'Real Estate': {
    icon: 'Home',
    subcategories: {
      Rent: [
        { name: 'city', label: 'City', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
        { name: 'pincode', label: 'Pincode', type: 'text', placeholder: '400001' },
        { name: 'bhk', label: 'BHK', type: 'select', options: ['1 BHK', '2 BHK', '3 BHK', '4 BHK', '4+ BHK'] },
        { name: 'furnished', label: 'Furnished', type: 'select', options: ['Unfurnished', 'Semi-furnished', 'Fully Furnished'] },
        { name: 'price', label: 'Rent (up to)', type: 'slider', min: 5000, max: 200000, step: 1000, unit: '₹/mo' },
        { name: 'parking', label: 'Parking', type: 'toggle' },
        { name: 'lift', label: 'Lift', type: 'toggle' },
      ],
      Buy: [
        { name: 'city', label: 'City', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
        { name: 'pincode', label: 'Pincode', type: 'text', placeholder: '400001' },
        { name: 'bhk', label: 'BHK', type: 'select', options: ['1 BHK', '2 BHK', '3 BHK', '4 BHK', '4+ BHK'] },
        { name: 'propertyType', label: 'Property Type', type: 'select', options: ['Apartment', 'Villa', 'Independent House', 'Penthouse'] },
        { name: 'price', label: 'Budget (up to)', type: 'slider', min: 1000000, max: 100000000, step: 500000, unit: '₹' },
        { name: 'parking', label: 'Parking', type: 'toggle' },
        { name: 'lift', label: 'Lift', type: 'toggle' },
      ],
      'PG/Hostel': [
        { name: 'city', label: 'City', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
        { name: 'locality', label: 'Locality', type: 'text', placeholder: 'Area / Locality' },
        { name: 'roomType', label: 'Room Type', type: 'select', options: ['Single', 'Double', 'Triple', 'Dormitory'] },
        { name: 'gender', label: 'Gender', type: 'select', options: ['Male', 'Female', 'Unisex'] },
        { name: 'food', label: 'Food Included', type: 'toggle' },
        { name: 'ac', label: 'AC', type: 'toggle' },
        { name: 'price', label: 'Rent (up to)', type: 'slider', min: 3000, max: 50000, step: 500, unit: '₹/mo' },
      ],
      Plot: [
        { name: 'city', label: 'City', type: 'autocomplete', options: INDIAN_CITIES, placeholder: 'Search city...', required: true },
        { name: 'plotSize', label: 'Plot Size (sq ft)', type: 'number', placeholder: '1000' },
        { name: 'plotType', label: 'Type', type: 'select', options: ['Residential', 'Commercial', 'Agricultural', 'Industrial'] },
        { name: 'price', label: 'Budget (up to)', type: 'slider', min: 500000, max: 50000000, step: 500000, unit: '₹' },
      ],
    },
  },

  Fashion: {
    icon: 'Shirt',
    subcategories: {
      Men: [
        { name: 'itemType', label: 'Item Type', type: 'select', options: ['Shirts', 'T-Shirts', 'Jeans', 'Trousers', 'Jackets', 'Shoes', 'Watches', 'Accessories'], required: true },
        { name: 'brand', label: 'Brand', type: 'select', options: ['Nike', 'Adidas', 'Puma', 'Zara', 'H&M', 'Levi\'s', 'Allen Solly', 'Peter England', 'Van Heusen', 'US Polo', 'Tommy Hilfiger', 'Calvin Klein', 'Woodland', 'Red Tape'] },
        { name: 'size', label: 'Size', type: 'select', options: ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'Free Size'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 200, max: 50000, step: 200, unit: '₹' },
      ],
      Women: [
        { name: 'itemType', label: 'Item Type', type: 'select', options: ['Dresses', 'Tops', 'Jeans', 'Sarees', 'Kurtis', 'Shoes', 'Bags', 'Jewelry'], required: true },
        { name: 'brand', label: 'Brand', type: 'select', options: ['Zara', 'H&M', 'FabIndia', 'W', 'Biba', 'Global Desi', 'Mango', 'Forever 21', 'AND', 'Vero Moda', 'Nike', 'Adidas', 'Puma'] },
        { name: 'size', label: 'Size', type: 'select', options: ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'Free Size'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 200, max: 50000, step: 200, unit: '₹' },
      ],
      Kids: [
        { name: 'itemType', label: 'Item Type', type: 'select', options: ['Clothing', 'Shoes', 'Accessories', 'School Bags'], required: true },
        { name: 'ageGroup', label: 'Age Group', type: 'select', options: ['0-2 years', '2-5 years', '5-10 years', '10-15 years'] },
        { name: 'gender', label: 'Gender', type: 'select', options: ['Boy', 'Girl', 'Unisex'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 100, max: 10000, step: 100, unit: '₹' },
      ],
    },
  },

  'Home & Living': {
    icon: 'Sofa',
    subcategories: {
      Furniture: [
        { name: 'itemType', label: 'Item', type: 'select', options: ['Sofa', 'Bed', 'Dining Table', 'Wardrobe', 'Desk', 'Bookshelf', 'Chair'], required: true },
        { name: 'material', label: 'Material', type: 'select', options: ['Wood', 'Metal', 'Fabric', 'Leather', 'Engineered Wood'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good', 'Fair'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 1000, max: 200000, step: 1000, unit: '₹' },
      ],
      Appliances: [
        { name: 'itemType', label: 'Appliance', type: 'select', options: ['Refrigerator', 'Washing Machine', 'AC', 'Microwave', 'Water Purifier', 'Dishwasher', 'Geyser'], required: true },
        { name: 'brand', label: 'Brand', type: 'select', options: ['LG', 'Samsung', 'Whirlpool', 'Bosch', 'IFB', 'Voltas', 'Daikin', 'Blue Star', 'Haier', 'Godrej', 'Kent', 'Aquaguard'] },
        { name: 'condition', label: 'Condition', type: 'select', options: ['New', 'Like New', 'Good'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 2000, max: 200000, step: 1000, unit: '₹' },
      ],
      Decor: [
        { name: 'itemType', label: 'Item', type: 'select', options: ['Wall Art', 'Rugs', 'Curtains', 'Lamps', 'Vases', 'Mirrors', 'Cushions'], required: true },
        { name: 'style', label: 'Style', type: 'select', options: ['Modern', 'Traditional', 'Minimalist', 'Bohemian', 'Industrial'] },
        { name: 'price', label: 'Price (up to)', type: 'slider', min: 200, max: 50000, step: 200, unit: '₹' },
      ],
    },
  },
}

export const CATEGORY_LIST = Object.keys(CATEGORIES)

export function getSubcategories(category) {
  return category && CATEGORIES[category] ? Object.keys(CATEGORIES[category].subcategories) : []
}

export function getFields(category, subcategory) {
  if (!category || !subcategory) return []
  return CATEGORIES[category]?.subcategories?.[subcategory] || []
}
