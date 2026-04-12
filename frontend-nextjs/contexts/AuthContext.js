'use client'

import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('wishi_auth')
    if (stored === 'true') setIsLoggedIn(true)
  }, [])

  const login = () => {
    setIsLoggedIn(true)
    localStorage.setItem('wishi_auth', 'true')
  }

  const logout = () => {
    setIsLoggedIn(false)
    localStorage.removeItem('wishi_auth')
  }

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
