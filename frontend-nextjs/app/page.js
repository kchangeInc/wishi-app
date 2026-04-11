'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ChevronLeft, ChevronRight, Heart, Search, ShoppingCart, User, Menu, X, Star, Home } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Masonry from 'react-masonry-css'

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

function Header({ onLoginClick, onSearchSubmit }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearchSubmit = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      onSearchSubmit(searchQuery.trim())
    }
  }

  return (
    <header className="pinterest-nav">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-sky-600 flex items-center justify-center text-white shadow-sm">
              <ShoppingCart className="w-5 h-5" />
            </div>
            <span className="text-xl sm:text-2xl font-bold tracking-tight text-sky-600">WISHI</span>
          </div>

          <div className="hidden lg:flex flex-1 justify-center max-w-md">
            <form onSubmit={handleSearchSubmit} className="w-full">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search for products, categories..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-sky-600 focus:border-transparent"
                />
              </div>
            </form>
          </div>

          <div className="hidden md:flex items-center gap-4">
            <nav className="flex items-center gap-6 text-sm font-medium">
              <a href="#" className="text-slate-700 hover:text-sky-600 transition">About</a>
              <a href="#" className="text-slate-700 hover:text-sky-600 transition">How It Works</a>
              <a href="#" className="text-slate-700 hover:text-sky-600 transition">Login</a>
            </nav>
            <button onClick={() => onLoginClick('register')} className="rounded-full bg-sky-600 px-5 py-2 text-sm font-semibold text-white hover:bg-sky-700 transition">
              Signup
            </button>
          </div>

          <button className="md:hidden p-2 rounded-lg border border-gray-200" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {menuOpen && (
          <div className="mt-4 space-y-4 border-t border-gray-200 py-4 md:hidden">
            <form onSubmit={handleSearchSubmit} className="px-2">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-sky-600 focus:border-transparent"
                />
              </div>
            </form>
            <button className="block w-full text-left text-gray-700 hover:text-sky-600">About</button>
            <button className="block w-full text-left text-gray-700 hover:text-sky-600">How It Works</button>
            <button className="block w-full text-left text-gray-700 hover:text-sky-600">Login</button>
            <button onClick={() => onLoginClick('login')} className="block w-full text-left text-sky-600 font-semibold">Sign in</button>
          </div>
        )}
      </div>
    </header>
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

function FeatureCard({ feature, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.12 + index * 0.05 }}
      className="group rounded-3xl overflow-hidden border border-gray-200 shadow-sm bg-white hover:shadow-xl transition-shadow"
    >
      <div className="h-44 bg-cover bg-center" style={{ backgroundImage: `linear-gradient(180deg, rgba(255,255,255,0.2), rgba(0,0,0,0.2)), url('https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=1200&q=80')` }} />
      <div className="p-6">
        <span className="inline-flex rounded-full bg-sky-100 text-sky-600 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em]">{feature.badge}</span>
        <h3 className="mt-4 text-xl font-semibold text-slate-900">{feature.title}</h3>
        <p className="mt-3 text-sm leading-6 text-slate-600">{feature.description}</p>
      </div>
    </motion.div>
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
    <div className="space-y-4">
      <div className="relative mx-auto w-full max-w-4xl h-[420px] sm:h-[480px] lg:h-[520px] overflow-hidden rounded-[32px] bg-white shadow-2xl">
        {features.map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={false}
            animate={activeIndex === index ? { opacity: 1, x: 0 } : { opacity: 0, x: index < activeIndex ? -40 : 40 }}
            transition={{ duration: 0.45 }}
            className={`absolute inset-0 flex flex-col justify-end p-8 text-white transition-all ${activeIndex === index ? 'relative opacity-100' : 'opacity-0 pointer-events-none'}`}
          >
            <img src={feature.image} alt={feature.alt} className="absolute inset-0 h-full w-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/30 to-transparent" />
            <div className="relative z-10 max-w-xl rounded-[28px] bg-white/85 p-6 shadow-2xl backdrop-blur-sm text-slate-900">
              <span className="inline-flex rounded-full bg-sky-100 text-sky-600 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em]">
                {feature.badge}
              </span>
              <h3 className="mt-4 text-3xl font-semibold">{feature.title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-700">{feature.description}</p>
            </div>
          </motion.div>
        ))}

        <button
          onClick={() => onSelect((activeIndex + features.length - 1) % features.length)}
          className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-3 text-slate-700 shadow-lg ring-1 ring-slate-200 transition hover:bg-white sm:left-4"
          aria-label="Previous feature"
        >
          <ChevronLeft className="h-5 w-5" />
        </button>
        <button
          onClick={() => onSelect((activeIndex + 1) % features.length)}
          className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-3 text-slate-700 shadow-lg ring-1 ring-slate-200 transition hover:bg-white sm:right-4"
          aria-label="Next feature"
        >
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>

      <div className="flex items-center justify-center gap-2">
        {features.map((_, index) => (
          <button
            key={`dot-${index}`}
            onClick={() => onSelect(index)}
            className={`h-2.5 w-2.5 rounded-full transition ${activeIndex === index ? 'bg-sky-600' : 'bg-slate-300 hover:bg-slate-400'}`}
            aria-label={`Show feature ${index + 1}`}
          />
        ))}
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

function WishlistMasonry() {
  const breakpointColumnsObj = {
    default: 5,
    1280: 4,
    1024: 3,
    768: 2,
    640: 1,
  }

  return (
    <Masonry
      breakpointCols={breakpointColumnsObj}
      className="masonry-grid"
      columnClassName="masonry-grid-column"
    >
      {sampleWishlists.map((item, index) => (
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
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState('register')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activeFeature, setActiveFeature] = useState(0)
  const [isPaused, setIsPaused] = useState(false)

  useEffect(() => {
    if (isPaused) return

    const interval = setInterval(() => {
      setActiveFeature((current) => (current + 1) % featureCards.length)
    }, 4000)

    return () => clearInterval(interval)
  }, [isPaused])

  const handleAction = (mode = 'login') => {
    if (!isLoggedIn) {
      setAuthMode(mode)
      setShowAuthModal(true)
      return
    }
    router.push('/search')
  }

  const handleSearchSubmit = (query) => {
    router.push(`/search?q=${encodeURIComponent(query)}`)
  }

  const handleHome = () => {
    router.push('/')
  }

  const handleSearch = () => {
    router.push('/search')
  }

  const handleProfile = () => {
    if (!isLoggedIn) {
      setAuthMode('login')
      setShowAuthModal(true)
      return
    }
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-28">
      <Header onLoginClick={handleAction} onSearchSubmit={handleSearchSubmit} />

      <section className="relative overflow-hidden bg-white">
        <div className="absolute inset-y-0 left-0 w-full sm:w-1/2 bg-gradient-to-br from-sky-500/20 via-transparent to-transparent" />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 lg:py-20">
          <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] items-center">
            <div className="max-w-2xl">
              <p className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">Stop Searching</p>
              <h1 className="mt-6 text-5xl sm:text-6xl font-bold tracking-tight text-slate-900">
                Start Wishing
              </h1>
              <p className="mt-6 text-3xl font-semibold leading-tight text-slate-900">
                Find Your <span className="text-sky-600">Ride</span> <span className="text-slate-500">Scooter, Bike</span> OR <span className="text-slate-500">Car</span>
              </p>
              <p className="mt-6 text-lg leading-8 text-slate-600 max-w-xl">
                Find your ride with a clean marketplace experience built for fast discovery, curated listings, and instant activity.
              </p>
              <div className="mt-10 flex flex-wrap gap-4">
                <button onClick={() => handleAction('register')} className="pinterest-btn px-8 py-4">
                  Join Wishi for Free
                </button>
                <button onClick={() => handleAction('login')} className="rounded-full border border-gray-300 px-7 py-4 text-sm font-semibold text-slate-700 hover:border-sky-600 hover:text-sky-600 transition">
                  I have a Wishi Account
                </button>
              </div>
            </div>

            <div className="grid gap-4" onMouseEnter={() => setIsPaused(true)} onMouseLeave={() => setIsPaused(false)}>
              <FeatureCarousel features={featureCards} activeIndex={activeFeature} onSelect={setActiveFeature} />
            </div>
          </div>
        </div>
      </section>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="mb-14">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
            <div>
              <p className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">Top categories</p>
              <h2 className="mt-4 text-3xl sm:text-4xl font-bold text-slate-900">Category-wise top picks</h2>
            </div>
            <button onClick={() => handleAction('login')} className="pinterest-btn px-6 py-3 w-full sm:w-auto">
              {isLoggedIn ? 'Load more results' : 'Login to continue'}
            </button>
          </div>

          <div className="grid gap-6 lg:grid-cols-5">
            {categories.map((category) => (
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
              <button onClick={() => handleAction('login')} className="rounded-full border border-gray-300 px-6 py-3 text-sm font-semibold text-slate-700 hover:border-sky-600 hover:text-sky-600 transition w-full sm:w-auto">
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
            <button onClick={() => handleAction('login')} className="rounded-full border border-gray-300 px-6 py-3 text-sm font-semibold text-slate-700 hover:border-sky-600 hover:text-sky-600 transition w-full sm:w-auto">
              Load more ideas
            </button>
          </div>
          <div className="mt-8">
            <WishlistMasonry />
          </div>
        </section>

        
        <section className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] items-start mb-16">
          <div className="rounded-3xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-700 text-white p-10 shadow-2xl overflow-hidden relative">
            <div className="absolute inset-0 opacity-15 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.35),_transparent_35%)]" />
            <div className="relative">
              <p className="text-sm uppercase tracking-[0.35em] text-white/80 font-semibold">Join WISHI</p>
              <h2 className="mt-4 text-4xl sm:text-5xl font-bold tracking-tight">Ready to save, share, and match smarter?</h2>
              <p className="mt-5 text-base leading-8 text-white/90 max-w-xl">Create an account to unlock your own wishlist dashboard, save boards, and receive instant match alerts.</p>
              <button onClick={() => handleAction('register')} className="mt-8 pinterest-btn px-8 py-4">
                Sign up free
              </button>
            </div>
          </div>

          <div className="rounded-3xl bg-white p-8 shadow-xl border border-gray-200">
            <p className="text-sm uppercase tracking-[0.3em] text-sky-100 font-semibold">Register</p>
            <h3 className="mt-4 text-2xl font-semibold text-slate-900">Create your WISHI account in seconds</h3>
            <form className="mt-8 space-y-4">
              <input type="text" aria-label="Full name" placeholder="Full name" className="pinterest-input w-full" />
              <input type="email" aria-label="Email" placeholder="Email address" className="pinterest-input w-full" />
              <input type="password" aria-label="Password" placeholder="Create password" className="pinterest-input w-full" />
              <button type="button" onClick={() => setShowAuthModal(true)} className="pinterest-btn w-full py-3">
                Create account
              </button>
            </form>
            <p className="mt-6 text-sm text-gray-500">Already have an account? <button type="button" onClick={() => handleAction('login')} className="font-semibold text-sky-600">Log in</button></p>
          </div>
        </section>

      </main>

      <footer className="border-t border-gray-200 bg-white py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid gap-8 lg:grid-cols-[1.3fr_0.7fr] items-center">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-sky-600 font-semibold">WISHI</p>
              <p className="mt-4 text-gray-600 max-w-2xl">A modern marketplace for wishlists and curated deals with a Pinterest-inspired browsing experience.</p>
            </div>
            <div className="grid gap-2 text-sm text-gray-600">
              <a href="#" className="hover:text-sky-600">Terms of Service</a>
              <a href="#" className="hover:text-sky-600">Privacy Policy</a>
              <a href="#" className="hover:text-sky-600">Help Center</a>
            </div>
          </div>
          <div className="mt-8 text-center text-sm text-gray-500">© 2026 WISHI. All rights reserved.</div>
        </div>
      </footer>

      <MobileBottomNav onHome={handleHome} onSearch={handleSearch} onProfile={handleProfile} />

      {showAuthModal && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center px-4 py-6">
          <div className="w-full max-w-2xl rounded-[32px] bg-white shadow-2xl overflow-hidden">
            <div className="flex flex-col gap-3 px-8 py-6 border-b border-gray-200 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-3xl font-bold text-slate-900">{authMode === 'login' ? 'Welcome back' : 'Create your account'}</h2>
                <p className="mt-2 text-sm text-slate-600">{authMode === 'login' ? 'Sign in to access saved boards and instant match alerts.' : 'Join WISHI for personalized discovery and wishlist matching.'}</p>
              </div>
              <button onClick={() => setShowAuthModal(false)} className="text-slate-500 hover:text-slate-900">Close</button>
            </div>
            <div className="px-8 py-8">
              {authMode === 'register' ? (
                <div className="grid gap-4">
                  <input type="text" placeholder="Full name" className="pinterest-input w-full" />
                  <input type="email" placeholder="Email address" className="pinterest-input w-full" />
                  <input type="password" placeholder="Password" className="pinterest-input w-full" />
                  <button onClick={() => setIsLoggedIn(true)} className="pinterest-btn w-full py-3">Create account</button>
                  <button className="w-full rounded-full border border-gray-200 py-3 text-sm text-slate-700 hover:bg-gray-50" onClick={() => setAuthMode('login')}>
                    Already have an account? Log in
                  </button>
                </div>
              ) : (
                <div className="grid gap-4">
                  <input type="email" placeholder="Email address" className="pinterest-input w-full" />
                  <input type="password" placeholder="Password" className="pinterest-input w-full" />
                  <button onClick={() => setIsLoggedIn(true)} className="pinterest-btn w-full py-3">Log in</button>
                  <button className="w-full rounded-full border border-gray-200 py-3 text-sm text-slate-700 hover:bg-gray-50" onClick={() => setAuthMode('register')}>
                    Create a new account
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
