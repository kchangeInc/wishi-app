'use client'

import { motion } from 'framer-motion'
import { Map, Home, Heart, Bell, MessageSquare, HelpCircle, Info, Footprints, Shield, FileText, User, Search } from 'lucide-react'
import Link from 'next/link'
import Header from '../../components/Header'
import Footer from '../../components/Footer'

const sections = [
  {
    title: 'Main',
    color: 'from-sky-500 to-sky-600',
    bg: 'bg-sky-50',
    text: 'text-sky-600',
    links: [
      { label: 'Home', href: '/', icon: Home, desc: 'Landing page with features and trending wishlists' },
      { label: 'Search', href: '/search', icon: Search, desc: 'Search products, categories, and brands' },
    ],
  },
  {
    title: 'Wishlist',
    color: 'from-violet-500 to-violet-600',
    bg: 'bg-violet-50',
    text: 'text-violet-600',
    links: [
      { label: 'My Wishlists', href: '/wishlist', icon: Heart, desc: 'Create and manage your wishlists' },
      { label: 'Notifications', href: '/notifications', icon: Bell, desc: 'Match alerts, price drops, and expiry reminders' },
    ],
  },
  {
    title: 'AI & Support',
    color: 'from-emerald-500 to-emerald-600',
    bg: 'bg-emerald-50',
    text: 'text-emerald-600',
    links: [
      { label: 'Chat with WISHI AI', href: '/chat', icon: MessageSquare, desc: 'Ask questions about WISHI, categories, and more' },
      { label: 'Help & Support', href: '/help', icon: HelpCircle, desc: 'FAQs, contact info, and troubleshooting' },
    ],
  },
  {
    title: 'Company',
    color: 'from-amber-500 to-amber-600',
    bg: 'bg-amber-50',
    text: 'text-amber-600',
    links: [
      { label: 'About Us', href: '/about', icon: Info, desc: 'Learn about WISHI and our demand-first model' },
      { label: 'How It Works', href: '/how-it-works', icon: Footprints, desc: '4 simple steps from wish to match' },
    ],
  },
  {
    title: 'Legal',
    color: 'from-slate-500 to-slate-600',
    bg: 'bg-slate-50',
    text: 'text-slate-600',
    links: [
      { label: 'Privacy Policy', href: '/privacy', icon: Shield, desc: 'How we handle and protect your data' },
      { label: 'Terms of Use', href: '/terms', icon: FileText, desc: 'Rules and disclaimers for using WISHI' },
    ],
  },
  {
    title: 'Account',
    color: 'from-rose-500 to-rose-600',
    bg: 'bg-rose-50',
    text: 'text-rose-600',
    links: [
      { label: 'Dashboard', href: '/dashboard', icon: User, desc: 'Your profile, settings, and feedback' },
    ],
  },
]

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.06 } } }
const fadeUp = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.3 } } }

export default function SitemapPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />

        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 pt-16 sm:pt-24 pb-12 sm:pb-16 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className="w-14 h-14 rounded-2xl bg-gradient-to-br from-sky-500 to-violet-600 flex items-center justify-center mx-auto mb-5 shadow-lg"
          >
            <Map className="w-7 h-7 text-white" />
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="text-3xl sm:text-5xl font-bold tracking-tight text-slate-900"
          >
            Sitemap
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto"
          >
            All pages on WISHI at a glance.
          </motion.p>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">
        <div className="space-y-8">
          {sections.map((section) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
            >
              <h2 className={`text-xs font-bold uppercase tracking-[0.2em] ${section.text} mb-3`}>{section.title}</h2>
              <motion.div
                className="grid gap-3"
                variants={stagger}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true }}
              >
                {section.links.map((link) => (
                  <motion.div key={link.href} variants={fadeUp}>
                    <Link
                      href={link.href}
                      className="group relative flex items-center gap-4 border border-gray-100 rounded-2xl p-4 hover:shadow-lg hover:border-gray-200 transition-all duration-300"
                    >
                      <div className={`absolute top-0 left-6 right-6 h-px bg-gradient-to-r ${section.color} opacity-30 rounded-full`} />
                      <div className={`w-10 h-10 rounded-xl ${section.bg} flex items-center justify-center flex-shrink-0`}>
                        <link.icon className={`w-5 h-5 ${section.text}`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-[15px] font-semibold text-slate-900 group-hover:text-sky-600 transition">{link.label}</h3>
                        <p className="text-xs text-slate-400 mt-0.5">{link.desc}</p>
                      </div>
                      <span className="text-xs text-slate-300 font-mono hidden sm:block">{link.href}</span>
                    </Link>
                  </motion.div>
                ))}
              </motion.div>
            </motion.div>
          ))}
        </div>
      </section>

      <Footer />
    </div>
  )
}
