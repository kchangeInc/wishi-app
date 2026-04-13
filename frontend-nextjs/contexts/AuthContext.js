'use client'

import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { loginWithGoogleToken, loginWithEmail, logoutApi, getTokens, getUser, setUser, clearTokens } from '../lib/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUserState] = useState(null)
  const [loading, setLoading] = useState(true)

  // Rehydrate from localStorage on mount
  useEffect(() => {
    const tokens = getTokens()
    const cached = getUser()
    if (tokens?.access_token && cached) {
      setIsLoggedIn(true)
      setUserState(cached)
    }
    setLoading(false)
  }, [])

  const login = useCallback(async (googleIdToken) => {
    const userData = await loginWithGoogleToken(googleIdToken)
    setUser(userData)
    setUserState(userData)
    setIsLoggedIn(true)
    return userData
  }, [])

  const loginEmail = useCallback(async (email, password) => {
    const userData = await loginWithEmail(email, password)
    setUser(userData)
    setUserState(userData)
    setIsLoggedIn(true)
    return userData
  }, [])

  const logout = useCallback(async () => {
    await logoutApi()
    setIsLoggedIn(false)
    setUserState(null)
  }, [])

  // Legacy compat: simple login without Google (for demo/dev)
  const loginDemo = useCallback(() => {
    const demoUser = { id: 0, email: 'demo@wishi.in', name: 'Demo User', display_name: 'Demo User', role: 'buyer' }
    clearTokens()
    setUser(demoUser)
    setUserState(demoUser)
    setIsLoggedIn(true)
  }, [])

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, loading, login, loginEmail, loginDemo, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
