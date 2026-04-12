import { CATEGORIES } from '../features/wishlist/wishlistFieldConfig'
import { MARKETPLACE_SOURCES } from '../features/wishlist/mockMatches'

// Slug conversion
export function toSlug(name) {
  return name.toLowerCase().replace(/&/g, '').replace(/\//g, '-').replace(/\s+/g, '-').replace(/-+/g, '-').trim()
}

// Build reverse lookup maps
const catMap = new Map()
const subMap = new Map()
const allParams = []

for (const [catName, catData] of Object.entries(CATEGORIES)) {
  const catSlug = toSlug(catName)
  catMap.set(catSlug, catName)
  for (const subName of Object.keys(catData.subcategories)) {
    const subSlug = toSlug(subName)
    subMap.set(`${catSlug}/${subSlug}`, { category: catName, subcategory: subName })
    allParams.push({ category: catSlug, subcategory: subSlug })
  }
}

export const SLUG_TO_CATEGORY = catMap
export const SLUG_TO_SUBCATEGORY = subMap
export const ALL_PARAMS = allParams

// Category-level params (5 routes)
export const CATEGORY_PARAMS = Object.keys(CATEGORIES).map((c) => ({ slug: toSlug(c) }))

// City SEO data
const FOOTER_CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']
const cityMap = new Map()
const cityParams = []
for (const city of FOOTER_CITIES) {
  const slug = toSlug(city)
  cityMap.set(slug, city)
  cityParams.push({ slug })
}
export const SLUG_TO_CITY = cityMap
export const CITY_PARAMS = cityParams

export function getCategorySeoContent(category) {
  const subs = Object.keys(CATEGORIES[category]?.subcategories || {})
  const sources = MARKETPLACE_SOURCES[category] || []
  const sourceNames = sources.map((s) => s.name)
  return {
    metaTitle: `${category} on WISHI | Browse ${subs.join(', ')} Deals`,
    metaDescription: `Explore ${category} listings on WISHI. Browse ${subs.join(', ')} from ${sourceNames.join(', ')}. Create a free wishlist and get matched automatically.`,
    keywords: [category.toLowerCase(), ...subs.map((s) => s.toLowerCase()), ...sourceNames, 'WISHI', 'demand marketplace'],
    headline: `Explore ${category} on WISHI`,
    description: `Browse all ${category} subcategories — ${subs.join(', ')} — and find the best deals from ${sourceNames.join(', ')}. Create a wishlist and let WISHI match you automatically.`,
    subcategories: subs,
    sourceNames,
    sources,
  }
}

export function getCitySeoContent(city) {
  const allCats = Object.keys(CATEGORIES)
  const totalSubs = Object.values(CATEGORIES).reduce((acc, c) => acc + Object.keys(c.subcategories).length, 0)
  return {
    metaTitle: `WISHI ${city} | Find the Best Deals in ${city}`,
    metaDescription: `Looking for deals in ${city}? WISHI searches top marketplaces to find ${city}'s best listings across ${allCats.join(', ')}. Create a free wishlist today.`,
    keywords: [`${city} deals`, `buy in ${city}`, ...allCats.map((c) => `${c.toLowerCase()} ${city}`), 'WISHI', 'demand marketplace'],
    headline: `Find the Best Deals in ${city}`,
    description: `WISHI helps you find the best listings in ${city} across ${allCats.length} categories and ${totalSubs} subcategories. Tell us what you want and we'll bring the best matches from top marketplaces.`,
    categories: allCats,
    totalSubs,
  }
}

// Deterministic hash for stable fake wishlist IDs
function simpleHash(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i)
    hash |= 0
  }
  return Math.abs(hash) || 1
}

// Build a fake wishlist for generating sample matches
export function buildFakeWishlist(category, subcategory) {
  const fields = {}
  const fieldConfig = CATEGORIES[category]?.subcategories?.[subcategory] || []

  for (const f of fieldConfig) {
    if (f.type === 'select' && f.options?.length) {
      fields[f.name] = f.options[0]
    } else if (f.type === 'slider') {
      fields[f.name] = Math.round((f.min + f.max) / 2)
    } else if (f.type === 'autocomplete' && f.options?.length) {
      fields[f.name] = f.options[0]
    } else if (f.type === 'toggle') {
      fields[f.name] = false
    }
  }

  return {
    id: simpleHash(`${category}:${subcategory}`),
    category,
    subcategory,
    fields,
  }
}

// Build SEO content for each category:subcategory
export function getSeoContent(category, subcategory) {
  const fieldConfig = CATEGORIES[category]?.subcategories?.[subcategory] || []
  const sources = MARKETPLACE_SOURCES[category] || []
  const sourceNames = sources.map((s) => s.name)

  const brandField = fieldConfig.find((f) => f.name === 'brand')
  const brands = brandField?.options || []

  const priceField = fieldConfig.find((f) => f.type === 'slider')
  const priceMin = priceField?.min || 0
  const priceMax = priceField?.max || 0
  const priceUnit = priceField?.unit || '₹'

  const formatPrice = (v) => `${priceUnit}${v.toLocaleString('en-IN')}`

  const keyFilters = fieldConfig
    .filter((f) => f.type === 'select' || f.type === 'autocomplete')
    .map((f) => f.label)

  const metaTitle = `Find ${subcategory} on WISHI | Best ${subcategory} Deals from ${sourceNames.slice(0, 3).join(', ')}`
  const metaDescription = `Looking for ${subcategory} in ${category}? WISHI finds the best matches from ${sourceNames.join(', ')}. ${brands.length ? `Top brands: ${brands.slice(0, 5).join(', ')}. ` : ''}Budget range ${formatPrice(priceMin)} to ${formatPrice(priceMax)}. Create a free wishlist today.`

  const keywords = [
    `buy ${subcategory.toLowerCase()}`,
    `${subcategory.toLowerCase()} deals India`,
    `best ${subcategory.toLowerCase()} price`,
    category.toLowerCase(),
    ...brands.slice(0, 5).map((b) => `${b} ${subcategory.toLowerCase()}`),
    ...sourceNames.map((s) => `${subcategory.toLowerCase()} on ${s}`),
    'WISHI',
    'demand marketplace',
  ]

  const headline = `Find the Best ${subcategory} on WISHI`
  const description = brands.length
    ? `Browse ${subcategory} listings from ${sourceNames.join(', ')} and more. Top brands include ${brands.slice(0, 6).join(', ')}. Set your budget between ${formatPrice(priceMin)} and ${formatPrice(priceMax)}, and WISHI will find matches for you automatically.`
    : `Explore ${subcategory} options in the ${category} category. Set your preferences and budget between ${formatPrice(priceMin)} and ${formatPrice(priceMax)}, and WISHI scans ${sourceNames.join(', ')} to bring you the best matches.`

  return {
    metaTitle,
    metaDescription,
    keywords,
    headline,
    description,
    brands,
    priceMin,
    priceMax,
    priceUnit,
    formatPrice,
    keyFilters,
    sourceNames,
    sources,
  }
}
