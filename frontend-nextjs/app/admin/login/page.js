'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../../contexts/AuthContext'

export default function AdminLoginPage() {
  const router = useRouter()
  const { loginEmail } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await loginEmail(email, password)
      if (user?.role !== 'admin') {
        setError('Access denied. Admin privileges required.')
        setLoading(false)
        return
      }
      router.push('/dashboard')
    } catch (err) {
      setError(err.message || 'Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="text-center mb-6">
            <div className="w-12 h-12 rounded-full bg-slate-900 flex items-center justify-center text-white mx-auto mb-4">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-xl font-bold text-slate-900">Admin Login</h1>
            <p className="text-sm text-slate-500 mt-1">Sign in to the admin panel</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setError('') }}
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:border-sky-500 focus:ring-1 focus:ring-sky-500 outline-none"
                placeholder="admin@wishi.in"
                required
                autoComplete="email"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => { setPassword(e.target.value); setError('') }}
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-700 placeholder-slate-400 focus:border-sky-500 focus:ring-1 focus:ring-sky-500 outline-none"
                placeholder="Enter your password"
                required
                autoComplete="current-password"
              />
            </div>

            {error && (
              <p className="text-xs text-red-500 text-center">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-full bg-slate-900 hover:bg-slate-800 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-all active:scale-[0.98] disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>
        </div>

        <p className="text-center text-xs text-slate-400 mt-6">WISHI Admin Panel</p>
      </div>
    </div>
  )
}
