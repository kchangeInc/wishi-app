'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bell, BellOff, Check, CheckCheck, Heart, Package, Tag, TrendingDown, Trash2, Clock, ExternalLink, Filter } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '../../contexts/AuthContext'
import { api } from '../../lib/api'

const NOTIFICATION_TYPES = {
  match: { icon: Package, bg: 'bg-sky-50', text: 'text-sky-600', border: 'border-sky-100', accent: 'bg-sky-500', label: 'New Match' },
  price_drop: { icon: TrendingDown, bg: 'bg-emerald-50', text: 'text-emerald-600', border: 'border-emerald-100', accent: 'bg-emerald-500', label: 'Price Drop' },
  expiry: { icon: Clock, bg: 'bg-amber-50', text: 'text-amber-600', border: 'border-amber-100', accent: 'bg-amber-500', label: 'Expiring' },
  favourite: { icon: Heart, bg: 'bg-rose-50', text: 'text-rose-600', border: 'border-rose-100', accent: 'bg-rose-500', label: 'Favourite' },
  promo: { icon: Tag, bg: 'bg-violet-50', text: 'text-violet-600', border: 'border-violet-100', accent: 'bg-violet-500', label: 'Promo' },
}

const MOCK_NOTIFICATIONS = [
  {
    id: 'n1',
    type: 'match',
    title: '3 new matches found',
    description: 'Your wishlist "Maruti Swift under ₹5L" has 3 new matches from OLX and Cars24.',
    wishlistId: 'w1',
    time: Date.now() - 15 * 60 * 1000,
    read: false,
  },
  {
    id: 'n2',
    type: 'price_drop',
    title: 'Price dropped on a match',
    description: 'Honda Activa 6G on OLX dropped from ₹65,000 to ₹58,000. Check it before it\'s gone!',
    wishlistId: 'w2',
    time: Date.now() - 2 * 60 * 60 * 1000,
    read: false,
  },
  {
    id: 'n3',
    type: 'expiry',
    title: 'Wishlist expiring in 3 days',
    description: 'Your wishlist "2 BHK Rent in Pune" will expire on April 15. Renew it to keep receiving matches.',
    wishlistId: 'w3',
    time: Date.now() - 5 * 60 * 60 * 1000,
    read: false,
  },
  {
    id: 'n4',
    type: 'match',
    title: '5 new matches found',
    description: 'Your wishlist "iPhone 14 under ₹50K" has 5 new matches from Amazon, Flipkart, and OLX.',
    wishlistId: 'w4',
    time: Date.now() - 12 * 60 * 60 * 1000,
    read: true,
  },
  {
    id: 'n5',
    type: 'favourite',
    title: 'Favourited item price update',
    description: 'Samsung Galaxy S23 you favourited is now available at ₹39,999 — ₹5,000 less than before.',
    wishlistId: 'w4',
    time: Date.now() - 24 * 60 * 60 * 1000,
    read: true,
  },
  {
    id: 'n6',
    type: 'match',
    title: '2 new matches found',
    description: 'Your wishlist "Wooden Sofa Set" has 2 new matches from Pepperfry and OLX.',
    wishlistId: 'w5',
    time: Date.now() - 2 * 24 * 60 * 60 * 1000,
    read: true,
  },
  {
    id: 'n7',
    type: 'promo',
    title: 'WISHI Tip: Try smarter filters',
    description: 'Did you know you can select preferred marketplaces when creating a wishlist? Get more relevant matches!',
    time: Date.now() - 3 * 24 * 60 * 60 * 1000,
    read: true,
  },
  {
    id: 'n8',
    type: 'expiry',
    title: 'Wishlist expired',
    description: 'Your wishlist "Royal Enfield Classic 350" has expired. Create a new one to keep searching.',
    wishlistId: 'w6',
    time: Date.now() - 5 * 24 * 60 * 60 * 1000,
    read: true,
  },
]

function timeAgo(ts) {
  const diff = Date.now() - ts
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'Just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  const days = Math.floor(hrs / 24)
  if (days < 7) return `${days}d ago`
  return new Date(ts).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
}

const cardStagger = { hidden: {}, show: { transition: { staggerChildren: 0.06 } } }
const cardItem = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.3 } } }

export default function NotificationsPage() {
  const router = useRouter()
  const { isLoggedIn } = useAuth()
  const [notifications, setNotifications] = useState([])
  const [filter, setFilter] = useState('all')
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    api.get('/notification/notifications').then((res) => {
      if (res.ok) return res.json()
      return null
    }).then((data) => {
      if (data && data.notifications && data.notifications.length > 0) {
        setNotifications(data.notifications.map((n) => ({
          id: n.id,
          type: n.type || 'match',
          title: n.title,
          description: n.message || n.description || '',
          wishlistId: n.wishlist_id,
          time: new Date(n.created_at).getTime(),
          read: n.is_read,
        })))
      } else {
        const saved = localStorage.getItem('wishi_notifications')
        if (saved) {
          const parsed = JSON.parse(saved)
          if (parsed.length > 0) setNotifications(parsed)
          else setNotifications(MOCK_NOTIFICATIONS)
        } else {
          setNotifications(MOCK_NOTIFICATIONS)
        }
      }
      setLoaded(true)
    }).catch(() => {
      const saved = localStorage.getItem('wishi_notifications')
      if (saved) {
        const parsed = JSON.parse(saved)
        if (parsed.length > 0) setNotifications(parsed)
        else setNotifications(MOCK_NOTIFICATIONS)
      } else {
        setNotifications(MOCK_NOTIFICATIONS)
      }
      setLoaded(true)
    })
  }, [])

  useEffect(() => {
    if (loaded) {
      localStorage.setItem('wishi_notifications', JSON.stringify(notifications))
    }
  }, [notifications, loaded])

  const markAsRead = async (id) => {
    setNotifications((prev) => prev.map((n) => n.id === id ? { ...n, read: true } : n))
    try { await api.put(`/notification/notifications/${id}/read`) } catch { /* offline */ }
  }

  const markAllRead = async () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })))
    try { await api.put('/notification/notifications/read-all') } catch { /* offline */ }
  }

  const deleteNotification = async (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id))
    try { await api.del(`/notification/notifications/${id}`) } catch { /* offline */ }
  }

  const clearAll = async () => {
    try { await api.del('/notification/notifications') } catch { /* offline */ }
    setNotifications(MOCK_NOTIFICATIONS)
  }

  const unreadCount = notifications.filter((n) => !n.read).length

  const filtered = filter === 'all'
    ? notifications
    : filter === 'unread'
    ? notifications.filter((n) => !n.read)
    : notifications.filter((n) => n.type === filter)

  const filterOptions = [
    { key: 'all', label: 'All' },
    { key: 'unread', label: `Unread (${unreadCount})` },
    { key: 'match', label: 'Matches' },
    { key: 'price_drop', label: 'Price Drops' },
    { key: 'expiry', label: 'Expiry' },
  ]

  return (
    <div className="min-h-screen bg-white">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />

        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 pt-12 sm:pt-16 pb-8 sm:pb-10">
          <div className="flex items-center justify-between">
            <div>
              <motion.h1
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900"
              >
                Notifications
              </motion.h1>
              <motion.p
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.1 }}
                className="mt-1 text-sm text-slate-500"
              >
                {unreadCount > 0
                  ? `You have ${unreadCount} unread notification${unreadCount !== 1 ? 's' : ''}`
                  : 'You\'re all caught up!'}
              </motion.p>
            </div>

            {notifications.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="flex items-center gap-2"
              >
                {unreadCount > 0 && (
                  <button
                    onClick={markAllRead}
                    className="flex items-center gap-1.5 text-xs font-medium text-sky-600 hover:text-sky-700 transition px-3 py-2 rounded-lg hover:bg-sky-50"
                  >
                    <CheckCheck className="w-3.5 h-3.5" />
                    Mark all read
                  </button>
                )}
                <button
                  onClick={clearAll}
                  className="flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-red-500 transition px-3 py-2 rounded-lg hover:bg-red-50"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  Clear all
                </button>
              </motion.div>
            )}
          </div>

          {/* Filter Chips */}
          {notifications.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.2 }}
              className="mt-5 flex items-center gap-2 overflow-x-auto pb-1"
            >
              <Filter className="w-3.5 h-3.5 text-slate-300 flex-shrink-0" />
              {filterOptions.map((opt) => (
                <button
                  key={opt.key}
                  onClick={() => setFilter(opt.key)}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition ${
                    filter === opt.key
                      ? 'bg-sky-600 text-white shadow-sm'
                      : 'bg-gray-100 text-slate-500 hover:bg-gray-200'
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </motion.div>
          )}
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">
        {filtered.length > 0 ? (
          <motion.div
            className="grid gap-4"
            variants={cardStagger}
            initial="hidden"
            animate="show"
          >
            <AnimatePresence>
              {filtered.map((notif) => {
                const config = NOTIFICATION_TYPES[notif.type] || NOTIFICATION_TYPES.match
                const Icon = config.icon

                return (
                  <motion.div
                    key={notif.id}
                    variants={cardItem}
                    exit={{ opacity: 0, y: -8, transition: { duration: 0.2 } }}
                    layout
                    className={`group relative border rounded-2xl p-4 transition-all duration-300 ${
                      notif.read
                        ? 'border-gray-100 hover:shadow-lg hover:shadow-gray-100/50 hover:border-gray-200'
                        : 'border-sky-100 bg-sky-50/20 hover:shadow-lg hover:shadow-sky-100/50 hover:border-sky-200'
                    }`}
                  >
                    {/* Accent line */}
                    <div className={`absolute top-0 left-6 right-6 h-px ${config.accent} opacity-40 rounded-full`} />

                    {/* Header: Icon + Title + Delete */}
                    <div className="flex items-start gap-3 mb-3">
                      <div className={`w-10 h-10 rounded-xl ${config.bg} flex items-center justify-center flex-shrink-0`}>
                        <Icon className={`w-4.5 h-4.5 ${config.text}`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className={`text-[15px] font-semibold truncate ${notif.read ? 'text-slate-700' : 'text-slate-900'}`}>
                          {notif.title}
                        </h3>
                        <div className="flex items-center gap-2 mt-0.5">
                          <span className={`text-[11px] font-medium ${config.text}`}>{config.label}</span>
                          <span className="text-[11px] text-slate-300"> &middot; </span>
                          <span className="flex items-center gap-1 text-[11px] text-slate-300">
                            <Clock className="w-3 h-3" />
                            {timeAgo(notif.time)}
                          </span>
                          {!notif.read && (
                            <span className="w-2 h-2 rounded-full bg-sky-500 animate-pulse" />
                          )}
                        </div>
                      </div>
                      <button
                        onClick={() => deleteNotification(notif.id)}
                        className="p-1.5 rounded-lg text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all flex-shrink-0"
                        aria-label="Delete"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>

                    {/* Description */}
                    <p className={`text-xs leading-relaxed line-clamp-2 mb-3 ${notif.read ? 'text-slate-400' : 'text-slate-500'}`}>
                      {notif.description}
                    </p>

                    {/* Footer */}
                    <div className="flex items-center justify-between pt-3 border-t border-gray-50">
                      <div className="flex items-center gap-2">
                        {!notif.read && (
                          <button
                            onClick={() => markAsRead(notif.id)}
                            className="inline-flex items-center gap-1 text-[11px] font-medium text-slate-400 hover:text-slate-600 transition"
                          >
                            <Check className="w-3 h-3" />
                            Mark read
                          </button>
                        )}
                      </div>
                      {notif.wishlistId ? (
                        <Link
                          href={`/wishlist/${notif.wishlistId}`}
                          onClick={() => markAsRead(notif.id)}
                          className="inline-flex items-center gap-1 text-[11px] font-semibold text-sky-600 hover:text-sky-700 transition"
                        >
                          View Matches
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      ) : (
                        <span className="text-[11px] text-slate-300">
                          {new Date(notif.time).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
                        </span>
                      )}
                    </div>
                  </motion.div>
                )
              })}
            </AnimatePresence>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="text-center py-16"
          >
            <div className="w-20 h-20 rounded-2xl bg-gray-50 flex items-center justify-center mx-auto mb-5">
              <BellOff className="w-9 h-9 text-slate-200" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">
              {notifications.length === 0 ? 'No notifications yet' : 'No matching notifications'}
            </h3>
            <p className="text-sm text-slate-400 max-w-md mx-auto mb-6">
              {notifications.length === 0
                ? 'Create a wishlist to start receiving match alerts, price drops, and expiry reminders.'
                : 'Try a different filter to see your notifications.'}
            </p>
            {notifications.length === 0 && (
              <button
                onClick={() => router.push('/wishlist')}
                className="rounded-full bg-sky-600 hover:bg-sky-700 text-white px-6 py-3 text-sm font-semibold transition-all shadow-lg shadow-sky-600/25"
              >
                Create a Wishlist
              </button>
            )}
          </motion.div>
        )}
      </section>

    </div>
  )
}
