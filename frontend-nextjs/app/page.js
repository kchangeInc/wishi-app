'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronLeft, ChevronRight, Search, User, Star, Home, Sparkles } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Masonry from 'react-masonry-css'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../lib/api'

const bannerIdeas = [
  { emoji: '🚗', text: 'Honda City under ₹8L', color: 'bg-blue-50 border-blue-100 text-blue-600' },
  { emoji: '🏠', text: '2BHK for Rent in Mumbai', color: 'bg-emerald-50 border-emerald-100 text-emerald-600' },
  { emoji: '📱', text: 'iPhone 15 Pro in Budget', color: 'bg-violet-50 border-violet-100 text-violet-600' },
  { emoji: '🛵', text: 'Scooter under ₹70K', color: 'bg-orange-50 border-orange-100 text-orange-600' },
  { emoji: '💻', text: 'MacBook Pro M3 under ₹2L', color: 'bg-pink-50 border-pink-100 text-pink-600' },
  { emoji: '🏡', text: '3BHK in Pune under ₹90L', color: 'bg-teal-50 border-teal-100 text-teal-600' },
  { emoji: '🏍️', text: 'Royal Enfield Classic 350', color: 'bg-amber-50 border-amber-100 text-amber-600' },
  { emoji: '📺', text: 'Samsung 65" QLED TV', color: 'bg-cyan-50 border-cyan-100 text-cyan-600' },
]

const featureCards = [
  {
    title: 'AI-powered matching',
    description: 'Auto-match your wishlist items with top verified listings.',
    badge: 'Smart',
    image: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80',
    alt: 'User receiving match notifications',
  },
  {
    title: 'Category discovery',
    description: 'Explore trending categories instantly for the best deals.',
    badge: 'Explore',
    image: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80',
    alt: 'Laptop with marketplace browsing screen',
  },
  {
    title: 'Save boards',
    description: 'Keep your favorite deals and access them later.',
    badge: 'Save',
    image: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1200&q=80',
    alt: 'Saved wishlist cards on a tablet',
  },
  {
    title: 'Alert notifications',
    description: 'Get notified when a preferred deal appears.',
    badge: 'Alerts',
    image: 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80',
    alt: 'Phone showing notification alert',
  },
  {
    title: 'Quick search',
    description: 'Use fast search to discover exactly what you need.',
    badge: 'Fast',
    image: 'https://images.unsplash.com/photo-1517430816045-df4b7de11d1b?auto=format&fit=crop&w=1200&q=80',
    alt: 'Search results on a mobile device',
  },
]

const categories = [
  { title: 'Automobile', subtitle: 'Cars, bikes, scooters' },
  { title: 'Electronics', subtitle: 'Phones, laptops, gadgets' },
  { title: 'Real Estate', subtitle: 'Homes, rentals, land' },
  { title: 'Fashion', subtitle: 'Style, apparel, accessories' },
  { title: 'Home & Living', subtitle: 'Furniture, décor, kitchen' },
]

const latestLinks = [
  'Top smartphone deals',
  'Best budget cars under ₹6L',
  'Verified seller listings',
  'Trending home décor ideas',
  'How to build a perfect wishlist',
]

const sampleWishlists = [
  {
    id: 1,
    title: 'Honda City 2020',
    price: '₹8.5L',
    location: 'Mumbai, Maharashtra',
    category: 'Automobile',
    urgency: 'High',
    matches: 12,
  },
  {
    id: 2,
    title: 'iPhone 15 Pro Max',
    price: '₹1.2L',
    location: 'Delhi, NCR',
    category: 'Electronics',
    urgency: 'Medium',
    matches: 8,
  },
  {
    id: 3,
    title: 'Royal Enfield Classic 350',
    price: '₹2.1L',
    location: 'Bangalore, Karnataka',
    category: 'Automobile',
    urgency: 'High',
    matches: 15,
  },
  {
    id: 4,
    title: 'MacBook Pro M3',
    price: '₹2.5L',
    location: 'Chennai, Tamil Nadu',
    category: 'Electronics',
    urgency: 'Medium',
    matches: 6,
  },
  {
    id: 5,
    title: '3BHK Apartment',
    price: '₹85L',
    location: 'Pune, Maharashtra',
    category: 'Real Estate',
    urgency: 'Low',
    matches: 3,
  },
  {
    id: 6,
    title: 'Samsung 65" QLED TV',
    price: '₹1.8L',
    location: 'Hyderabad, Telangana',
    category: 'Electronics',
    urgency: 'Medium',
    matches: 9,
  },
]

function RotatingIdeas({ ideas = [] }) {
  const items = ideas.length > 0
    ? ideas.map(i => ({ emoji: i.emoji, text: i.text, color: `${i.color_bg} ${i.color_border} ${i.color_text}` }))
    : bannerIdeas
  const [visible, setVisible] = useState([0, 1, 2])

  useEffect(() => {
    const interval = setInterval(() => {
      setVisible(prev => prev.map(i => (i + 3) % items.length))
    }, 3000)
    return () => clearInterval(interval)
  }, [items.length])

  return (
    <div className="flex flex-wrap items-center gap-2">
      <span className="text-sm text-slate-400">People are looking for</span>
      <AnimatePresence mode="popLayout">
        {visible.map(idx => (
          <motion.span
            key={`${idx}-${items[idx].text}`}
            initial={{ opacity: 0, scale: 0.8, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -10 }}
            transition={{ duration: 0.3 }}
            className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-sm font-medium ${items[idx].color}`}
          >
            {items[idx].emoji} {items[idx].text}
          </motion.span>
        ))}
      </AnimatePresence>
    </div>
  )
}

function StatsBar({ apiCategories, apiWishlists }) {
  const stats = [
    { label: 'Categories', value: apiCategories.length || 5, icon: '📂' },
    { label: 'Active Wishes', value: apiWishlists.length || 0, icon: '⭐' },
    { label: 'Matches Found', value: apiWishlists.reduce((sum, w) => sum + (w.match_count || 0), 0), icon: '🎯' },
    { label: 'Marketplaces', value: '15+', icon: '🏪' },
  ]
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
      {stats.map(stat => (
        <div key={stat.label} className="rounded-2xl bg-white border border-gray-200 p-4 text-center">
          <span className="text-2xl">{stat.icon}</span>
          <p className="mt-2 text-2xl font-bold text-slate-900">{stat.value}</p>
          <p className="text-xs text-slate-500">{stat.label}</p>
        </div>
      ))}
    </div>
  )
}

function MobileBottomNav({ onHome, onSearch, onProfile }) {
  return (
    <div className="fixed inset-x-0 bottom-0 z-50 border-t border-gray-200 bg-white shadow-2xl lg:hidden">
      <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-3">
        <button onClick={onHome} className="flex flex-col items-center gap-1 text-sm font-medium text-slate-700 hover:text-sky-600">
          <Home className="h-5 w-5" />
          Home
        </button>
        <button onClick={onSearch} className="flex flex-col items-center gap-1 text-sm font-medium text-slate-700 hover:text-sky-600">
          <Search className="h-5 w-5" />
          Search
        </button>
        <button onClick={onProfile} className="flex flex-col items-center gap-1 text-sm font-medium text-slate-700 hover:text-sky-600">
          <User className="h-5 w-5" />
          Profile
        </button>
      </div>
    </div>
  )
}

function CategoryCard({ category }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      className="group rounded-3xl overflow-hidden border border-gray-200 shadow-sm bg-white hover:shadow-xl transition-shadow"
    >
      <div className="h-44 bg-cover bg-center" style={{ backgroundImage: `linear-gradient(180deg, rgba(0,0,0,0.08), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80')` }} />
      <div className="p-6">
        <h3 className="text-xl font-semibold text-slate-900">{category.title}</h3>
        <p className="mt-2 text-sm text-slate-600">{category.subtitle}</p>
        <button className="mt-5 inline-flex items-center text-sky-600 font-semibold text-sm hover:underline">View more</button>
      </div>
    </motion.article>
  )
}

function FeatureCarousel({ features, activeIndex, onSelect }) {
  return (
    <div className="flex flex-col items-center gap-4 sm:gap-6">
      {/* Phone mockup */}
      <div className="relative mx-auto w-[260px] sm:w-[280px] md:w-[300px]">
        {/* Phone frame */}
        <div className="relative rounded-[30px] sm:rounded-[36px] md:rounded-[40px] border-[5px] sm:border-[6px] border-slate-800 bg-slate-800 shadow-2xl shadow-slate-900/40 overflow-hidden">
          {/* Notch */}
          {/* <div className="absolute top-0 left-1/2 -translate-x-1/2 z-30 w-20 sm:w-24 md:w-28 h-5 sm:h-6 bg-slate-800 rounded-b-xl sm:rounded-b-2xl" /> */}
          {/* Status bar */}
          {/* <div className="absolute top-1.5 left-1/2 -translate-x-1/2 z-30 w-12 sm:w-14 md:w-16 h-1 sm:h-1.5 bg-slate-700 rounded-full" /> */}

          {/* Screen content */}
          <div className="relative h-[360px] sm:h-[420px] md:h-[480px] overflow-hidden bg-gray-100">
            {features.map((feature, index) => {
              const isActive = activeIndex === index
              return (
                <motion.div
                  key={feature.title}
                  className="absolute inset-0"
                  initial={false}
                  animate={{
                    opacity: isActive ? 1 : 0,
                    y: isActive ? 0 : index > activeIndex ? 40 : -40,
                  }}
                  transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                  style={{ zIndex: isActive ? 2 : 1 }}
                >
                  <motion.img
                    src={feature.image}
                    alt={feature.alt}
                    className="absolute inset-0 h-full w-full object-cover"
                    initial={false}
                    animate={{ scale: isActive ? 1.05 : 1 }}
                    transition={{ duration: 5, ease: 'easeOut' }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

                  {/* In-screen content */}
                  <div className="absolute bottom-0 left-0 right-0 p-3 sm:p-4 md:p-5">
                    <motion.div
                      initial={false}
                      animate={{ opacity: isActive ? 1 : 0, y: isActive ? 0 : 16 }}
                      transition={{ duration: 0.4, delay: isActive ? 0.2 : 0 }}
                    >
                      <span className="inline-flex items-center gap-1 rounded-full bg-sky-500 px-2 sm:px-2.5 py-0.5 text-[9px] sm:text-[10px] font-bold uppercase tracking-wider text-white">
                        <Star className="h-2 w-2 sm:h-2.5 sm:w-2.5 fill-white" />
                        {feature.badge}
                      </span>
                    </motion.div>
                    <motion.h3
                      initial={false}
                      animate={{ opacity: isActive ? 1 : 0, y: isActive ? 0 : 16 }}
                      transition={{ duration: 0.4, delay: isActive ? 0.3 : 0 }}
                      className="mt-1.5 sm:mt-2 text-base sm:text-lg font-bold text-white leading-tight"
                    >
                      {feature.title}
                    </motion.h3>
                    <motion.p
                      initial={false}
                      animate={{ opacity: isActive ? 1 : 0, y: isActive ? 0 : 16 }}
                      transition={{ duration: 0.4, delay: isActive ? 0.4 : 0 }}
                      className="mt-1 sm:mt-1.5 text-[10px] sm:text-xs leading-relaxed text-white/75"
                    >
                      {feature.description}
                    </motion.p>
                  </div>
                </motion.div>
              )
            })}
          </div>

          {/* Home indicator bar */}
          <div className="absolute bottom-1.5 sm:bottom-2 left-1/2 -translate-x-1/2 z-30 w-16 sm:w-20 md:w-24 h-1 bg-white/60 rounded-full" />
        </div>

        {/* Floating badge - top right outside phone */}
        {/* <motion.div
          key={`badge-${activeIndex}`}
          initial={{ opacity: 0, scale: 0.8, y: 8 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="absolute -top-2 sm:-top-3 -right-2 sm:-right-6 md:-right-10 z-20 rounded-xl sm:rounded-2xl bg-white px-2 sm:px-3 py-1.5 sm:py-2 shadow-lg border border-gray-100"
        > */}
          {/* <p className="text-[8px] sm:text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Feature</p> */}
          {/* <p className="text-xs sm:text-sm font-bold text-sky-600">{features[activeIndex].badge}</p> */}
        {/* </motion.div> */}

        {/* Floating counter - bottom left outside phone */}
        {/* <motion.div
          key={`count-${activeIndex}`}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="absolute -bottom-1 sm:-bottom-2 -left-2 sm:-left-4 md:-left-8 z-20 flex items-center gap-1 sm:gap-1.5 rounded-full bg-sky-600 px-2 sm:px-3 py-1 sm:py-1.5 shadow-lg shadow-sky-600/30"
        > */}
          {/* <span className="text-xs sm:text-sm font-bold text-white">{String(activeIndex + 1).padStart(2, '0')}</span>
          <span className="text-[9px] sm:text-[10px] text-white/60">/</span>
          <span className="text-[9px] sm:text-[10px] text-white/60">{String(features.length).padStart(2, '0')}</span> */}
        {/* </motion.div> */}
      </div>

      {/* Navigation arrows + dots */}
      <div className="flex items-center gap-3 sm:gap-4">
        <button
          onClick={() => onSelect((activeIndex + features.length - 1) % features.length)}
          className="w-8 h-8 sm:w-9 sm:h-9 flex items-center justify-center rounded-full border border-gray-200 text-slate-500 transition hover:border-sky-500 hover:text-sky-600 hover:bg-sky-50"
          aria-label="Previous feature"
        >
          <ChevronLeft className="h-4 w-4" />
        </button>
        <div className="flex items-center gap-1.5">
          {features.map((_, index) => (
            <button
              key={`dot-${index}`}
              onClick={() => onSelect(index)}
              className={`rounded-full transition-all duration-300 ${activeIndex === index ? 'w-6 sm:w-7 h-2 bg-sky-500' : 'w-2 h-2 bg-gray-200 hover:bg-gray-300'}`}
              aria-label={`Show feature ${index + 1}`}
            />
          ))}
        </div>
        <button
          onClick={() => onSelect((activeIndex + 1) % features.length)}
          className="w-8 h-8 sm:w-9 sm:h-9 flex items-center justify-center rounded-full border border-gray-200 text-slate-500 transition hover:border-sky-500 hover:text-sky-600 hover:bg-sky-50"
          aria-label="Next feature"
        >
          <ChevronRight className="h-4 w-4" />
        </button>
      </div>
    </div>
  )
}

function LatestLinks() {
  return (
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
      {latestLinks.map((item) => (
        <a key={item} href="#" className="rounded-3xl border border-gray-200 bg-white p-5 text-sm font-medium text-gray-800 transition hover:shadow-lg">
          {item}
        </a>
      ))}
    </div>
  )
}

function WishlistMasonry({ apiWishlists }) {
  const breakpointColumnsObj = {
    default: 5,
    1280: 4,
    1024: 3,
    768: 2,
    640: 1,
  }

  // Use API data if available, fallback to sample data
  const items = apiWishlists.length > 0
    ? apiWishlists.map(w => ({
        id: w.id,
        title: w.display_title || w.title,
        price: w.filters_json?.price ? `₹${Number(w.filters_json.price).toLocaleString('en-IN')}` : '',
        location: w.filters_json?.location || '',
        category: w.category || w.category_name || 'General',
        urgency: w.priority || 'Medium',
        matches: w.match_count || 0,
      }))
    : sampleWishlists

  return (
    <Masonry
      breakpointCols={breakpointColumnsObj}
      className="masonry-grid"
      columnClassName="masonry-grid-column"
    >
      {items.map((item, index) => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 + index * 0.05 }}
          className="group rounded-3xl overflow-hidden shadow-lg border border-gray-200 bg-white"
        >
          <div className="h-72 bg-cover bg-center" style={{ backgroundImage: `linear-gradient(180deg, rgba(0,0,0,0.16), rgba(0,0,0,0.08)), url('https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=900&q=80')` }} />
          <div className="p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs uppercase tracking-[0.2em] text-sky-600 font-semibold">{item.category}</span>
              <button className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700">{item.urgency}</button>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">{item.title}</h3>
            <p className="text-sm text-gray-600 mb-4">{item.location}</p>
            <div className="flex items-center justify-between text-sm text-gray-700">
              <span className="font-semibold">{item.price}</span>
              <span className="inline-flex items-center gap-1 text-yellow-600">{item.matches} matches</span>
            </div>
          </div>
        </motion.div>
      ))}
    </Masonry>
  )
}

export default function HomePage() {
  const router = useRouter()
  const { isLoggedIn } = useAuth()
  const [activeFeature, setActiveFeature] = useState(0)
  const [isPaused, setIsPaused] = useState(false)
  const [apiCategories, setApiCategories] = useState([])
  const [apiWishlists, setApiWishlists] = useState([])
  const [apiBannerIdeas, setApiBannerIdeas] = useState([])

  // Fetch dynamic data from API
  useEffect(() => {
    async function fetchData() {
      try {
        const [catRes, wlRes, bannerRes] = await Promise.all([
          api.get('/wishlist/categories'),
          api.get('/wishlist/wishlists?limit=12'),
          api.get('/wishlist/banner-ideas'),
        ])
        if (catRes.ok) setApiCategories(await catRes.json())
        if (wlRes.ok) setApiWishlists(await wlRes.json())
        if (bannerRes.ok) setApiBannerIdeas(await bannerRes.json())
      } catch (err) {
        console.error('Failed to load home data:', err)
      }
    }
    fetchData()
  }, [])

  useEffect(() => {
    if (isPaused) return

    const interval = setInterval(() => {
      setActiveFeature((current) => (current + 1) % featureCards.length)
    }, 4000)

    return () => clearInterval(interval)
  }, [isPaused])

  const handleHome = () => {
    router.push('/')
  }

  const handleSearch = () => {
    router.push('/search')
  }

  const handleProfile = () => {
    router.push(isLoggedIn ? '/dashboard' : '/')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <section className="relative overflow-hidden bg-white">
        <div className="absolute inset-y-0 left-0 w-full sm:w-1/2 bg-gradient-to-br from-sky-500/20 via-transparent to-transparent" />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 lg:py-20">
          <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] items-center">
            <div className="max-w-2xl">
              <p className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">WISHI</p>
              <h1 className="mt-6 text-5xl sm:text-6xl font-bold tracking-tight text-slate-900">
                Welcome to WISHI
              </h1>
              <p className="mt-6 text-3xl font-semibold leading-tight text-slate-900">
                Tell Us What You Want. <span className="text-sky-600">We'll Find It.</span>
              </p>
              <p className="mt-6 text-lg leading-8 text-slate-600 max-w-xl">
                WISHI is a smarter way to buy. Instead of searching across multiple platforms, simply tell us what you want — and we'll bring the best matches to you.
              </p>
              <div className="mt-5">
                <RotatingIdeas ideas={apiBannerIdeas} />
              </div>
              <p className="mt-4 text-sm text-slate-400">
                Create a wish in seconds and start receiving matching listings automatically.<br />
                No endless browsing. No missed deals. Just real demand meeting real supply.
              </p>
              <div className="mt-10 flex flex-wrap gap-4">
                <button onClick={() => router.push(isLoggedIn ? '/wishlist' : '/search')} className="pinterest-btn px-8 py-4">
                  Create Your First Wish
                </button>
                <button onClick={() => router.push('/search')} className="rounded-full border border-gray-300 px-7 py-4 text-sm font-semibold text-slate-700 hover:border-sky-600 hover:text-sky-600 transition">
                  Explore Trending Demand
                </button>
              </div>
            </div>

            <div className="grid gap-4" onMouseEnter={() => setIsPaused(true)} onMouseLeave={() => setIsPaused(false)}>
              <FeatureCarousel features={featureCards} activeIndex={activeFeature} onSelect={setActiveFeature} />
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats Bar ──────────────────────────────────────────── */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-6 relative z-10 mb-8">
        <StatsBar apiCategories={apiCategories} apiWishlists={apiWishlists} />
      </section>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="mb-14">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
            <div>
              <p className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">Top categories</p>
              <h2 className="mt-4 text-3xl sm:text-4xl font-bold text-slate-900">Category-wise top picks</h2>
            </div>
            <button onClick={() => router.push('/search')} className="pinterest-btn px-6 py-3 w-full sm:w-auto">
              {isLoggedIn ? 'Load more results' : 'Login to continue'}
            </button>
          </div>

          <div className="grid gap-6 lg:grid-cols-5">
            {(apiCategories.length > 0
              ? apiCategories.map(cat => ({ title: cat.name, subtitle: (cat.subcategories || []).map(s => s.name).join(', ') || 'Browse all' }))
              : categories
            ).map((category) => (
              <CategoryCard key={category.title} category={category} />
            ))}
          </div>
        </section>

        <section className="mb-16">
          <div className="rounded-3xl bg-white p-8 shadow-xl border border-gray-200">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
              <div>
                <p className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">Latest items</p>
                <h2 className="mt-4 text-3xl font-bold text-slate-900">Top latest item links</h2>
                <p className="mt-3 text-gray-600 max-w-2xl">Browse the most recent listings and trending searches that make your page SEO-ready.</p>
              </div>
              <button onClick={() => router.push('/search')} className="rounded-full border border-gray-300 px-6 py-3 text-sm font-semibold text-slate-700 hover:border-sky-600 hover:text-sky-600 transition w-full sm:w-auto">
                Explore latest
              </button>
            </div>

            <div className="mt-8">
              <LatestLinks />
            </div>
          </div>
        </section>

        <section className="rounded-3xl bg-white p-8 shadow-xl border border-gray-200 mb-16">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
            <div>
              <p className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">Recently added</p>
              <h2 className="mt-4 text-3xl font-bold text-slate-900">Latest wishlists and trending items</h2>
            </div>
            <button onClick={() => router.push('/search')} className="rounded-full border border-gray-300 px-6 py-3 text-sm font-semibold text-slate-700 hover:border-sky-600 hover:text-sky-600 transition w-full sm:w-auto">
              Load more ideas
            </button>
          </div>
          <div className="mt-8">
            <WishlistMasonry apiWishlists={apiWishlists} />
          </div>
        </section>

        
        <section className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] items-start mb-16">
          <div className="rounded-3xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-700 text-white p-10 shadow-2xl overflow-hidden relative">
            <div className="absolute inset-0 opacity-15 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.35),_transparent_35%)]" />
            <div className="relative">
              <p className="text-sm uppercase tracking-[0.35em] text-white/80 font-semibold">Join WISHI</p>
              <h2 className="mt-4 text-4xl sm:text-5xl font-bold tracking-tight">Ready to save, share, and match smarter?</h2>
              <p className="mt-5 text-base leading-8 text-white/90 max-w-xl">Create an account to unlock your own wishlist dashboard, save boards, and receive instant match alerts.</p>
              <button onClick={() => router.push(isLoggedIn ? '/wishlist' : '/search')} className="mt-8 pinterest-btn px-8 py-4">
                Sign up free
              </button>
            </div>
          </div>

          <div className="rounded-3xl bg-white p-8 shadow-xl border border-gray-200 flex flex-col items-center text-center">
            <p className="text-sm uppercase tracking-[0.3em] text-sky-600 font-semibold">Get Started</p>
            <h3 className="mt-4 text-2xl font-semibold text-slate-900">Join WISHI in one click</h3>
            <p className="mt-2 text-sm text-slate-500 max-w-xs">Create your account in seconds using Google Sign-In. Start creating wishes and receive matches instantly.</p>
            <button type="button" onClick={() => router.push(isLoggedIn ? '/wishlist' : '/search')} className="mt-8 flex items-center justify-center gap-3 w-full max-w-xs rounded-full border border-gray-200 bg-white hover:bg-gray-50 px-6 py-3.5 text-sm font-semibold text-slate-700 shadow-sm transition-all active:scale-[0.98]">
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Continue with Google
            </button>
            <p className="mt-6 text-xs text-gray-400">By signing up, you agree to our <a href="/terms" className="underline hover:text-sky-600">Terms</a> & <a href="/privacy" className="underline hover:text-sky-600">Privacy</a></p>
          </div>
        </section>

      </main>


      <MobileBottomNav onHome={handleHome} onSearch={handleSearch} onProfile={handleProfile} />

    </div>
  )
}
