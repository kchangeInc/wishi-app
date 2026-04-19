// frontend-nextjs/lib/api.js
// Centralized API client — wraps fetch with JWT, base URL, and token refresh

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

function getTokens() {
  if (typeof window === 'undefined') return null
  const raw = localStorage.getItem('wishi_tokens')
  if (!raw) return null
  try { return JSON.parse(raw) } catch { return null }
}

function setTokens(tokens) {
  localStorage.setItem('wishi_tokens', JSON.stringify(tokens))
}

function clearTokens() {
  localStorage.removeItem('wishi_tokens')
  localStorage.removeItem('wishi_user')
}

function getUser() {
  if (typeof window === 'undefined') return null
  const raw = localStorage.getItem('wishi_user')
  if (!raw) return null
  try { return JSON.parse(raw) } catch { return null }
}

function setUser(user) {
  localStorage.setItem('wishi_user', JSON.stringify(user))
}

let refreshPromise = null

async function refreshAccessToken() {
  const tokens = getTokens()
  if (!tokens?.refresh_token) {
    clearTokens()
    return null
  }

  // Deduplicate concurrent refresh attempts
  if (refreshPromise) return refreshPromise

  refreshPromise = (async () => {
    try {
      const res = await fetch(`${API_BASE}/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grant_type: 'refresh_token', refresh_token: tokens.refresh_token }),
      })
      if (!res.ok) {
        clearTokens()
        return null
      }
      const data = await res.json()
      setTokens({ access_token: data.access_token, refresh_token: data.refresh_token })
      if (data.user) setUser(data.user)
      return data.access_token
    } catch {
      clearTokens()
      return null
    } finally {
      refreshPromise = null
    }
  })()

  return refreshPromise
}

/**
 * Authenticated fetch wrapper.
 * On 401 → refresh token → retry once.
 */
export async function apiFetch(path, options = {}) {
  const tokens = getTokens()
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  if (tokens?.access_token) {
    headers['Authorization'] = `Bearer ${tokens.access_token}`
  }

  let res = await fetch(`${API_BASE}${path}`, { ...options, headers })

  // Auto-refresh on 401
  if (res.status === 401 && tokens?.refresh_token) {
    const newToken = await refreshAccessToken()
    if (newToken) {
      headers['Authorization'] = `Bearer ${newToken}`
      res = await fetch(`${API_BASE}${path}`, { ...options, headers })
    }
  }

  return res
}

// Convenience methods
export const api = {
  get: (path) => apiFetch(path),
  post: (path, body) => apiFetch(path, { method: 'POST', body: JSON.stringify(body) }),
  put: (path, body) => apiFetch(path, { method: 'PUT', body: JSON.stringify(body) }),
  del: (path) => apiFetch(path, { method: 'DELETE' }),
}

// Auth helpers (used by AuthContext)
export async function loginWithGoogleToken(idToken) {
  const res = await fetch(`${API_BASE}/auth/google-token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id_token: idToken }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Google login failed')
  }
  const data = await res.json()
  setTokens({ access_token: data.access_token, refresh_token: data.refresh_token })
  if (data.user) setUser(data.user)
  return data.user
}

export async function loginWithEmail(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Login failed')
  }
  const data = await res.json()
  setTokens({ access_token: data.access_token, refresh_token: data.refresh_token })
  if (data.user) setUser(data.user)
  return data.user
}

export async function logoutApi() {
  try {
    await apiFetch('/auth/logout', { method: 'POST' })
  } catch { /* ignore */ }
  clearTokens()
}

export { getTokens, setTokens, clearTokens, getUser, setUser }
