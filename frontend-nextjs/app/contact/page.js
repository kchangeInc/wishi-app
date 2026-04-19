'use client'

import { useState } from 'react'
import { Mail, MapPin, Phone, Send, ArrowRight, MessageSquare, FileText, Shield } from 'lucide-react'
import { motion } from 'framer-motion'
import Link from 'next/link'

const quickLinks = [
  { icon: MessageSquare, label: 'Chat with AI', description: 'Get instant answers from our AI assistant', href: '/chat', color: 'bg-violet-50 text-violet-600' },
  { icon: FileText, label: 'Help Center', description: 'Browse FAQs and guides', href: '/help', color: 'bg-sky-50 text-sky-600' },
  { icon: Shield, label: 'Privacy Policy', description: 'How we protect your data', href: '/privacy', color: 'bg-emerald-50 text-emerald-600' },
]

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', message: '' })
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    setSubmitted(true)
    setForm({ name: '', email: '', message: '' })
    setTimeout(() => setSubmitted(false), 4000)
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />
        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 pt-16 sm:pt-24 pb-12 sm:pb-16 text-center">
          <motion.p initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">
            Contact Us
          </motion.p>
          <motion.h1 initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }} className="mt-4 text-3xl sm:text-5xl font-bold tracking-tight text-slate-900">
            Get in <span className="text-sky-600">Touch</span>
          </motion.h1>
          <motion.p initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.2 }} className="mt-6 text-base sm:text-lg text-slate-500 max-w-2xl mx-auto leading-relaxed">
            Have a question, feedback, or need help? We'd love to hear from you.
          </motion.p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">

        {/* Contact Info Cards */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.3 }} className="grid gap-4 sm:grid-cols-3 mb-12">
          <div className="rounded-2xl border border-gray-100 p-5 text-center hover:shadow-lg hover:border-gray-200 transition-all">
            <div className="w-10 h-10 rounded-xl bg-sky-50 flex items-center justify-center mx-auto mb-3">
              <Mail className="w-5 h-5 text-sky-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Email</h3>
            <a href="mailto:support@wishi.in" className="text-sm text-sky-600 hover:underline mt-1 block">support@wishi.in</a>
          </div>
          <div className="rounded-2xl border border-gray-100 p-5 text-center hover:shadow-lg hover:border-gray-200 transition-all">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center mx-auto mb-3">
              <Phone className="w-5 h-5 text-emerald-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Phone</h3>
            <p className="text-sm text-slate-400 mt-1">Coming soon</p>
          </div>
          <div className="rounded-2xl border border-gray-100 p-5 text-center hover:shadow-lg hover:border-gray-200 transition-all">
            <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center mx-auto mb-3">
              <MapPin className="w-5 h-5 text-amber-600" />
            </div>
            <h3 className="text-sm font-bold text-slate-900">Office</h3>
            <p className="text-sm text-slate-400 mt-1">India</p>
          </div>
        </motion.div>

        {/* Contact Form */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.4 }} className="rounded-2xl border border-gray-100 p-6 sm:p-8 mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-6">Send us a message</h2>

          {submitted && (
            <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="mb-6 flex items-center gap-2 rounded-lg bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Message sent! We'll get back to you soon.
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Name</label>
              <input
                type="text"
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition"
                placeholder="Your name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Email</label>
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition"
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Message</label>
              <textarea
                required
                rows={4}
                value={form.message}
                onChange={(e) => setForm({ ...form, message: e.target.value })}
                className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition resize-none"
                placeholder="How can we help?"
              />
            </div>
            <button type="submit" className="rounded-full bg-sky-600 hover:bg-sky-700 text-white px-6 py-3 text-sm font-semibold transition inline-flex items-center gap-2">
              <Send className="w-4 h-4" />
              Send Message
            </button>
          </form>
        </motion.div>

        {/* Quick Links */}
        <section className="mb-12">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Quick Help</h2>
          <div className="grid gap-4 sm:grid-cols-3">
            {quickLinks.map((item) => (
              <Link key={item.label} href={item.href} className="group rounded-2xl border border-gray-100 p-5 hover:shadow-lg hover:border-gray-200 transition-all">
                <div className={`w-10 h-10 rounded-xl ${item.color} flex items-center justify-center mb-3`}>
                  <item.icon className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">{item.label}</h3>
                <p className="text-xs text-slate-400 mt-1">{item.description}</p>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
