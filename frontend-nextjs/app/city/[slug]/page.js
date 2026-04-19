import { notFound } from 'next/navigation'
import Link from 'next/link'
import { MapPin, Car, Smartphone, Home, Shirt, Sofa, ShoppingCart, ArrowRight, ChevronRight } from 'lucide-react'
import { CITY_PARAMS, SLUG_TO_CITY, getCitySeoContent, toSlug } from '../../../lib/seoUtils'
import { CATEGORIES } from '../../../features/wishlist/wishlistFieldConfig'
import { MARKETPLACE_SOURCES } from '../../../features/wishlist/mockMatches'

const categoryIcons = { Automobile: Car, Electronics: Smartphone, 'Real Estate': Home, Fashion: Shirt, 'Home & Living': Sofa }
const categoryGradients = {
  Automobile: 'from-blue-500 to-blue-600',
  Electronics: 'from-violet-500 to-violet-600',
  'Real Estate': 'from-emerald-500 to-emerald-600',
  Fashion: 'from-pink-500 to-pink-600',
  'Home & Living': 'from-amber-500 to-amber-600',
}

const FOOTER_CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']

export function generateStaticParams() {
  return CITY_PARAMS
}

export async function generateMetadata({ params }) {
  const { slug } = params
  const city = SLUG_TO_CITY.get(slug)
  if (!city) return {}
  const seo = getCitySeoContent(city)
  return {
    title: seo.metaTitle,
    description: seo.metaDescription,
    keywords: seo.keywords,
    openGraph: { title: seo.metaTitle, description: seo.metaDescription, type: 'website', url: `https://wishi.in/city/${slug}` },
    alternates: { canonical: `https://wishi.in/city/${slug}` },
  }
}

export default async function CityPage({ params }) {
  const { slug } = params
  const city = SLUG_TO_CITY.get(slug)
  if (!city) notFound()

  const seo = getCitySeoContent(city)
  const allCategories = Object.entries(CATEGORIES)
  const otherCities = FOOTER_CITIES.filter((c) => c !== city)

  // Collect all marketplaces
  const allSources = new Map()
  for (const sources of Object.values(MARKETPLACE_SOURCES)) {
    for (const s of sources) allSources.set(s.name, s)
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: seo.metaTitle,
    description: seo.metaDescription,
    url: `https://wishi.in/city/${slug}`,
    breadcrumb: {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://wishi.in' },
        { '@type': 'ListItem', position: 2, name: city },
      ],
    },
  }

  return (
    <div className="min-h-screen bg-white">
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

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <nav className="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div className="flex items-center gap-1.5 text-xs text-slate-400">
          <Link href="/" className="hover:text-sky-600 transition">Home</Link>
          <ChevronRight className="w-3 h-3" />
          <span className="text-slate-700 font-medium">{city}</span>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-500 to-sky-600 flex items-center justify-center shadow-lg">
              <MapPin className="w-7 h-7 text-white" />
            </div>
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-slate-400">City</p>
              <h1 className="text-3xl sm:text-4xl font-bold text-slate-900">{seo.headline}</h1>
            </div>
          </div>
          <p className="text-base sm:text-lg text-slate-500 max-w-3xl leading-relaxed">{seo.description}</p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">

        {/* Categories in this city */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Browse Categories in {city}</h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {allCategories.map(([catName, catData]) => {
              const CatIcon = categoryIcons[catName] || ShoppingCart
              const catGradient = categoryGradients[catName] || 'from-sky-500 to-sky-600'
              const subs = Object.keys(catData.subcategories)
              const catSlug = toSlug(catName)
              return (
                <div key={catName} className="rounded-2xl border border-gray-100 p-5 hover:shadow-lg hover:border-gray-200 transition-all">
                  <div className="flex items-center gap-3 mb-4">
                    <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${catGradient} flex items-center justify-center flex-shrink-0`}>
                      <CatIcon className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <Link href={`/category/${catSlug}`} className="text-base font-semibold text-slate-900 hover:text-sky-600 transition">
                        {catName}
                      </Link>
                      <p className="text-xs text-slate-400">{subs.length} subcategories</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {subs.map((sub) => (
                      <Link
                        key={sub}
                        href={`/items/${catSlug}/${toSlug(sub)}`}
                        className="rounded-full bg-gray-50 border border-gray-100 px-3 py-1 text-xs font-medium text-slate-600 hover:bg-sky-50 hover:text-sky-600 hover:border-sky-100 transition"
                      >
                        {sub}
                      </Link>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* Marketplaces */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Marketplaces in {city}</h2>
          <p className="text-sm text-slate-400 mb-4">WISHI searches these platforms to find listings in {city}.</p>
          <div className="flex flex-wrap gap-3">
            {[...allSources.values()].map((s) => (
              <div key={s.name} className="flex items-center gap-2 rounded-full border border-gray-100 bg-white px-4 py-2">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: s.color }} />
                <span className="text-sm font-medium text-slate-700">{s.name}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Stats */}
        <section className="mb-12 grid gap-4 sm:grid-cols-3">
          <div className="rounded-2xl border border-gray-100 p-5 text-center">
            <p className="text-3xl font-bold text-sky-600">{seo.categories.length}</p>
            <p className="text-sm text-slate-400 mt-1">Categories</p>
          </div>
          <div className="rounded-2xl border border-gray-100 p-5 text-center">
            <p className="text-3xl font-bold text-sky-600">{seo.totalSubs}</p>
            <p className="text-sm text-slate-400 mt-1">Subcategories</p>
          </div>
          <div className="rounded-2xl border border-gray-100 p-5 text-center">
            <p className="text-3xl font-bold text-sky-600">{allSources.size}+</p>
            <p className="text-sm text-slate-400 mt-1">Marketplaces</p>
          </div>
        </section>

        {/* CTA */}
        <section className="mb-12 rounded-2xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-600 p-8 sm:p-10 text-center relative overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.4),_transparent_40%)]" />
          <div className="relative">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">Looking for deals in {city}?</h2>
            <p className="mt-3 text-sm sm:text-base text-white/80 max-w-lg mx-auto">
              Create a free wishlist and let WISHI find the best matches in {city} for you.
            </p>
            <div className="mt-6">
              <Link href="/wishlist" className="rounded-full bg-white text-sky-600 hover:bg-sky-50 px-8 py-3.5 text-sm font-semibold transition shadow-lg inline-flex items-center gap-2">
                Create Your Wishlist <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </section>

        {/* Other Cities */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Explore Other Cities</h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {otherCities.map((c) => (
              <Link
                key={c}
                href={`/city/${toSlug(c)}`}
                className="group flex items-center gap-3 rounded-2xl border border-gray-100 p-4 hover:shadow-lg hover:border-gray-200 transition-all"
              >
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-sky-600 flex items-center justify-center flex-shrink-0">
                  <MapPin className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-slate-900">{c}</h3>
                  <p className="text-xs text-slate-400">Deals in {c}</p>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
