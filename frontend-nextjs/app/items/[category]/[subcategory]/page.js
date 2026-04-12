import { notFound } from 'next/navigation'
import Link from 'next/link'
import { Car, Smartphone, Home, Shirt, Sofa, ShoppingCart, ArrowRight, ChevronRight } from 'lucide-react'
import { ALL_PARAMS, SLUG_TO_CATEGORY, SLUG_TO_SUBCATEGORY, buildFakeWishlist, getSeoContent, toSlug } from '../../../../lib/seoUtils'
import { CATEGORIES } from '../../../../features/wishlist/wishlistFieldConfig'
import { generateMatches, MARKETPLACE_SOURCES } from '../../../../features/wishlist/mockMatches'
import MatchCardStatic from '../../../../components/MatchCardStatic'
import Footer from '../../../../components/Footer'

const categoryIcons = { Automobile: Car, Electronics: Smartphone, 'Real Estate': Home, Fashion: Shirt, 'Home & Living': Sofa }
const categoryGradients = {
  Automobile: 'from-blue-500 to-blue-600',
  Electronics: 'from-violet-500 to-violet-600',
  'Real Estate': 'from-emerald-500 to-emerald-600',
  Fashion: 'from-pink-500 to-pink-600',
  'Home & Living': 'from-amber-500 to-amber-600',
}

export function generateStaticParams() {
  return ALL_PARAMS
}

export async function generateMetadata({ params }) {
  const { category: catSlug, subcategory: subSlug } = params
  const entry = SLUG_TO_SUBCATEGORY.get(`${catSlug}/${subSlug}`)
  if (!entry) return {}

  const seo = getSeoContent(entry.category, entry.subcategory)
  return {
    title: seo.metaTitle,
    description: seo.metaDescription,
    keywords: seo.keywords,
    openGraph: {
      title: seo.metaTitle,
      description: seo.metaDescription,
      type: 'website',
      url: `https://wishi.in/items/${catSlug}/${subSlug}`,
    },
    alternates: {
      canonical: `https://wishi.in/items/${catSlug}/${subSlug}`,
    },
  }
}

export default async function ItemDetailPage({ params }) {
  const { category: catSlug, subcategory: subSlug } = params
  const catName = SLUG_TO_CATEGORY.get(catSlug)
  const entry = SLUG_TO_SUBCATEGORY.get(`${catSlug}/${subSlug}`)
  if (!catName || !entry) notFound()

  const { category, subcategory } = entry
  const seo = getSeoContent(category, subcategory)
  const fakeWishlist = buildFakeWishlist(category, subcategory)
  const matches = generateMatches(fakeWishlist)
  const Icon = categoryIcons[category] || ShoppingCart
  const gradient = categoryGradients[category] || 'from-sky-500 to-sky-600'
  const sources = MARKETPLACE_SOURCES[category] || []

  // Build cross-links (other subcategories)
  const crossLinks = []
  for (const [cat, data] of Object.entries(CATEGORIES)) {
    for (const sub of Object.keys(data.subcategories)) {
      if (cat === category && sub === subcategory) continue
      crossLinks.push({ category: cat, subcategory: sub, catSlug: toSlug(cat), subSlug: toSlug(sub) })
    }
  }

  // JSON-LD
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: seo.metaTitle,
    description: seo.metaDescription,
    url: `https://wishi.in/items/${catSlug}/${subSlug}`,
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://wishi.in' },
        { '@type': 'ListItem', position: 2, name: category, item: `https://wishi.in/items/${catSlug}/${toSlug(Object.keys(CATEGORIES[category].subcategories)[0])}` },
        { '@type': 'ListItem', position: 3, name: subcategory },
      ],
    },
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Minimal SEO Header */}
      <header className="border-b border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center text-white">
              <ShoppingCart className="w-4 h-4" />
            </div>
            <span className="text-lg font-bold tracking-tight text-sky-600">WISHI</span>
          </Link>
          <Link href="/wishlist" className="rounded-full bg-sky-600 hover:bg-sky-700 text-white px-5 py-2 text-sm font-semibold transition">
            Create Wishlist
          </Link>
        </div>
      </header>

      {/* JSON-LD */}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      {/* Breadcrumb */}
      <nav className="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <Link href="/" className="hover:text-sky-600 transition">Home</Link>
          <ChevronRight className="w-3 h-3" />
          <span className="text-slate-500">{category}</span>
          <ChevronRight className="w-3 h-3" />
          <span className="text-slate-700 font-medium">{subcategory}</span>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
          <div className="flex items-center gap-4 mb-6">
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center shadow-lg`}>
              <Icon className="w-7 h-7 text-white" />
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-400">{category}</p>
              <h1 className="text-3xl sm:text-4xl font-bold text-slate-900">{seo.headline}</h1>
            </div>
          </div>
          <p className="text-base sm:text-lg text-slate-500 max-w-3xl leading-relaxed">{seo.description}</p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">

        {/* Brands */}
        {seo.brands.length > 0 && (
          <section className="mb-12">
            <h2 className="text-lg font-bold text-slate-900 mb-4">Popular {subcategory} Brands</h2>
            <div className="flex flex-wrap gap-2">
              {seo.brands.map((brand) => (
                <span key={brand} className="rounded-full bg-gray-50 border border-gray-100 px-3.5 py-1.5 text-sm font-medium text-slate-600">
                  {brand}
                </span>
              ))}
            </div>
          </section>
        )}

        {/* Price Range + Filters */}
        <section className="mb-12 grid gap-4 sm:grid-cols-2">
          <div className="rounded-2xl border border-gray-100 p-5">
            <h3 className="text-sm font-bold text-slate-900 mb-2">Price Range</h3>
            <p className="text-2xl font-bold text-sky-600">
              {seo.formatPrice(seo.priceMin)} — {seo.formatPrice(seo.priceMax)}
            </p>
            <p className="text-xs text-slate-400 mt-1">Set your own budget when creating a wishlist</p>
          </div>
          <div className="rounded-2xl border border-gray-100 p-5">
            <h3 className="text-sm font-bold text-slate-900 mb-2">Available Filters</h3>
            <div className="flex flex-wrap gap-1.5">
              {seo.keyFilters.map((f) => (
                <span key={f} className="rounded-full bg-sky-50 px-2.5 py-1 text-xs font-medium text-sky-600">{f}</span>
              ))}
            </div>
          </div>
        </section>

        {/* Marketplace Sources */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">We Search These Marketplaces</h2>
          <div className="flex flex-wrap gap-3">
            {sources.map((s) => (
              <div key={s.name} className="flex items-center gap-2 rounded-full border border-gray-100 bg-white px-4 py-2">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: s.color }} />
                <span className="text-sm font-medium text-slate-700">{s.name}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Sample Listings */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Sample {subcategory} Listings</h2>
          <p className="text-sm text-slate-400 mb-6">These are example matches. Create a wishlist to get personalized results.</p>
          <div className="columns-1 sm:columns-2 lg:columns-3 gap-4">
            {matches.map((match) => (
              <MatchCardStatic key={match.id} match={match} />
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="mb-12 rounded-2xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-600 p-8 sm:p-10 text-center relative overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.4),_transparent_40%)]" />
          <div className="relative">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">
              Looking for {subcategory}?
            </h2>
            <p className="mt-3 text-sm sm:text-base text-white/80 max-w-lg mx-auto">
              Create a free wishlist with your preferences and let WISHI find the best matches for you.
            </p>
            <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link
                href="/wishlist"
                className="rounded-full bg-white text-sky-600 hover:bg-sky-50 px-8 py-3.5 text-sm font-semibold transition shadow-lg inline-flex items-center gap-2"
              >
                Create Your Wishlist
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </section>

        {/* Cross-links */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Explore Other Categories</h2>
          <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {crossLinks.slice(0, 18).map((link) => (
              <Link
                key={`${link.catSlug}/${link.subSlug}`}
                href={`/items/${link.catSlug}/${link.subSlug}`}
                className="flex items-center justify-between rounded-xl border border-gray-100 px-4 py-3 hover:border-gray-200 hover:shadow-sm transition"
              >
                <div>
                  <span className="text-sm font-medium text-slate-700">{link.subcategory}</span>
                  <span className="text-xs text-slate-400 ml-2">{link.category}</span>
                </div>
                <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
              </Link>
            ))}
          </div>
        </section>
      </div>

      <Footer />
    </div>
  )
}
