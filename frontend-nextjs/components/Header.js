'use client'

import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Search, ShoppingCart, Menu, X, Heart, User, LogOut, Settings, MessageSquare, ChevronDown, ChevronRight, MapPin, Bell, Bot } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useGoogleReady } from './Providers'
import { INDIAN_CITIES, CATEGORIES } from '../features/wishlist/wishlistFieldConfig'

// Build search suggestions from categories, subcategories, and brands
const SEARCH_SUGGESTIONS = (() => {
  const items = []
  for (const [cat, data] of Object.entries(CATEGORIES)) {
    items.push({ label: cat, type: 'category' })
    for (const [sub, fields] of Object.entries(data.subcategories)) {
      items.push({ label: sub, type: 'subcategory', category: cat })
      const brandField = fields.find((f) => f.name === 'brand')
      if (brandField?.options) {
        brandField.options.forEach((b) => items.push({ label: b, type: 'brand', category: cat, subcategory: sub }))
      }
      const itemTypeField = fields.find((f) => f.name === 'itemType')
      if (itemTypeField?.options) {
        itemTypeField.options.forEach((t) => items.push({ label: t, type: 'item', category: cat, subcategory: sub }))
      }
    }
  }
  // Deduplicate by label (keep first)
  const seen = new Set()
  return items.filter((i) => {
    const key = i.label.toLowerCase()
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
})()

export default function Header() {
  const router = useRouter()
  const { isLoggedIn, user, login, loginEmail, loginDemo, logout } = useAuth()
  const googleReady = useGoogleReady()
  const [menuOpen, setMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState('register')
  const [showProfileMenu, setShowProfileMenu] = useState(false)
  const [location, setLocation] = useState('All India')
  const [locationQuery, setLocationQuery] = useState('')
  const [showLocationDropdown, setShowLocationDropdown] = useState(false)
  const [showSearchSuggestions, setShowSearchSuggestions] = useState(false)
  const [loginEmailValue, setLoginEmailValue] = useState('')
  const [loginPassword, setLoginPassword] = useState('')
  const [loginError, setLoginError] = useState('')
  const [loginLoading, setLoginLoading] = useState(false)
  const profileRef = useRef(null)
  const locationRef = useRef(null)
  const searchRef = useRef(null)

  useEffect(() => {
    const handleClick = (e) => {
      if (profileRef.current && !profileRef.current.contains(e.target)) setShowProfileMenu(false)
      if (locationRef.current && !locationRef.current.contains(e.target)) setShowLocationDropdown(false)
      if (searchRef.current && !searchRef.current.contains(e.target)) setShowSearchSuggestions(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  useEffect(() => {
    const saved = localStorage.getItem('wishi_location')
    if (saved) setLocation(saved)
  }, [])

  const filteredCities = locationQuery
    ? INDIAN_CITIES.filter((c) => c.toLowerCase().includes(locationQuery.toLowerCase())).slice(0, 8)
    : INDIAN_CITIES.slice(0, 8)

  const filteredSuggestions = searchQuery.trim().length >= 2
    ? SEARCH_SUGGESTIONS.filter((s) => s.label.toLowerCase().includes(searchQuery.toLowerCase())).slice(0, 8)
    : []

  const typeLabels = { category: 'Category', subcategory: 'Subcategory', brand: 'Brand', item: 'Item' }
  const typeColors = { category: 'text-sky-600 bg-sky-50', subcategory: 'text-violet-600 bg-violet-50', brand: 'text-emerald-600 bg-emerald-50', item: 'text-amber-600 bg-amber-50' }

  const selectCity = (city) => {
    setLocation(city)
    setLocationQuery('')
    setShowLocationDropdown(false)
    localStorage.setItem('wishi_location', city)
  }

  const handleSearchSubmit = (e) => {
    e.preventDefault()
    setShowSearchSuggestions(false)
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}&location=${encodeURIComponent(location)}`)
    }
  }

  const selectSuggestion = (suggestion) => {
    setSearchQuery(suggestion.label)
    setShowSearchSuggestions(false)
    router.push(`/search?q=${encodeURIComponent(suggestion.label)}&location=${encodeURIComponent(location)}`)
  }

  const openAuth = (mode) => {
    setAuthMode(mode)
    setShowAuthModal(true)
    setMenuOpen(false)
    setLoginEmailValue('')
    setLoginPassword('')
    setLoginError('')
  }

  const handleLogin = () => {
    if (googleReady) {
      try {
        // Use Google Identity Services directly (loaded by GoogleOAuthProvider)
        const client = window.google.accounts.oauth2.initTokenClient({
          client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
          scope: 'email profile',
          callback: async (response) => {
            if (response.access_token) {
              try {
                await login(response.access_token)
                setShowAuthModal(false)
              } catch {
                loginDemo()
                setShowAuthModal(false)
              }
            }
          },
        })
        client.requestAccessToken()
        return
      } catch {
        // Google sign-in failed, fall through to demo
      }
    }
    loginDemo()
    setShowAuthModal(false)
  }

  const handleEmailLogin = async (e) => {
    e.preventDefault()
    setLoginError('')
    setLoginLoading(true)
    try {
      await loginEmail(loginEmailValue, loginPassword)
      setShowAuthModal(false)
      setLoginEmailValue('')
      setLoginPassword('')
    } catch (err) {
      setLoginError(err.message || 'Invalid email or password')
    } finally {
      setLoginLoading(false)
    }
  }

  const handleLogout = async () => {
    await logout()
    setShowProfileMenu(false)
    setMenuOpen(false)
    router.push('/')
  }

  return (
    <>
      <header className="sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6">
          <div className="flex items-center h-14 sm:h-16 gap-2 sm:gap-3">

            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 flex-shrink-0">
              <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-sky-600 flex items-center justify-center text-white shadow-sm">
                <ShoppingCart className="w-4 h-4 sm:w-5 sm:h-5" />
              </div>
              <span className="hidden sm:block text-lg font-bold tracking-tight text-sky-600">WISHI</span>
            </Link>

            {/* Location Selector */}
            <div className="relative hidden md:block" ref={locationRef}>
              <button
                onClick={() => setShowLocationDropdown(!showLocationDropdown)}
                className="flex items-center gap-1.5 rounded-full border border-gray-200 px-3 py-2 hover:border-sky-300 transition text-sm"
              >
                <MapPin className="w-3.5 h-3.5 text-sky-600" />
                <span className="text-slate-700 font-medium max-w-[120px] truncate">{location}</span>
                <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform ${showLocationDropdown ? 'rotate-180' : ''}`} />
              </button>

              {showLocationDropdown && (
                <div className="absolute top-full left-0 mt-2 w-64 bg-white rounded-xl border border-gray-200 shadow-lg z-50 overflow-hidden">
                  <div className="p-2">
                    <div className="relative">
                      <MapPin className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-300" />
                      <input
                        type="text"
                        value={locationQuery}
                        onChange={(e) => setLocationQuery(e.target.value)}
                        placeholder="Search city..."
                        className="w-full pl-8 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500"
                        autoFocus
                      />
                    </div>
                  </div>
                  <div className="max-h-48 overflow-y-auto">
                    <button
                      onClick={() => selectCity('All India')}
                      className={`w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 hover:bg-gray-50 transition ${location === 'All India' ? 'text-sky-600 font-medium' : 'text-slate-700'}`}
                    >
                      <MapPin className="w-3 h-3 text-slate-300" />
                      All India
                    </button>
                    {filteredCities.map((city) => (
                      <button
                        key={city}
                        onClick={() => selectCity(city)}
                        className={`w-full text-left px-4 py-2.5 text-sm flex items-center gap-2 hover:bg-gray-50 transition ${location === city ? 'text-sky-600 font-medium' : 'text-slate-700'}`}
                      >
                        <MapPin className="w-3 h-3 text-slate-300" />
                        {city}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Search Bar */}
            <form onSubmit={handleSearchSubmit} className="flex-1 min-w-0 hidden sm:block relative" ref={searchRef}>
              <div className="flex items-center border border-gray-200 rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-sky-500/20 focus-within:border-sky-500 transition">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => { setSearchQuery(e.target.value); setShowSearchSuggestions(true) }}
                  onFocus={() => setShowSearchSuggestions(true)}
                  placeholder="Search for products, categories..."
                  className="flex-1 min-w-0 px-4 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
                  autoComplete="off"
                />
                <button
                  type="submit"
                  className="w-10 h-10 flex items-center justify-center bg-sky-600 hover:bg-sky-700 transition flex-shrink-0"
                >
                  <Search className="w-4 h-4 text-white" />
                </button>
              </div>

              {/* Search Suggestions Dropdown */}
              {showSearchSuggestions && filteredSuggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-xl border border-gray-200 shadow-lg z-50 overflow-hidden">
                  <div className="max-h-72 overflow-y-auto py-1">
                    {filteredSuggestions.map((s, i) => (
                      <button
                        key={`${s.label}-${i}`}
                        type="button"
                        onClick={() => selectSuggestion(s)}
                        className="flex items-center gap-3 w-full px-4 py-2.5 text-left hover:bg-gray-50 transition"
                      >
                        <Search className="w-3.5 h-3.5 text-slate-300 flex-shrink-0" />
                        <span className="flex-1 text-sm text-slate-700">{s.label}</span>
                        <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${typeColors[s.type]}`}>
                          {typeLabels[s.type]}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </form>

            {/* Right Actions */}
            <div className="hidden md:flex items-center gap-1">
              {isLoggedIn ? (
                <>
                  <Link href="/wishlist" className="flex flex-col items-center justify-center w-12 h-12 rounded-lg text-slate-500 hover:text-sky-600 hover:bg-sky-50 transition">
                    <Heart className="w-5 h-5" />
                    <span className="text-[10px] font-medium mt-0.5">Wishlist</span>
                  </Link>
                  <Link href="/chat" className="flex flex-col items-center justify-center w-12 h-12 rounded-lg text-slate-500 hover:text-sky-600 hover:bg-sky-50 transition">
                    <Bot className="w-5 h-5" />
                    <span className="text-[10px] font-medium mt-0.5">AI Chat</span>
                  </Link>
                  <Link href="/notifications" className="relative flex flex-col items-center justify-center w-12 h-12 rounded-lg text-slate-500 hover:text-sky-600 hover:bg-sky-50 transition">
                    <Bell className="w-5 h-5" />
                    <span className="text-[10px] font-medium mt-0.5">Alerts</span>
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500" />
                  </Link>

                  {/* Profile */}
                  <div className="relative ml-1" ref={profileRef}>
                    <button
                      onClick={() => setShowProfileMenu(!showProfileMenu)}
                      className="flex items-center gap-1.5 rounded-full border-2 border-sky-500 pl-0.5 pr-2.5 py-0.5 hover:shadow-md transition"
                    >
                      <div className="w-8 h-8 rounded-full bg-sky-600 flex items-center justify-center text-white text-xs font-bold">
                        {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                      </div>
                      <ChevronDown className={`w-3 h-3 text-slate-400 transition-transform ${showProfileMenu ? 'rotate-180' : ''}`} />
                    </button>

                    {showProfileMenu && (
                      <div className="absolute right-0 mt-2 w-52 rounded-xl bg-white border border-gray-200 shadow-lg py-1.5 z-50">
                        <div className="px-4 py-2.5 border-b border-gray-100">
                          <p className="text-sm font-semibold text-slate-900">{user?.display_name || user?.name || 'User'}</p>
                          <p className="text-xs text-slate-400">{user?.email || ''}</p>
                        </div>
                        <div className="py-1">
                          <Link href="/dashboard" onClick={() => setShowProfileMenu(false)} className="flex items-center gap-3 px-4 py-2 text-sm text-slate-700 hover:bg-gray-50 transition">
                            <User className="w-4 h-4 text-slate-400" />
                            My Profile
                          </Link>
                          <Link href="/wishlist" onClick={() => setShowProfileMenu(false)} className="flex items-center gap-3 px-4 py-2 text-sm text-slate-700 hover:bg-gray-50 transition">
                            <Heart className="w-4 h-4 text-slate-400" />
                            My Wishlists
                          </Link>
                          <Link href="/dashboard?tab=feedback" onClick={() => setShowProfileMenu(false)} className="flex items-center gap-3 px-4 py-2 text-sm text-slate-700 hover:bg-gray-50 transition">
                            <MessageSquare className="w-4 h-4 text-slate-400" />
                            Feedback
                          </Link>
                          <Link href="/dashboard?tab=settings" onClick={() => setShowProfileMenu(false)} className="flex items-center gap-3 px-4 py-2 text-sm text-slate-700 hover:bg-gray-50 transition">
                            <Settings className="w-4 h-4 text-slate-400" />
                            Settings
                          </Link>
                        </div>
                        <div className="border-t border-gray-100 pt-1">
                          <button onClick={handleLogout} className="flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition w-full text-left">
                            <LogOut className="w-4 h-4" />
                            Logout
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <>
                  <Link href="/about" className="text-sm font-medium text-slate-600 hover:text-sky-600 transition px-3 py-2">About</Link>
                  <Link href="/how-it-works" className="text-sm font-medium text-slate-600 hover:text-sky-600 transition px-3 py-2">How It Works</Link>
                  {/* <Link href="/help" className="text-sm font-medium text-slate-600 hover:text-sky-600 transition px-3 py-2">Help</Link> */}
                  <button onClick={() => openAuth('login')} className="rounded-full bg-sky-600 hover:bg-sky-700 px-5 py-2 text-sm font-semibold text-white transition ml-1">Login</button>
                  {/* <button onClick={() => openAuth('register')} className="rounded-full bg-sky-600 hover:bg-sky-700 px-5 py-2 text-sm font-semibold text-white transition ml-1">
                    Signup
                  </button> */}
                </>
              )}
            </div>

            {/* Mobile: search icon + menu */}
            <div className="flex items-center gap-1 md:hidden">
              <button
                onClick={() => { setMenuOpen(false); router.push('/search') }}
                className="sm:hidden p-2 rounded-lg text-slate-600"
              >
                <Search className="w-5 h-5" />
              </button>
              {isLoggedIn && (
                <Link href="/wishlist" className="p-2 rounded-lg text-slate-600 hover:text-sky-600">
                  <Heart className="w-5 h-5" />
                </Link>
              )}
              <button className="p-2 rounded-lg border border-gray-200" onClick={() => setMenuOpen(!menuOpen)}>
                {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          {menuOpen && (
            <div className="border-t border-gray-200 py-4 md:hidden space-y-1">
              {/* Mobile Search */}
              <div className="mb-3 sm:hidden relative">
                <form onSubmit={handleSearchSubmit}>
                  <div className="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                    <input
                      type="text"
                      value={searchQuery}
                      onChange={(e) => { setSearchQuery(e.target.value); setShowSearchSuggestions(true) }}
                      onFocus={() => setShowSearchSuggestions(true)}
                      placeholder="Search..."
                      className="flex-1 px-3 py-2.5 text-sm focus:outline-none"
                      autoComplete="off"
                    />
                    <button type="submit" className="w-10 h-10 flex items-center justify-center bg-sky-600">
                      <Search className="w-4 h-4 text-white" />
                    </button>
                  </div>
                </form>

                {/* Mobile Search Suggestions */}
                {showSearchSuggestions && filteredSuggestions.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-xl border border-gray-200 shadow-lg z-50 overflow-hidden">
                    <div className="max-h-56 overflow-y-auto py-1">
                      {filteredSuggestions.map((s, i) => (
                        <button
                          key={`m-${s.label}-${i}`}
                          type="button"
                          onClick={() => { selectSuggestion(s); setMenuOpen(false) }}
                          className="flex items-center gap-3 w-full px-4 py-2.5 text-left hover:bg-gray-50 transition"
                        >
                          <Search className="w-3.5 h-3.5 text-slate-300 flex-shrink-0" />
                          <span className="flex-1 text-sm text-slate-700">{s.label}</span>
                          <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${typeColors[s.type]}`}>
                            {typeLabels[s.type]}
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Mobile Location */}
              <button
                onClick={() => setShowLocationDropdown(!showLocationDropdown)}
                className="flex items-center gap-2 w-full px-3 py-2.5 rounded-lg text-sm text-slate-700 hover:bg-gray-50"
              >
                <MapPin className="w-4 h-4 text-sky-600" />
                <span className="font-medium">{location}</span>
                <ChevronRight className="w-3.5 h-3.5 text-slate-400 ml-auto" />
              </button>

              <Link href="/about" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-700 hover:bg-gray-50" onClick={() => setMenuOpen(false)}>About</Link>
              <Link href="/how-it-works" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-700 hover:bg-gray-50" onClick={() => setMenuOpen(false)}>How It Works</Link>
              <Link href="/help" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-700 hover:bg-gray-50" onClick={() => setMenuOpen(false)}>Help & Support</Link>

              {isLoggedIn ? (
                <>
                  <Link href="/wishlist" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-semibold text-sky-600 hover:bg-sky-50" onClick={() => setMenuOpen(false)}>
                    <Heart className="w-4 h-4" />
                    Wishlist
                  </Link>
                  <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-700 hover:bg-gray-50" onClick={() => setMenuOpen(false)}>
                    <User className="w-4 h-4 text-slate-400" />
                    My Profile
                  </Link>
                  <Link href="/chat" className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-700 hover:bg-gray-50 w-full" onClick={() => setMenuOpen(false)}>
                    <Bot className="w-4 h-4 text-slate-400" />
                    Chat with WISHI AI
                  </Link>
                  <button onClick={handleLogout} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-red-600 hover:bg-red-50 w-full">
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </>
              ) : (
                <div className="flex gap-2 pt-2 px-3">
                  <button onClick={() => openAuth('login')} className="flex-1 rounded-lg border border-gray-200 py-2.5 text-sm font-medium text-slate-700 hover:bg-gray-50">Login</button>
                  <button onClick={() => openAuth('register')} className="flex-1 rounded-lg bg-sky-600 py-2.5 text-sm font-semibold text-white hover:bg-sky-700">Signup</button>
                </div>
              )}
            </div>
          )}
        </div>
      </header>

      {/* Auth Modal */}
      {showAuthModal && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center px-4 py-6">
          <div className="w-full max-w-md rounded-[32px] bg-white shadow-2xl overflow-hidden">
            <div className="px-8 pt-8 pb-2 text-center">
              <div className="w-14 h-14 rounded-full bg-sky-600 flex items-center justify-center text-white mx-auto mb-4 shadow-lg shadow-sky-600/25">
                <ShoppingCart className="w-6 h-6" />
              </div>
              <h2 className="text-2xl font-bold text-slate-900">
                {authMode === 'login' ? 'Login to WISHI' : 'Join WISHI'}
              </h2>
              <p className="mt-2 text-sm text-slate-500 max-w-xs mx-auto">
                {authMode === 'login'
                  ? 'Sign in with your email or Google account.'
                  : 'Create your account in seconds using Google Sign-In. Start creating wishes and receive matches instantly.'}
              </p>
            </div>
            <div className="px-8 py-6">
              {/* Email/Password form */}
              <form onSubmit={handleEmailLogin} className="space-y-3 mb-4">
                <div>
                  <input
                    type="email"
                    placeholder="Email address"
                    value={loginEmailValue}
                    onChange={(e) => { setLoginEmailValue(e.target.value); setLoginError('') }}
                    className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:border-sky-500 focus:ring-1 focus:ring-sky-500 outline-none"
                    required
                    autoComplete="email"
                  />
                </div>
                <div>
                  <input
                    type="password"
                    placeholder="Password"
                    value={loginPassword}
                    onChange={(e) => { setLoginPassword(e.target.value); setLoginError('') }}
                    className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:border-sky-500 focus:ring-1 focus:ring-sky-500 outline-none"
                    required
                    autoComplete="current-password"
                  />
                </div>
                {loginError && (
                  <p className="text-xs text-red-500 text-center">{loginError}</p>
                )}
                <button
                  type="submit"
                  disabled={loginLoading}
                  className="w-full rounded-full bg-sky-600 hover:bg-sky-700 px-6 py-3.5 text-sm font-semibold text-white shadow-sm transition-all active:scale-[0.98] disabled:opacity-50"
                >
                  {loginLoading ? 'Signing in...' : 'Sign in'}
                </button>
              </form>

              {/* Divider */}
              <div className="flex items-center gap-3 mb-4">
                <div className="flex-1 h-px bg-gray-200" />
                <span className="text-xs text-slate-400">or</span>
                <div className="flex-1 h-px bg-gray-200" />
              </div>

              {/* Google button */}
              <button
                onClick={handleLogin}
                className="flex items-center justify-center gap-3 w-full rounded-full border border-gray-200 bg-white hover:bg-gray-50 px-6 py-3.5 text-sm font-semibold text-slate-700 shadow-sm transition-all active:scale-[0.98]"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Continue with Google
              </button>

              <div className="mt-5 text-center">
                <button
                  onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
                  className="text-sm text-slate-400 hover:text-sky-600 transition"
                >
                  {authMode === 'login' ? "Don't have an account? Sign up" : 'Already have an account? Log in'}
                </button>
              </div>
            </div>

            <div className="px-8 pb-6 pt-2 border-t border-gray-100 flex items-center justify-between">
              <p className="text-[11px] text-slate-300">
                By continuing, you agree to our <a href="/terms" className="underline hover:text-sky-600">Terms</a> & <a href="/privacy" className="underline hover:text-sky-600">Privacy</a>
              </p>
              <button onClick={() => setShowAuthModal(false)} className="text-xs font-medium text-slate-400 hover:text-slate-600 transition">Close</button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
