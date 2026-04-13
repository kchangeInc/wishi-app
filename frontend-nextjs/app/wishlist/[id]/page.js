'use client'

import { useEffect, useState, useMemo } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { MapPin, ExternalLink, ChevronLeft, ArrowUpDown, ShieldCheck, Sparkles, Car, Smartphone, Home, Shirt, Sofa, Tag, Check, Heart, X } from 'lucide-react'
import { motion } from 'framer-motion'
import Header from '../../../components/Header'
import Footer from '../../../components/Footer'
import { useAuth } from '../../../contexts/AuthContext'
import { generateMatches, MARKETPLACE_SOURCES } from '../../../features/wishlist/mockMatches'
import { getFields } from '../../../features/wishlist/wishlistFieldConfig'
import { api } from '../../../lib/api'

const categoryIcons = { Automobile: Car, Electronics: Smartphone, 'Real Estate': Home, Fashion: Shirt, 'Home & Living': Sofa }
const categoryGradients = {
  Automobile: 'from-blue-400 to-blue-600',
  Electronics: 'from-violet-400 to-violet-600',
  'Real Estate': 'from-emerald-400 to-emerald-600',
  Fashion: 'from-pink-400 to-pink-600',
  'Home & Living': 'from-amber-400 to-amber-600',
}

function scoreColor(score) {
  if (score >= 90) return 'text-emerald-700 bg-emerald-50 border-emerald-200'
  if (score >= 80) return 'text-amber-700 bg-amber-50 border-amber-200'
  return 'text-slate-600 bg-gray-50 border-gray-200'
}

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.05 } } }
const cardAnim = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.35 } } }

export default function MatchesPage() {
  const router = useRouter()
  const params = useParams()
  const { isLoggedIn } = useAuth()
  const [wishlist, setWishlist] = useState(null)
  const [apiMatches, setApiMatches] = useState(null)
  const [sortBy, setSortBy] = useState('match')
  const [activeMarketplaces, setActiveMarketplaces] = useState([])
  const [removedIds, setRemovedIds] = useState(new Set())
  const [favouriteIds, setFavouriteIds] = useState(new Set())
  useEffect(() => {
    if (!isLoggedIn) { router.push('/'); return }

    // Try API first for wishlist details
    api.get(`/wishlist/wishlists/${params.id}`).then((res) => {
      if (res.ok) return res.json()
      return null
    }).then((data) => {
      if (data) {
        setWishlist(data)
        initMarketplaces(data)
      } else throw new Error('not found')
    }).catch(() => {
      // Fallback to localStorage
      const stored = localStorage.getItem('wishi_wishlists')
      if (stored) {
        const all = JSON.parse(stored)
        const found = all.find((w) => String(w.id) === String(params.id))
        if (found) {
          setWishlist(found)
          initMarketplaces(found)
        } else {
          router.push('/wishlist')
        }
      } else {
        router.push('/wishlist')
      }
    })

    // Try to load matches from API
    api.get(`/wishlist/wishlists/${params.id}/matches`).then((res) => {
      if (res.ok) return res.json()
      return null
    }).then((data) => {
      if (data && data.length > 0) {
        setApiMatches(data.map((m) => ({
          id: m.id,
          title: m.title || m.product_title,
          price: m.price,
          formattedPrice: m.formatted_price || `₹${Number(m.price).toLocaleString('en-IN')}`,
          location: m.location || m.city || '',
          matchScore: m.score || m.match_score || 0,
          source: { name: m.source_name || m.marketplace_source || 'Unknown', color: m.source_color || '#6b7280', url: m.source_url || m.url || '#' },
          specs: m.specs || [],
          sellerTag: m.seller_tag || null,
          featured: m.is_featured || false,
          postedAgo: m.posted_ago || '',
          is_favourite: m.is_favourite || false,
        })))
        // Set initial favourites from API response
        const favIds = new Set(data.filter((m) => m.is_favourite).map((m) => m.id))
        setFavouriteIds(favIds)
      }
    }).catch(() => { /* will use mock matches */ })

    // Load removed and favourited match ids from localStorage as fallback
    const removed = localStorage.getItem(`wishi_removed_${params.id}`)
    if (removed) setRemovedIds(new Set(JSON.parse(removed)))
    const favs = localStorage.getItem(`wishi_favourites_${params.id}`)
    if (favs) setFavouriteIds((prev) => prev.size > 0 ? prev : new Set(JSON.parse(favs)))
  }, [isLoggedIn, params.id, router])

  const initMarketplaces = (wl) => {
    if (wl.preferredMarketplaces && wl.preferredMarketplaces.length > 0) {
      setActiveMarketplaces(wl.preferredMarketplaces)
    } else {
      const sources = MARKETPLACE_SOURCES[wl.category] || []
      setActiveMarketplaces(sources.map((s) => s.name))
    }
  }

  const matches = useMemo(() => {
    if (apiMatches && apiMatches.length > 0) return apiMatches
    return wishlist ? generateMatches(wishlist) : []
  }, [wishlist, apiMatches])

  const toggleFavourite = async (matchId) => {
    const isFav = favouriteIds.has(matchId)
    setFavouriteIds((prev) => {
      const next = new Set(prev)
      if (next.has(matchId)) next.delete(matchId)
      else next.add(matchId)
      localStorage.setItem(`wishi_favourites_${params.id}`, JSON.stringify([...next]))
      return next
    })
    try {
      if (isFav) {
        await api.del(`/wishlist/wishlists/${params.id}/matches/${matchId}/favourite`)
      } else {
        await api.post(`/wishlist/wishlists/${params.id}/matches/${matchId}/favourite`)
      }
    } catch { /* offline */ }
  }

  const removeMatch = async (matchId) => {
    setRemovedIds((prev) => {
      const next = new Set(prev)
      next.add(matchId)
      localStorage.setItem(`wishi_removed_${params.id}`, JSON.stringify([...next]))
      return next
    })
    try {
      await api.post(`/wishlist/wishlists/${params.id}/matches/${matchId}/dismiss`)
    } catch { /* offline */ }
  }

  const sorted = useMemo(() => {
    const filtered = matches.filter((m) => !removedIds.has(m.id) && activeMarketplaces.includes(m.source.name))
    const arr = [...filtered]
    if (sortBy === 'match') arr.sort((a, b) => b.matchScore - a.matchScore)
    else if (sortBy === 'price-low') arr.sort((a, b) => a.price - b.price)
    else if (sortBy === 'price-high') arr.sort((a, b) => b.price - a.price)
    else if (sortBy === 'newest') arr.sort((a, b) => a.id - b.id)
    else if (sortBy === 'favourites') arr.sort((a, b) => (favouriteIds.has(b.id) ? 1 : 0) - (favouriteIds.has(a.id) ? 1 : 0))
    return arr
  }, [matches, sortBy, activeMarketplaces, removedIds])

  if (!isLoggedIn || !wishlist) return null

  const fields = wishlist.fields || {}
  const Icon = categoryIcons[wishlist.category] || Tag
  const gradient = categoryGradients[wishlist.category] || 'from-gray-400 to-gray-600'
  const brandModel = [fields.brand, fields.model].filter(Boolean).join(' ')
  const fieldConfig = getFields(wishlist.category, wishlist.subcategory)
  const priceField = fieldConfig.find((f) => f.type === 'slider' && fields[f.name] !== undefined)

  return (
    <div className="min-h-screen bg-gray-50/50">
      <Header />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-10">
        {/* Back + Wishlist Summary */}
        <div className="mb-8">
          <Link href="/wishlist" className="inline-flex items-center gap-1.5 text-sm text-sky-600 hover:text-sky-700 transition mb-4">
            <ChevronLeft className="w-4 h-4" />
            Back to Wishlists
          </Link>

          <div className="flex flex-col sm:flex-row sm:items-center gap-4 sm:gap-6">
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${gradient} flex items-center justify-center flex-shrink-0 shadow-lg shadow-${wishlist.category === 'Automobile' ? 'blue' : 'gray'}-200/50`}>
              <Icon className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h1 className="text-xl sm:text-2xl font-bold text-slate-900">
                {brandModel || wishlist.subcategory}
              </h1>
              <div className="flex flex-wrap items-center gap-2 mt-1 text-sm text-slate-400">
                <span>{wishlist.category}</span>
                <span className="text-slate-200">→</span>
                <span>{wishlist.subcategory}</span>
                {priceField && (
                  <>
                    <span className="text-slate-200">·</span>
                    <span className="font-medium text-slate-600">Up to {priceField.unit}{Number(fields[priceField.name]).toLocaleString('en-IN')}</span>
                  </>
                )}
                {(fields.location || fields.city) && (
                  <>
                    <span className="text-slate-200">·</span>
                    <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{fields.location || fields.city}</span>
                  </>
                )}
              </div>
            </div>
            <div className="text-sm font-medium text-slate-500">
              {sorted.length} of {matches.length} matches
            </div>
          </div>
        </div>

        {/* Marketplace Filter + Sort Bar */}
        <div className="mb-6 space-y-4">
          {/* Marketplace Filter Chips */}
          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => {
                const sources = MARKETPLACE_SOURCES[wishlist.category] || []
                const allNames = sources.map((s) => s.name)
                setActiveMarketplaces(activeMarketplaces.length === allNames.length ? [] : allNames)
              }}
              className={`rounded-full px-3 py-1.5 text-xs font-medium border transition-all ${
                activeMarketplaces.length === (MARKETPLACE_SOURCES[wishlist.category] || []).length
                  ? 'border-sky-500 bg-sky-50 text-sky-700'
                  : 'border-gray-200 text-slate-500 hover:border-gray-300'
              }`}
            >
              All
            </button>
            {(MARKETPLACE_SOURCES[wishlist.category] || []).map((src) => {
              const active = activeMarketplaces.includes(src.name)
              return (
                <button
                  key={src.name}
                  onClick={() => {
                    setActiveMarketplaces((prev) =>
                      active ? prev.filter((n) => n !== src.name) : [...prev, src.name]
                    )
                  }}
                  className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium border transition-all ${
                    active
                      ? 'border-sky-500 bg-sky-50 text-sky-700'
                      : 'border-gray-200 text-slate-400 hover:border-gray-300'
                  }`}
                >
                  <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: src.color }} />
                  {src.name}
                  {active && <Check className="w-3 h-3" />}
                </button>
              )
            })}
          </div>

          {/* Sort */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ArrowUpDown className="w-4 h-4 text-slate-400" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="text-sm font-medium text-slate-700 bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 appearance-none pr-8 cursor-pointer"
              >
                <option value="match">Best Match</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="newest">Newest First</option>
                <option value="favourites">Favourites First</option>
              </select>
            </div>
            {favouriteIds.size > 0 && (
              <span className="inline-flex items-center gap-1 text-xs text-rose-500">
                <Heart className="w-3 h-3 fill-rose-500" />
                {favouriteIds.size} saved
              </span>
            )}
          </div>
        </div>

        {/* Pinterest Masonry Grid */}
        {sorted.length === 0 ? (
          <div className="py-20 text-center">
            <p className="text-sm text-slate-400">No matches for selected marketplaces</p>
            <button
              onClick={() => {
                const sources = MARKETPLACE_SOURCES[wishlist.category] || []
                setActiveMarketplaces(sources.map((s) => s.name))
              }}
              className="mt-2 text-sm font-medium text-sky-600 hover:text-sky-700 transition"
            >
              Show all marketplaces
            </button>
          </div>
        ) : (
        <motion.div
          className="columns-1 sm:columns-2 lg:columns-3 gap-4 [column-fill:_balance]"
          variants={stagger}
          initial="hidden"
          animate="show"
        >
          {sorted.map((match) => (
            <motion.div
              key={match.id}
              variants={cardAnim}
              className="break-inside-avoid mb-4"
            >
              <div className="group bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl hover:shadow-gray-200/40 hover:-translate-y-0.5 transition-all duration-300">
                {/* Image Placeholder */}
                <div className={`relative h-32 sm:h-36 bg-gradient-to-br ${gradient} flex items-center justify-center`}>
                  <Icon className="w-10 h-10 text-white/30" />

                  {/* Favourite Button */}
                  <button
                    onClick={() => toggleFavourite(match.id)}
                    className="absolute top-3 left-3 w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-sm hover:scale-110 transition-transform z-10"
                    aria-label={favouriteIds.has(match.id) ? 'Remove from favourites' : 'Add to favourites'}
                  >
                    <Heart className={`w-4 h-4 transition-colors ${favouriteIds.has(match.id) ? 'fill-rose-500 text-rose-500' : 'text-slate-400'}`} />
                  </button>

                  {/* Remove Button */}
                  <button
                    onClick={() => removeMatch(match.id)}
                    className="absolute top-3 left-12 w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-sm opacity-0 group-hover:opacity-100 hover:scale-110 transition-all z-10"
                    aria-label="Remove match"
                  >
                    <X className="w-4 h-4 text-slate-400 hover:text-red-500" />
                  </button>

                  {/* Source Badge */}
                  <div className="absolute top-3 right-3 flex items-center gap-1.5 bg-white/95 backdrop-blur-sm rounded-full px-2.5 py-1 shadow-sm">
                    <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: match.source.color }} />
                    <span className="text-[11px] font-semibold text-slate-700">{match.source.name}</span>
                  </div>

                  {/* Featured Badge */}
                  {match.featured && (
                    <div className="absolute bottom-3 right-3 flex items-center gap-1 bg-amber-400 rounded-full px-2 py-0.5 shadow-sm">
                      <Sparkles className="w-3 h-3 text-white" />
                      <span className="text-[10px] font-bold text-white">FEATURED</span>
                    </div>
                  )}

                  {/* Match Score */}
                  <div className={`absolute bottom-3 left-3 flex items-center gap-1 rounded-full px-2.5 py-1 border text-xs font-bold ${scoreColor(match.matchScore)}`}>
                    {match.matchScore}% match
                  </div>
                </div>

                {/* Content */}
                <div className="p-4">
                  <h3 className="text-[15px] font-semibold text-slate-900 leading-snug mb-1.5 line-clamp-2">
                    {match.title}
                  </h3>

                  <p className="text-lg font-bold text-slate-900 mb-2">
                    {match.formattedPrice}
                  </p>

                  {/* Location + Time */}
                  <div className="flex items-center justify-between text-xs text-slate-400 mb-3">
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3 h-3" />{match.location}
                    </span>
                    <span>{match.postedAgo}</span>
                  </div>

                  {/* Specs Tags */}
                  {match.specs.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mb-3">
                      {match.specs.map((spec, i) => (
                        <span key={i} className="rounded-full bg-gray-100 px-2 py-0.5 text-[11px] font-medium text-slate-500">
                          {spec}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Seller Tag */}
                  {match.sellerTag && (
                    <div className="flex items-center gap-1 mb-3 text-xs text-emerald-600">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span className="font-medium">{match.sellerTag}</span>
                    </div>
                  )}

                  {/* Open Button */}
                  <a
                    href={match.source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 w-full rounded-xl py-2.5 text-sm font-semibold transition-all
                      bg-slate-900 text-white hover:bg-slate-800 active:scale-[0.98]"
                  >
                    Open on {match.source.name}
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
        )}
      </div>
      <Footer />
    </div>
  )
}
