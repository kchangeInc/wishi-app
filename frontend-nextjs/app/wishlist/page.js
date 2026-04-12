'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Trash2, MapPin, Tag, Plus, ChevronRight, Car, Smartphone, Home, Shirt, Sofa, Clock, ArrowRight, Zap, CalendarClock } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from '../../components/Header'
import Footer from '../../components/Footer'
import { useAuth } from '../../contexts/AuthContext'
import WishlistForm from '../../features/wishlist/WishlistForm'
import { getFields } from '../../features/wishlist/wishlistFieldConfig'
import { getMatchCount } from '../../features/wishlist/mockMatches'

const categoryIcons = { Automobile: Car, Electronics: Smartphone, 'Real Estate': Home, Fashion: Shirt, 'Home & Living': Sofa }
const categoryColors = {
  Automobile: { bg: 'bg-blue-50', text: 'text-blue-600', border: 'border-blue-100', accent: 'bg-blue-500' },
  Electronics: { bg: 'bg-violet-50', text: 'text-violet-600', border: 'border-violet-100', accent: 'bg-violet-500' },
  'Real Estate': { bg: 'bg-emerald-50', text: 'text-emerald-600', border: 'border-emerald-100', accent: 'bg-emerald-500' },
  Fashion: { bg: 'bg-pink-50', text: 'text-pink-600', border: 'border-pink-100', accent: 'bg-pink-500' },
  'Home & Living': { bg: 'bg-amber-50', text: 'text-amber-600', border: 'border-amber-100', accent: 'bg-amber-500' },
}

const cardStagger = { hidden: {}, show: { transition: { staggerChildren: 0.06 } } }
const cardItem = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.3 } } }

function ExpiryBadge({ expiresAt }) {
  if (!expiresAt) return null
  const now = new Date()
  const expiry = new Date(expiresAt)
  const diffMs = expiry - now
  const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24))

  if (diffDays <= 0) {
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-red-500">
        <CalendarClock className="w-3 h-3" />
        Expired
      </span>
    )
  }
  if (diffDays <= 7) {
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-amber-500">
        <CalendarClock className="w-3 h-3" />
        {diffDays}d left
      </span>
    )
  }
  return (
    <span className="inline-flex items-center gap-1 text-[11px] text-slate-300">
      <CalendarClock className="w-3 h-3" />
      {expiry.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
    </span>
  )
}

export default function WishlistPage() {
  const router = useRouter()
  const { isLoggedIn } = useAuth()
  const [wishlists, setWishlists] = useState([])
  const [success, setSuccess] = useState(false)
  const [tab, setTab] = useState('create')

  useEffect(() => {
    if (!isLoggedIn) {
      router.push('/')
      return
    }
    const stored = localStorage.getItem('wishi_wishlists')
    if (stored) setWishlists(JSON.parse(stored))
  }, [isLoggedIn, router])

  const handleCreate = (data) => {
    const now = new Date()
    const expires = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000)
    const newItem = { ...data, id: Date.now(), createdAt: now.toISOString(), expiresAt: expires.toISOString() }
    const updated = [newItem, ...wishlists]
    setWishlists(updated)
    localStorage.setItem('wishi_wishlists', JSON.stringify(updated))
    setSuccess(true)
    setTab('list')
    setTimeout(() => setSuccess(false), 3000)
  }

  const handleDelete = (id) => {
    const updated = wishlists.filter((w) => w.id !== id)
    setWishlists(updated)
    localStorage.setItem('wishi_wishlists', JSON.stringify(updated))
  }

  if (!isLoggedIn) return null

  return (
    <div className="min-h-screen bg-white">
      <Header />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
        {/* Tabs */}
        <div className="flex gap-1 p-1 rounded-full bg-gray-100 w-fit mb-10">
          <button
            onClick={() => setTab('create')}
            className={`px-5 py-2 rounded-full text-sm font-medium transition ${tab === 'create' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
          >
            Create
          </button>
          <button
            onClick={() => setTab('list')}
            className={`px-5 py-2 rounded-full text-sm font-medium transition ${tab === 'list' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
          >
            My List{wishlists.length > 0 && ` (${wishlists.length})`}
          </button>
        </div>

        {/* Success toast */}
        <AnimatePresence>
          {success && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="mb-6 flex items-center gap-2 rounded-lg bg-emerald-50 px-4 py-3 text-sm text-emerald-700"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Wishlist created
            </motion.div>
          )}
        </AnimatePresence>

        {/* Create tab */}
        {tab === 'create' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
            <div className="mb-8">
              <h1 className="text-2xl font-semibold text-slate-900">New Wishlist</h1>
              <p className="mt-1 text-sm text-slate-400">Describe what you're looking for</p>
            </div>
            <WishlistForm onSubmit={handleCreate} />
          </motion.div>
        )}

        {/* List tab */}
        {tab === 'list' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-2xl font-semibold text-slate-900">My Wishlists</h1>
                <p className="mt-1 text-sm text-slate-400">{wishlists.length} {wishlists.length === 1 ? 'item' : 'items'}</p>
              </div>
              <button
                onClick={() => setTab('create')}
                className="inline-flex items-center gap-1.5 rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 transition"
              >
                <Plus className="w-3.5 h-3.5" />
                New
              </button>
            </div>

            {wishlists.length === 0 ? (
              <div className="py-24 sm:py-32 text-center">
                <h2 className="text-3xl sm:text-4xl font-bold text-slate-900">Stop Searching</h2>
                <h2 className="text-3xl sm:text-4xl font-extrabold italic bg-gradient-to-r from-sky-500 to-violet-500 bg-clip-text text-transparent mt-1">Start WISHING</h2>
                <p className="mt-4 text-sm sm:text-base text-slate-400 max-w-xs mx-auto">Create your first wishlist. We'll search everything for you.</p>
                <button
                  onClick={() => setTab('create')}
                  className="mt-8 rounded-full bg-gradient-to-r from-sky-500 to-violet-500 hover:from-sky-600 hover:to-violet-600 text-white px-10 py-3.5 text-sm font-semibold shadow-lg shadow-violet-500/25 transition-all active:scale-[0.98]"
                >
                  New Wishlist
                </button>
              </div>
            ) : (
              <motion.div className="grid gap-4 sm:grid-cols-2" variants={cardStagger} initial="hidden" animate="show">
                {wishlists.map((item) => {
                  const isLegacy = !item.subcategory
                  const colors = categoryColors[item.category] || categoryColors.Automobile
                  const Icon = categoryIcons[item.category] || Tag

                  if (isLegacy) {
                    return (
                      <motion.div
                        key={item.id}
                        variants={cardItem}
                        layout
                        className="group relative border border-gray-100 rounded-2xl p-4 hover:shadow-lg hover:shadow-gray-100/50 hover:border-gray-200 transition-all duration-300"
                      >
                        <div className={`absolute top-0 left-6 right-6 h-px ${colors.accent} opacity-40 rounded-full`} />
                        <div className="flex items-start gap-3 mb-3">
                          <div className={`w-10 h-10 rounded-xl ${colors.bg} flex items-center justify-center flex-shrink-0`}>
                            <Icon className={`w-4.5 h-4.5 ${colors.text}`} />
                          </div>
                          <div className="flex-1 min-w-0">
                            <h3 className="text-[15px] font-semibold text-slate-900 truncate">{item.title}</h3>
                            <span className={`inline-block text-[11px] font-medium ${colors.text} mt-0.5`}>{item.category}</span>
                          </div>
                          <button
                            onClick={() => handleDelete(item.id)}
                            className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all flex-shrink-0"
                            aria-label="Delete"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                        {item.location && (
                          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-2">
                            <MapPin className="w-3 h-3" />{item.location}
                          </div>
                        )}
                        {item.description && <p className="text-xs text-slate-400 line-clamp-2 mb-3">{item.description}</p>}
                        <div className="flex items-center justify-between pt-3 border-t border-gray-50">
                          <div className="flex items-center gap-3">
                            <div className="flex items-center gap-1.5 text-[11px] text-slate-300">
                              <Clock className="w-3 h-3" />
                              {new Date(item.createdAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                            </div>
                            <ExpiryBadge expiresAt={item.expiresAt} />
                          </div>
                          <Link
                            href={`/wishlist/${item.id}`}
                            className="inline-flex items-center gap-1 text-[11px] font-semibold text-sky-600 hover:text-sky-700 transition"
                          >
                            <Zap className="w-3 h-3" />
                            {getMatchCount(item)} matches
                            <ChevronRight className="w-3 h-3" />
                          </Link>
                        </div>
                      </motion.div>
                    )
                  }

                  const fieldConfig = getFields(item.category, item.subcategory)
                  const fields = item.fields || {}
                  const priceField = fieldConfig.find((f) => f.type === 'slider' && fields[f.name] !== undefined)
                  const locationField = fieldConfig.find((f) => (f.name === 'city' || f.name === 'location') && fields[f.name])
                  const selectFields = fieldConfig.filter((f) => f.type === 'select' && fields[f.name] && f.name !== 'brand' && f.name !== 'model')
                  const brandModel = [fields.brand, fields.model].filter(Boolean).join(' ')
                  const toggleFields = fieldConfig.filter((f) => f.type === 'toggle' && fields[f.name])

                  return (
                    <motion.div
                      key={item.id}
                      variants={cardItem}
                      layout
                      className="group relative border border-gray-100 rounded-2xl p-4 hover:shadow-lg hover:shadow-gray-100/50 hover:border-gray-200 transition-all duration-300"
                    >
                      <div className={`absolute top-0 left-6 right-6 h-px ${colors.accent} opacity-40 rounded-full`} />

                      {/* Header */}
                      <div className="flex items-start gap-3 mb-3">
                        <div className={`w-10 h-10 rounded-xl ${colors.bg} flex items-center justify-center flex-shrink-0`}>
                          <Icon className={`w-4.5 h-4.5 ${colors.text}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="text-[15px] font-semibold text-slate-900 truncate">
                            {brandModel || item.subcategory}
                          </h3>
                          <div className="flex items-center gap-1.5 mt-0.5">
                            <span className={`text-[11px] font-medium ${colors.text}`}>{item.category}</span>
                            <ArrowRight className="w-2.5 h-2.5 text-slate-300" />
                            <span className="text-[11px] text-slate-400">{item.subcategory}</span>
                          </div>
                        </div>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all flex-shrink-0"
                          aria-label="Delete"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>

                      {/* Price + Location row */}
                      <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 mb-3">
                        {priceField && (
                          <span className="text-sm font-semibold text-slate-900">
                            {priceField.unit}{Number(fields[priceField.name]).toLocaleString('en-IN')}
                            <span className="text-[11px] font-normal text-slate-400 ml-1">max</span>
                          </span>
                        )}
                        {locationField && (
                          <span className="flex items-center gap-1 text-xs text-slate-400">
                            <MapPin className="w-3 h-3" />{fields[locationField.name]}
                          </span>
                        )}
                      </div>

                      {/* Tags */}
                      <div className="flex flex-wrap gap-1.5 mb-3">
                        {selectFields.slice(0, 4).map((f) => (
                          <span key={f.name} className={`rounded-full px-2.5 py-0.5 text-[11px] font-medium ${colors.bg} ${colors.text}`}>
                            {fields[f.name]}
                          </span>
                        ))}
                        {toggleFields.map((f) => (
                          <span key={f.name} className="rounded-full px-2.5 py-0.5 text-[11px] font-medium bg-gray-100 text-slate-500">
                            {f.label}
                          </span>
                        ))}
                      </div>

                      {/* Notes */}
                      {fields.notes && <p className="text-xs text-slate-400 line-clamp-2 mb-3">{fields.notes}</p>}

                      {/* Footer */}
                      <div className="flex items-center justify-between pt-3 border-t border-gray-50">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center gap-1.5 text-[11px] text-slate-300">
                            <Clock className="w-3 h-3" />
                            {new Date(item.createdAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                          </div>
                          <ExpiryBadge expiresAt={item.expiresAt} />
                        </div>
                        <Link
                          href={`/wishlist/${item.id}`}
                          className="inline-flex items-center gap-1 text-[11px] font-semibold text-sky-600 hover:text-sky-700 transition"
                        >
                          <Zap className="w-3 h-3" />
                          {getMatchCount(item)} matches
                          <ChevronRight className="w-3 h-3" />
                        </Link>
                      </div>
                    </motion.div>
                  )
                })}
              </motion.div>
            )}
          </motion.div>
        )}
      </div>
      <Footer />
    </div>
  )
}
