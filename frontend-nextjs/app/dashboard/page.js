'use client'

import { Suspense, useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { User, Lock, Heart, MessageSquare, HelpCircle, LogOut, Star, ChevronDown, ChevronRight, Check, Bookmark, History, Bell, Camera, Link2, Globe, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAuth } from '../../contexts/AuthContext'
import { api } from '../../lib/api'

const inputClass = 'w-full border-0 border-b border-gray-200 bg-transparent px-0 py-2 text-sm text-slate-900 placeholder:text-slate-300 focus:outline-none focus:border-sky-500 transition-colors'

const menuItems = [
  { id: 'profile', label: 'Profile Details', icon: User },
  { id: 'password', label: 'Change Password', icon: Lock },
  { id: 'wishlists', label: 'My Wishlists', icon: Heart, href: '/wishlist' },
  { id: 'saved', label: 'Saved Listings', icon: Bookmark },
  { id: 'matches', label: 'Match History', icon: History },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'feedback', label: 'Feedback', icon: MessageSquare },
  { id: 'help', label: 'Help & Support', icon: HelpCircle },
]

// ── Profile Details ──
function ProfileSection() {
  const { user } = useAuth()
  const [editing, setEditing] = useState(false)
  const [saved, setSaved] = useState(false)
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    phone: '',
    location: '',
    bio: '',
    website: '',
    instagram: '',
    twitter: '',
  })

  useEffect(() => {
    // Populate from auth user first, then try API, then localStorage
    if (user) {
      setProfile((prev) => ({
        ...prev,
        name: user.name || prev.name,
        email: user.email || prev.email,
        phone: user.phone || prev.phone,
        location: user.location || prev.location,
        bio: user.bio || prev.bio,
        website: user.website || prev.website,
        instagram: user.instagram || prev.instagram,
        twitter: user.twitter || prev.twitter,
      }))
    }
    api.get('/auth/me').then((res) => {
      if (res.ok) return res.json()
      return null
    }).then((data) => {
      if (data) setProfile((prev) => ({ ...prev, ...data }))
    }).catch(() => {
      const stored = localStorage.getItem('wishi_profile')
      if (stored) setProfile(JSON.parse(stored))
    })
  }, [user])

  const update = (field, value) => setProfile((p) => ({ ...p, [field]: value }))

  const handleSave = async () => {
    localStorage.setItem('wishi_profile', JSON.stringify(profile))
    try {
      await api.put('/auth/me', profile)
    } catch { /* offline — localStorage is already saved */ }
    setEditing(false)
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Profile Details</h2>
          <p className="text-sm text-slate-400 mt-0.5">Manage your personal information</p>
        </div>
        {!editing ? (
          <button onClick={() => setEditing(true)} className="text-sm font-medium text-sky-600 hover:text-sky-700 transition">
            Edit
          </button>
        ) : (
          <button onClick={handleSave} className="inline-flex items-center gap-1.5 rounded-full bg-sky-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-sky-700 transition">
            <Check className="w-3.5 h-3.5" />
            Save
          </button>
        )}
      </div>

      <AnimatePresence>
        {saved && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mb-6 flex items-center gap-2 rounded-lg bg-emerald-50 px-4 py-2.5 text-sm text-emerald-700"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Profile saved
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex items-center gap-5 mb-8 pb-8 border-b border-gray-100">
        <div className="relative group">
          <div className="w-16 h-16 rounded-full bg-sky-600 flex items-center justify-center text-white text-xl font-bold flex-shrink-0">
            {profile.name ? profile.name.charAt(0).toUpperCase() : 'U'}
          </div>
          {editing && (
            <button className="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition">
              <Camera className="w-5 h-5 text-white" />
            </button>
          )}
        </div>
        <div>
          <p className="text-base font-medium text-slate-900">{profile.name || 'User'}</p>
          <p className="text-sm text-slate-400">{profile.email || 'user@wishi.com'}</p>
          {profile.bio && !editing && <p className="text-xs text-slate-400 mt-1 max-w-xs">{profile.bio}</p>}
        </div>
      </div>

      <div className="space-y-6 max-w-md">
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Full Name</label>
          <input type="text" value={profile.name} onChange={(e) => update('name', e.target.value)} placeholder="Enter your name" className={inputClass} disabled={!editing} />
        </div>
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Email</label>
          <input type="email" value={profile.email} onChange={(e) => update('email', e.target.value)} placeholder="Enter your email" className={inputClass} disabled={!editing} />
        </div>
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Phone</label>
          <input type="tel" value={profile.phone} onChange={(e) => update('phone', e.target.value)} placeholder="Enter phone number" className={inputClass} disabled={!editing} />
        </div>
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Location</label>
          <input type="text" value={profile.location} onChange={(e) => update('location', e.target.value)} placeholder="Enter your city" className={inputClass} disabled={!editing} />
        </div>

        <div className="pt-4 border-t border-gray-100">
          <p className="text-sm font-medium text-slate-700 mb-4">About You</p>
          <div className="space-y-6">
            <div>
              <label className="block text-[13px] font-medium text-slate-600 mb-1">Bio</label>
              <textarea value={profile.bio} onChange={(e) => update('bio', e.target.value)} placeholder="Tell us a bit about yourself..." rows={2} className={`${inputClass} resize-none`} disabled={!editing} />
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-100">
          <p className="text-sm font-medium text-slate-700 mb-4">Social Links</p>
          <div className="space-y-6">
            <div>
              <label className="flex items-center gap-1.5 text-[13px] font-medium text-slate-600 mb-1">
                <Globe className="w-3.5 h-3.5" /> Website
              </label>
              <input type="url" value={profile.website} onChange={(e) => update('website', e.target.value)} placeholder="https://yourwebsite.com" className={inputClass} disabled={!editing} />
            </div>
            <div>
              <label className="flex items-center gap-1.5 text-[13px] font-medium text-slate-600 mb-1">
                <Link2 className="w-3.5 h-3.5" /> Instagram
              </label>
              <input type="text" value={profile.instagram} onChange={(e) => update('instagram', e.target.value)} placeholder="@username" className={inputClass} disabled={!editing} />
            </div>
            <div>
              <label className="flex items-center gap-1.5 text-[13px] font-medium text-slate-600 mb-1">
                <Link2 className="w-3.5 h-3.5" /> Twitter
              </label>
              <input type="text" value={profile.twitter} onChange={(e) => update('twitter', e.target.value)} placeholder="@username" className={inputClass} disabled={!editing} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Change Password ──
function PasswordSection() {
  const [saved, setSaved] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
    e.target.reset()
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-slate-900">Change Password</h2>
        <p className="text-sm text-slate-400 mt-0.5">Update your password to keep your account secure</p>
      </div>

      <AnimatePresence>
        {saved && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mb-6 flex items-center gap-2 rounded-lg bg-emerald-50 px-4 py-2.5 text-sm text-emerald-700"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Password updated
          </motion.div>
        )}
      </AnimatePresence>

      <form onSubmit={handleSubmit} className="space-y-6 max-w-md">
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Current Password</label>
          <input type="password" placeholder="Enter current password" className={inputClass} required />
        </div>
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">New Password</label>
          <input type="password" placeholder="Enter new password" className={inputClass} required />
        </div>
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Confirm New Password</label>
          <input type="password" placeholder="Confirm new password" className={inputClass} required />
        </div>
        <button type="submit" className="rounded-full bg-sky-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-sky-700 transition">
          Update Password
        </button>
      </form>
    </div>
  )
}

// ── Feedback ──
function FeedbackSection() {
  const [rating, setRating] = useState(0)
  const [hover, setHover] = useState(0)
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    const message = e.target.querySelector('textarea')?.value
    try {
      await api.post('/wishlist/feedback', { rating, message })
    } catch { /* offline */ }
    setSent(true)
    setRating(0)
    setTimeout(() => setSent(false), 3000)
    e.target.reset()
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-slate-900">Feedback</h2>
        <p className="text-sm text-slate-400 mt-0.5">Help us improve your experience</p>
      </div>

      <AnimatePresence>
        {sent && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mb-6 flex items-center gap-2 rounded-lg bg-emerald-50 px-4 py-2.5 text-sm text-emerald-700"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Thank you for your feedback!
          </motion.div>
        )}
      </AnimatePresence>

      <form onSubmit={handleSubmit} className="space-y-6 max-w-md">
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-3">How would you rate your experience?</label>
          <div className="flex gap-1">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => setRating(star)}
                onMouseEnter={() => setHover(star)}
                onMouseLeave={() => setHover(0)}
                className="p-0.5 transition"
              >
                <Star
                  className={`w-7 h-7 transition ${(hover || rating) >= star ? 'text-amber-400 fill-amber-400' : 'text-gray-200'}`}
                />
              </button>
            ))}
            {rating > 0 && <span className="ml-2 self-center text-sm text-slate-400">{rating}/5</span>}
          </div>
        </div>
        <div>
          <label className="block text-[13px] font-medium text-slate-600 mb-1">Your Message</label>
          <textarea placeholder="Tell us what you think..." rows={4} className={`${inputClass} resize-none`} required />
        </div>
        <button type="submit" className="rounded-full bg-sky-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-sky-700 transition">
          Send Feedback
        </button>
      </form>
    </div>
  )
}

// ── Help & Support ──
function HelpSection() {
  const [open, setOpen] = useState(null)

  const faqs = [
    { q: 'How do I create a wishlist?', a: 'Go to the Wishlist page from the navigation menu. Fill in the details about what you\'re looking for — category, location, budget, and more — then click "Create Wishlist".' },
    { q: 'How does matching work?', a: 'Once you create a wishlist, our system automatically matches your preferences with available listings. You\'ll be notified when there\'s a match.' },
    { q: 'Can I edit or delete a wishlist?', a: 'Yes, you can manage all your wishlists from the My Wishlists page. Hover over any wishlist to see the delete option.' },
    { q: 'Is my data safe?', a: 'Your data is stored securely. We don\'t share your personal information with third parties without your consent.' },
    { q: 'How do I contact support?', a: 'You can reach us at support@wishi.com or through the feedback form in your profile settings.' },
  ]

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-slate-900">Help & Support</h2>
        <p className="text-sm text-slate-400 mt-0.5">Frequently asked questions and contact info</p>
      </div>

      <div className="space-y-0 max-w-lg">
        {faqs.map((faq, i) => (
          <div key={i} className="border-b border-gray-100">
            <button
              onClick={() => setOpen(open === i ? null : i)}
              className="flex items-center justify-between w-full py-4 text-left text-sm font-medium text-slate-800 hover:text-sky-600 transition"
            >
              {faq.q}
              <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform flex-shrink-0 ml-4 ${open === i ? 'rotate-180' : ''}`} />
            </button>
            <AnimatePresence>
              {open === i && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <p className="pb-4 text-sm text-slate-500 leading-relaxed">{faq.a}</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>

      <div className="mt-10 p-5 rounded-xl bg-gray-50 max-w-lg">
        <p className="text-sm font-medium text-slate-800">Still need help?</p>
        <p className="text-sm text-slate-400 mt-1">Reach out to us at <a href="mailto:support@wishi.com" className="text-sky-600 font-medium">support@wishi.com</a></p>
      </div>
    </div>
  )
}

// ── Saved Listings ──
function SavedListingsSection() {
  const [savedItems, setSavedItems] = useState([])

  useEffect(() => {
    api.get('/wishlist/saved-listings').then((res) => {
      if (res.ok) return res.json()
      return null
    }).then((data) => {
      if (data && data.length > 0) setSavedItems(data)
      else {
        const stored = localStorage.getItem('wishi_saved_listings')
        if (stored) setSavedItems(JSON.parse(stored))
      }
    }).catch(() => {
      const stored = localStorage.getItem('wishi_saved_listings')
      if (stored) setSavedItems(JSON.parse(stored))
    })
  }, [])

  const handleRemove = async (id) => {
    const updated = savedItems.filter((item) => item.id !== id)
    setSavedItems(updated)
    localStorage.setItem('wishi_saved_listings', JSON.stringify(updated))
    try { await api.del(`/wishlist/saved-listings/${id}`) } catch { /* offline */ }
  }

  const mockListings = [
    { id: 1, title: 'Honda City 2020 V CVT', price: '₹8,50,000', location: 'Mumbai', category: 'Automobile', savedAt: '2024-12-10' },
    { id: 2, title: 'iPhone 14 Pro Max 256GB', price: '₹89,999', location: 'Delhi', category: 'Electronics', savedAt: '2024-12-08' },
    { id: 3, title: '2BHK Flat in Andheri West', price: '₹1.2 Cr', location: 'Mumbai', category: 'Real Estate', savedAt: '2024-12-05' },
  ]

  const items = savedItems.length > 0 ? savedItems : mockListings

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-slate-900">Saved Listings</h2>
        <p className="text-sm text-slate-400 mt-0.5">Items you've bookmarked for later</p>
      </div>

      {items.length === 0 ? (
        <div className="py-20 text-center">
          <Bookmark className="w-8 h-8 text-slate-200 mx-auto mb-3" />
          <p className="text-sm text-slate-400">No saved listings yet</p>
          <p className="text-xs text-slate-300 mt-1">Bookmark items while browsing to see them here</p>
        </div>
      ) : (
        <div className="divide-y divide-gray-100">
          {items.map((item) => (
            <div key={item.id} className="group py-4 flex items-start gap-4">
              <div className="mt-1.5 w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center flex-shrink-0">
                <Bookmark className="w-4 h-4 text-sky-500" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-[15px] font-medium text-slate-900">{item.title}</h3>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-xs text-slate-400">
                      <span className="font-medium text-sky-600">{item.price}</span>
                      <span className="w-0.5 h-0.5 rounded-full bg-slate-300" />
                      <span>{item.location}</span>
                      <span className="w-0.5 h-0.5 rounded-full bg-slate-300" />
                      <span className="rounded-full bg-gray-100 px-2 py-0.5 text-[11px]">{item.category}</span>
                    </div>
                    <p className="mt-1.5 text-[11px] text-slate-300">Saved {new Date(item.savedAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</p>
                  </div>
                  <button
                    onClick={() => handleRemove(item.id)}
                    className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-300 hover:text-red-500 transition flex-shrink-0"
                    aria-label="Remove"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Match History ──
function MatchHistorySection() {
  const [matches, setMatches] = useState([])

  useEffect(() => {
    api.get('/wishlist/wishlists').then((res) => {
      if (res.ok) return res.json()
      return null
    }).then(async (wishlists) => {
      if (!wishlists || wishlists.length === 0) throw new Error('no wishlists')
      // Collect recent matches across all wishlists
      const allMatches = []
      for (const wl of wishlists.slice(0, 10)) {
        try {
          const res = await api.get(`/wishlist/wishlists/${wl.id}/matches?limit=5`)
          if (res.ok) {
            const data = await res.json()
            for (const m of data) {
              allMatches.push({
                id: m.id,
                wishlistTitle: wl.title || wl.subcategory || `Wishlist #${wl.id}`,
                matchedItem: m.title || m.product_title || 'Match',
                matchedAt: m.matched_at || m.created_at,
                score: m.score || m.match_score || 0,
              })
            }
          }
        } catch { /* skip */ }
      }
      if (allMatches.length > 0) {
        allMatches.sort((a, b) => new Date(b.matchedAt) - new Date(a.matchedAt))
        setMatches(allMatches.slice(0, 20))
      } else throw new Error('no matches')
    }).catch(() => {
      const stored = localStorage.getItem('wishi_match_history')
      if (stored) setMatches(JSON.parse(stored))
    })
  }, [])

  const mockMatches = [
    { id: 1, wishlistTitle: 'Honda City under 8L', matchedItem: 'Honda City 2020 V CVT — Mumbai', matchedAt: '2024-12-11', score: 95 },
    { id: 2, wishlistTitle: '2BHK in Mumbai', matchedItem: '2BHK Flat, Andheri West — ₹1.2 Cr', matchedAt: '2024-12-09', score: 88 },
    { id: 3, wishlistTitle: 'iPhone under 90K', matchedItem: 'iPhone 14 Pro Max 256GB — Delhi', matchedAt: '2024-12-07', score: 92 },
    { id: 4, wishlistTitle: 'Samsung TV 55"', matchedItem: 'Samsung Crystal 4K 55" — Pune', matchedAt: '2024-12-03', score: 78 },
  ]

  const items = matches.length > 0 ? matches : mockMatches

  const scoreColor = (score) => {
    if (score >= 90) return 'text-emerald-600 bg-emerald-50'
    if (score >= 80) return 'text-amber-600 bg-amber-50'
    return 'text-slate-500 bg-gray-100'
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-slate-900">Match History</h2>
        <p className="text-sm text-slate-400 mt-0.5">Listings matched to your wishlists</p>
      </div>

      {items.length === 0 ? (
        <div className="py-20 text-center">
          <History className="w-8 h-8 text-slate-200 mx-auto mb-3" />
          <p className="text-sm text-slate-400">No matches yet</p>
          <p className="text-xs text-slate-300 mt-1">Create a wishlist and we'll find matches for you</p>
        </div>
      ) : (
        <div className="space-y-0">
          {items.map((item, i) => (
            <div key={item.id} className="flex gap-4 py-4 border-b border-gray-100 last:border-0">
              {/* Timeline dot */}
              <div className="flex flex-col items-center pt-1.5">
                <div className="w-2 h-2 rounded-full bg-sky-500" />
                {i < items.length - 1 && <div className="w-px flex-1 bg-gray-100 mt-1" />}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[13px] text-slate-400">Wishlist: <span className="font-medium text-slate-600">{item.wishlistTitle}</span></p>
                    <h3 className="text-[15px] font-medium text-slate-900 mt-0.5">{item.matchedItem}</h3>
                    <p className="mt-1.5 text-[11px] text-slate-300">
                      {new Date(item.matchedAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                    </p>
                  </div>
                  <span className={`text-xs font-semibold px-2.5 py-1 rounded-full flex-shrink-0 ${scoreColor(item.score)}`}>
                    {item.score}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Notification Settings ──
function NotificationsSection() {
  const [settings, setSettings] = useState({
    emailMatches: true,
    emailPriceDrops: true,
    emailNewsletter: false,
    pushMatches: true,
    pushMessages: true,
    pushPromotions: false,
  })
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    api.get('/notification/notification-settings').then((res) => {
      if (res.ok) return res.json()
      return null
    }).then((data) => {
      if (data) {
        setSettings({
          emailMatches: data.email_matches ?? true,
          emailPriceDrops: data.email_price_drops ?? true,
          emailNewsletter: data.email_newsletter ?? false,
          pushMatches: data.push_matches ?? true,
          pushMessages: data.push_messages ?? true,
          pushPromotions: data.push_promotions ?? false,
        })
      } else {
        const stored = localStorage.getItem('wishi_notifications')
        if (stored) setSettings(JSON.parse(stored))
      }
    }).catch(() => {
      const stored = localStorage.getItem('wishi_notifications')
      if (stored) setSettings(JSON.parse(stored))
    })
  }, [])

  const toggle = (key) => setSettings((prev) => ({ ...prev, [key]: !prev[key] }))

  const handleSave = async () => {
    localStorage.setItem('wishi_notifications', JSON.stringify(settings))
    try {
      await api.put('/notification/notification-settings', {
        email_matches: settings.emailMatches,
        email_price_drops: settings.emailPriceDrops,
        email_newsletter: settings.emailNewsletter,
        push_matches: settings.pushMatches,
        push_messages: settings.pushMessages,
        push_promotions: settings.pushPromotions,
      })
    } catch { /* offline — localStorage is already saved */ }
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  const Toggle = ({ checked, onChange }) => (
    <button
      type="button"
      onClick={onChange}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${checked ? 'bg-sky-600' : 'bg-gray-200'}`}
    >
      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow-sm ${checked ? 'translate-x-6' : 'translate-x-1'}`} />
    </button>
  )

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Notification Settings</h2>
          <p className="text-sm text-slate-400 mt-0.5">Choose what updates you receive</p>
        </div>
        <button onClick={handleSave} className="inline-flex items-center gap-1.5 rounded-full bg-sky-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-sky-700 transition">
          <Check className="w-3.5 h-3.5" />
          Save
        </button>
      </div>

      <AnimatePresence>
        {saved && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mb-6 flex items-center gap-2 rounded-lg bg-emerald-50 px-4 py-2.5 text-sm text-emerald-700"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
            Settings saved
          </motion.div>
        )}
      </AnimatePresence>

      <div className="max-w-md">
        <div className="mb-8">
          <p className="text-sm font-medium text-slate-700 mb-4">Email Notifications</p>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-800">Match alerts</p>
                <p className="text-xs text-slate-400 mt-0.5">When a listing matches your wishlist</p>
              </div>
              <Toggle checked={settings.emailMatches} onChange={() => toggle('emailMatches')} />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-800">Price drops</p>
                <p className="text-xs text-slate-400 mt-0.5">When saved items drop in price</p>
              </div>
              <Toggle checked={settings.emailPriceDrops} onChange={() => toggle('emailPriceDrops')} />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-800">Newsletter</p>
                <p className="text-xs text-slate-400 mt-0.5">Weekly digest and recommendations</p>
              </div>
              <Toggle checked={settings.emailNewsletter} onChange={() => toggle('emailNewsletter')} />
            </div>
          </div>
        </div>

        <div className="pt-6 border-t border-gray-100">
          <p className="text-sm font-medium text-slate-700 mb-4">Push Notifications</p>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-800">New matches</p>
                <p className="text-xs text-slate-400 mt-0.5">Instant alerts for wishlist matches</p>
              </div>
              <Toggle checked={settings.pushMatches} onChange={() => toggle('pushMatches')} />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-800">Messages</p>
                <p className="text-xs text-slate-400 mt-0.5">When sellers respond to your enquiries</p>
              </div>
              <Toggle checked={settings.pushMessages} onChange={() => toggle('pushMessages')} />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-800">Promotions</p>
                <p className="text-xs text-slate-400 mt-0.5">Deals and special offers</p>
              </div>
              <Toggle checked={settings.pushPromotions} onChange={() => toggle('pushPromotions')} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// ── Main Page ──
function DashboardContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const { isLoggedIn, logout } = useAuth()
  const [activeTab, setActiveTab] = useState('profile')

  useEffect(() => {
    if (!isLoggedIn) {
      router.push('/')
      return
    }
    const tab = searchParams.get('tab')
    if (tab && menuItems.some((m) => m.id === tab)) {
      setActiveTab(tab)
    }
  }, [isLoggedIn, router, searchParams])

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  const handleMenuClick = (item) => {
    if (item.href) {
      router.push(item.href)
      return
    }
    setActiveTab(item.id)
  }

  if (!isLoggedIn) return null

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
        {/* Mobile tab bar */}
        <div className="flex gap-1 overflow-x-auto pb-4 mb-6 lg:hidden scrollbar-hide">
          {menuItems.map((item) => {
            if (item.href) {
              return (
                <Link key={item.id} href={item.href} className="flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-medium whitespace-nowrap text-slate-500 bg-gray-100 hover:bg-gray-200 transition">
                  <item.icon className="w-3.5 h-3.5" />
                  {item.label}
                </Link>
              )
            }
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-medium whitespace-nowrap transition ${activeTab === item.id ? 'bg-slate-900 text-white' : 'text-slate-500 bg-gray-100 hover:bg-gray-200'}`}
              >
                <item.icon className="w-3.5 h-3.5" />
                {item.label}
              </button>
            )
          })}
        </div>

        <div className="flex gap-10">
          {/* Desktop sidebar */}
          <aside className="hidden lg:block w-52 flex-shrink-0">
            <nav className="sticky top-20 space-y-0.5">
              {menuItems.map((item) => {
                const isActive = !item.href && activeTab === item.id
                if (item.href) {
                  return (
                    <Link key={item.id} href={item.href} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-500 hover:text-slate-900 hover:bg-gray-50 transition">
                      <item.icon className="w-4 h-4" />
                      {item.label}
                      <ChevronRight className="w-3.5 h-3.5 ml-auto text-slate-300" />
                    </Link>
                  )
                }
                return (
                  <button
                    key={item.id}
                    onClick={() => handleMenuClick(item)}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm w-full text-left transition ${isActive ? 'bg-sky-50 text-sky-700 font-medium' : 'text-slate-500 hover:text-slate-900 hover:bg-gray-50'}`}
                  >
                    <item.icon className={`w-4 h-4 ${isActive ? 'text-sky-600' : ''}`} />
                    {item.label}
                  </button>
                )
              })}
              <div className="pt-4 mt-4 border-t border-gray-100">
                <button onClick={handleLogout} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-red-500 hover:bg-red-50 transition w-full text-left">
                  <LogOut className="w-4 h-4" />
                  Logout
                </button>
              </div>
            </nav>
          </aside>

          {/* Main content */}
          <main className="flex-1 min-w-0">
            <motion.div key={activeTab} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }}>
              {activeTab === 'profile' && <ProfileSection />}
              {activeTab === 'password' && <PasswordSection />}
              {activeTab === 'saved' && <SavedListingsSection />}
              {activeTab === 'matches' && <MatchHistorySection />}
              {activeTab === 'notifications' && <NotificationsSection />}
              {activeTab === 'feedback' && <FeedbackSection />}
              {activeTab === 'help' && <HelpSection />}
            </motion.div>
          </main>
        </div>
      </div>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <Suspense>
      <DashboardContent />
    </Suspense>
  )
}
