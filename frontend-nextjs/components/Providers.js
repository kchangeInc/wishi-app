'use client'

import { createContext, useContext } from 'react'
import { GoogleOAuthProvider } from '@react-oauth/google'
import { AuthProvider } from '../contexts/AuthContext'

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || ''

const GoogleReadyContext = createContext(false)
export const useGoogleReady = () => useContext(GoogleReadyContext)

export default function Providers({ children }) {
  const inner = (
    <GoogleReadyContext.Provider value={!!GOOGLE_CLIENT_ID}>
      <AuthProvider>{children}</AuthProvider>
    </GoogleReadyContext.Provider>
  )

  if (!GOOGLE_CLIENT_ID) return inner

  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      {inner}
    </GoogleOAuthProvider>
  )
}
