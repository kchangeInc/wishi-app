import { INDIAN_CITIES } from './wishlistFieldConfig'

export const MARKETPLACE_SOURCES = {
  Automobile: [
    { name: 'OLX', urlTemplate: 'https://www.olx.in/items/q-{q}', color: '#002f34' },
    { name: 'CarDekho', urlTemplate: 'https://www.cardekho.com/used-cars+{q}', color: '#e23744' },
    { name: 'Cars24', urlTemplate: 'https://www.cars24.com/buy-used-cars-{q}', color: '#f5a623' },
    { name: 'CarWale', urlTemplate: 'https://www.carwale.com/used/cars-in-{q}', color: '#00b0ff' },
    { name: 'Droom', urlTemplate: 'https://droom.in/used-{q}', color: '#43a047' },
  ],
  Electronics: [
    { name: 'Amazon', urlTemplate: 'https://www.amazon.in/s?k={q}', color: '#ff9900' },
    { name: 'Flipkart', urlTemplate: 'https://www.flipkart.com/search?q={q}', color: '#2874f0' },
    { name: 'OLX', urlTemplate: 'https://www.olx.in/items/q-{q}', color: '#002f34' },
    { name: 'Croma', urlTemplate: 'https://www.croma.com/searchB?q={q}', color: '#00b050' },
    { name: 'Reliance Digital', urlTemplate: 'https://www.reliancedigital.in/search?q={q}', color: '#003399' },
  ],
  'Real Estate': [
    { name: '99acres', urlTemplate: 'https://www.99acres.com/search/property/buy/{q}', color: '#d92228' },
    { name: 'MagicBricks', urlTemplate: 'https://www.magicbricks.com/property-for-sale-in-{q}', color: '#e44d26' },
    { name: 'Housing.com', urlTemplate: 'https://housing.com/in/buy/{q}', color: '#00c1a2' },
    { name: 'NoBroker', urlTemplate: 'https://www.nobroker.in/property/sale/{q}', color: '#e53935' },
    { name: 'OLX', urlTemplate: 'https://www.olx.in/items/q-{q}', color: '#002f34' },
  ],
  Fashion: [
    { name: 'Myntra', urlTemplate: 'https://www.myntra.com/{q}', color: '#ff3e6c' },
    { name: 'Ajio', urlTemplate: 'https://www.ajio.com/search/?text={q}', color: '#3b3b3b' },
    { name: 'Amazon', urlTemplate: 'https://www.amazon.in/s?k={q}', color: '#ff9900' },
    { name: 'Flipkart', urlTemplate: 'https://www.flipkart.com/search?q={q}', color: '#2874f0' },
    { name: 'Tata CLiQ', urlTemplate: 'https://www.tatacliq.com/search/?searchCategory=all&text={q}', color: '#434ba1' },
  ],
  'Home & Living': [
    { name: 'Pepperfry', urlTemplate: 'https://www.pepperfry.com/search?q={q}', color: '#f16522' },
    { name: 'Urban Ladder', urlTemplate: 'https://www.urbanladder.com/search?q={q}', color: '#ff7043' },
    { name: 'Amazon', urlTemplate: 'https://www.amazon.in/s?k={q}', color: '#ff9900' },
    { name: 'Flipkart', urlTemplate: 'https://www.flipkart.com/search?q={q}', color: '#2874f0' },
    { name: 'HomeTown', urlTemplate: 'https://www.hometown.in/search?q={q}', color: '#c62828' },
  ],
}

const POSTED_AGO = ['Just now', '2 hours ago', '5 hours ago', '1 day ago', '2 days ago', '3 days ago', '4 days ago', '5 days ago', '1 week ago', '2 weeks ago']

const SELLER_TAGS = ['Verified Seller', 'Top Rated', 'Trusted', 'Featured', 'Premium', null, null, null, null, null]

// Seeded pseudo-random from wishlist id for deterministic results
function seededRandom(seed) {
  let s = seed
  return () => {
    s = (s * 16807 + 0) % 2147483647
    return (s - 1) / 2147483646
  }
}

function pick(arr, rng) {
  return arr[Math.floor(rng() * arr.length)]
}

function shuffle(arr, rng) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

// Title generators per category
const TITLE_PARTS = {
  Automobile: {
    Car: (f, rng) => {
      const years = ['2019', '2020', '2021', '2022', '2023', '2024']
      const y = f.year || pick(years, rng)
      const b = f.brand || pick(['Maruti Suzuki', 'Hyundai', 'Tata', 'Honda', 'Toyota'], rng)
      const m = f.model || pick(['Swift', 'Creta', 'Nexon', 'City', 'Innova'], rng)
      const ft = f.fuelType || pick(['Petrol', 'Diesel'], rng)
      return { title: `${b} ${m} ${y} ${ft}`, specs: [y, ft, f.owners || pick(['1st Owner', '2nd Owner'], rng), pick(['45,000 km', '32,000 km', '18,000 km', '67,000 km', '28,000 km'], rng)] }
    },
    Bike: (f, rng) => {
      const b = f.brand || pick(['Royal Enfield', 'Honda', 'Bajaj', 'KTM'], rng)
      const m = f.model || pick(['Classic 350', 'Pulsar', 'Duke 200', 'CB Hornet'], rng)
      const y = f.year || pick(['2021', '2022', '2023'], rng)
      return { title: `${b} ${m} ${y}`, specs: [y, f.engineCC || pick(['150-250', '250-500'], rng), pick(['12,000 km', '8,000 km', '22,000 km'], rng)] }
    },
    Scooter: (f, rng) => {
      const b = f.brand || pick(['Honda', 'TVS', 'Ola', 'Ather'], rng)
      const m = f.model || pick(['Activa 6G', 'Jupiter', 'S1 Pro', '450X'], rng)
      return { title: `${b} ${m}`, specs: [f.year || '2023', pick(['5,000 km', '3,200 km', '8,400 km'], rng)] }
    },
    Truck: (f, rng) => {
      const b = f.brand || pick(['Tata', 'Ashok Leyland', 'Eicher'], rng)
      return { title: `${b} ${f.tonnage || 'Light'} Truck`, specs: [f.year || '2022', f.fuelType || 'Diesel', f.tonnage || 'Light (3.5-7.5T)'] }
    },
    Bus: (f, rng) => {
      const b = f.brand || pick(['Tata', 'Ashok Leyland'], rng)
      return { title: `${b} ${f.seating || '35-50'} Seater Bus`, specs: [f.fuelType || 'Diesel', f.seating || '35-50 seats'] }
    },
  },
  Electronics: {
    Mobile: (f, rng) => {
      const b = f.brand || pick(['Samsung', 'Apple', 'OnePlus', 'Xiaomi'], rng)
      const models = { Samsung: 'Galaxy S24', Apple: 'iPhone 15', OnePlus: '12R', Xiaomi: '14', Realme: 'GT Neo 5', Vivo: 'V30', Oppo: 'Reno 11', Google: 'Pixel 8', Nothing: 'Phone 2', Motorola: 'Edge 50', iQOO: 'Neo 9', Poco: 'F6' }
      return { title: `${b} ${models[b] || 'Pro'} ${f.storage || '128GB'}`, specs: [f.storage || '128GB', f.ram || '8GB', f.condition || 'Like New'] }
    },
    Laptop: (f, rng) => {
      const b = f.brand || pick(['Apple', 'Dell', 'HP', 'Lenovo'], rng)
      const models = { Apple: 'MacBook Air M2', Dell: 'Inspiron 15', HP: 'Pavilion', Lenovo: 'IdeaPad Slim 5', Asus: 'Vivobook', Acer: 'Aspire 5' }
      return { title: `${b} ${models[b] || 'Pro'} ${f.processor || ''}`.trim(), specs: [f.processor || 'Intel i5', f.ram || '16GB', f.storage || '512GB SSD', f.condition || 'New'] }
    },
    TV: (f, rng) => {
      const b = f.brand || pick(['Samsung', 'LG', 'Sony'], rng)
      return { title: `${b} ${f.screenSize || '55"'} ${f.displayType || 'LED'} Smart TV`, specs: [f.screenSize || '55"', f.displayType || 'LED', f.smartTV ? 'Smart TV' : null].filter(Boolean) }
    },
    Camera: (f, rng) => {
      const b = f.brand || pick(['Canon', 'Sony', 'Nikon'], rng)
      return { title: `${b} ${f.cameraType || 'Mirrorless'} Camera ${f.megapixels || ''}`.trim(), specs: [f.cameraType || 'Mirrorless', f.megapixels || '20-30MP', f.condition || 'Like New'] }
    },
  },
  'Real Estate': {
    Rent: (f, rng) => ({ title: `${f.bhk || '2 BHK'} ${f.furnished || 'Semi-furnished'} Flat for Rent`, specs: [f.bhk || '2 BHK', f.furnished || 'Semi-furnished', f.parking ? 'Parking' : null, f.lift ? 'Lift' : null].filter(Boolean) }),
    Buy: (f, rng) => ({ title: `${f.bhk || '2 BHK'} ${f.propertyType || 'Apartment'} for Sale`, specs: [f.bhk || '2 BHK', f.propertyType || 'Apartment', f.parking ? 'Parking' : null, f.lift ? 'Lift' : null].filter(Boolean) }),
    'PG/Hostel': (f, rng) => ({ title: `${f.roomType || 'Double'} Room PG ${f.gender || 'Unisex'}`, specs: [f.roomType || 'Double', f.gender || 'Unisex', f.food ? 'Food Included' : null, f.ac ? 'AC' : null].filter(Boolean) }),
    Plot: (f, rng) => ({ title: `${f.plotType || 'Residential'} Plot ${f.plotSize ? f.plotSize + ' sq ft' : ''}`.trim(), specs: [f.plotType || 'Residential', f.plotSize ? f.plotSize + ' sq ft' : null].filter(Boolean) }),
  },
  Fashion: {
    Men: (f, rng) => {
      const b = f.brand || pick(['Nike', 'Adidas', 'Zara', 'Levi\'s'], rng)
      return { title: `${b} ${f.itemType || 'T-Shirts'} — ${f.size || 'L'}`, specs: [f.itemType || 'T-Shirts', f.size || 'L', f.condition || 'New'] }
    },
    Women: (f, rng) => {
      const b = f.brand || pick(['Zara', 'H&M', 'FabIndia'], rng)
      return { title: `${b} ${f.itemType || 'Dresses'} — ${f.size || 'M'}`, specs: [f.itemType || 'Dresses', f.size || 'M', f.condition || 'New'] }
    },
    Kids: (f, rng) => ({ title: `Kids ${f.itemType || 'Clothing'} — ${f.ageGroup || '5-10 years'}`, specs: [f.itemType || 'Clothing', f.ageGroup || '5-10 years', f.gender || 'Unisex'] }),
  },
  'Home & Living': {
    Furniture: (f, rng) => ({ title: `${f.material || 'Wood'} ${f.itemType || 'Sofa'}`, specs: [f.itemType || 'Sofa', f.material || 'Wood', f.condition || 'New'] }),
    Appliances: (f, rng) => {
      const b = f.brand || pick(['LG', 'Samsung', 'Whirlpool'], rng)
      return { title: `${b} ${f.itemType || 'Refrigerator'}`, specs: [f.itemType || 'Refrigerator', f.condition || 'Like New'] }
    },
    Decor: (f, rng) => ({ title: `${f.style || 'Modern'} ${f.itemType || 'Wall Art'}`, specs: [f.itemType || 'Wall Art', f.style || 'Modern'] }),
  },
}

export function generateMatches(wishlist) {
  if (!wishlist || !wishlist.category) return []

  const rng = seededRandom(wishlist.id || Date.now())
  const count = 6 + Math.floor(rng() * 7) // 6–12
  const sources = MARKETPLACE_SOURCES[wishlist.category] || MARKETPLACE_SOURCES.Electronics
  const fields = wishlist.fields || {}
  const sub = wishlist.subcategory || Object.keys(TITLE_PARTS[wishlist.category] || {})[0] || 'Car'
  const titleGen = TITLE_PARTS[wishlist.category]?.[sub]

  // Find the price field value from the wishlist
  const maxPrice = fields.price || 500000
  const location = fields.location || fields.city || pick(INDIAN_CITIES.slice(0, 20), rng)

  const matches = []

  for (let i = 0; i < count; i++) {
    const source = sources[i % sources.length]
    const { title, specs } = titleGen ? titleGen(fields, rng) : { title: `${sub} Listing`, specs: [] }

    // Vary the title slightly for each match
    const suffix = i > 0 ? [' — Great Deal', ' — Low KM', ' — Barely Used', ' — Like New', ' — Mint Condition', ' — Well Maintained', ' — Urgent Sale', ' — Negotiable', ' — Best Price', ' — Certified', ' — Premium'][i % 11] : ''
    const matchTitle = i === 0 ? title : title + (rng() > 0.5 ? suffix : '')

    // Price variation: 60%–120% of max price
    const priceFactor = 0.6 + rng() * 0.6
    const price = Math.round((maxPrice * priceFactor) / 100) * 100
    const formattedPrice = `₹${price.toLocaleString('en-IN')}`

    const matchScore = Math.floor(75 + rng() * 24) // 75–98
    const matchLocation = rng() > 0.3 ? location : pick(INDIAN_CITIES.slice(0, 30), rng)

    // Build search query for marketplace URL
    const query = encodeURIComponent(`${fields.brand || ''} ${sub} ${matchLocation}`.trim())
    const url = source.urlTemplate.replace('{q}', query)

    const sellerTag = pick(SELLER_TAGS, rng)
    const featured = rng() > 0.8

    matches.push({
      id: wishlist.id * 100 + i + 1,
      title: matchTitle,
      price,
      formattedPrice,
      source: { name: source.name, url, color: source.color },
      matchScore,
      location: matchLocation,
      postedAgo: POSTED_AGO[i % POSTED_AGO.length],
      specs: shuffle(specs, rng).slice(0, 2 + Math.floor(rng() * 3)),
      sellerTag,
      featured,
    })
  }

  // Sort by match score descending
  matches.sort((a, b) => b.matchScore - a.matchScore)
  return matches
}

export function getMatchCount(wishlist) {
  if (!wishlist || !wishlist.category) return 0
  const rng = seededRandom(wishlist.id || Date.now())
  return 6 + Math.floor(rng() * 7)
}
