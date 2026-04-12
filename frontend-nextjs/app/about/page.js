'use client'

import { motion } from 'framer-motion'
import { ArrowRight, RefreshCw, Target, Zap, Users } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Header from '../../components/Header'
import Footer from '../../components/Footer'
import { useAuth } from '../../contexts/AuthContext'

const values = [
  {
    icon: RefreshCw,
    title: 'Demand-First Model',
    desc: 'Instead of browsing listings, users simply tell us what they are looking for. We aggregate this demand and surface relevant listings from across the web.',
    color: 'from-sky-500 to-sky-600',
    bg: 'bg-sky-50',
  },
  {
    icon: Zap,
    title: 'Faster Buying',
    desc: 'No more hours searching across multiple websites. Create a wish in seconds and let matches come to you.',
    color: 'from-amber-500 to-amber-600',
    bg: 'bg-amber-50',
  },
  {
    icon: Target,
    title: 'Better Matching',
    desc: 'We believe the future of marketplaces is not about more listings — it\'s about better matching.',
    color: 'from-emerald-500 to-emerald-600',
    bg: 'bg-emerald-50',
  },
  {
    icon: Users,
    title: 'Connecting Buyers & Sellers',
    desc: 'Sellers don\'t know what buyers actually want. WISHI bridges that gap by making real demand visible.',
    color: 'from-violet-500 to-violet-600',
    bg: 'bg-violet-50',
  },
]

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } }
const fadeUp = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } }

export default function AboutPage() {
  const router = useRouter()
  const { isLoggedIn } = useAuth()

  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />

        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 pt-16 sm:pt-24 pb-12 sm:pb-16 text-center">
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold"
          >
            About Us
          </motion.p>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="mt-4 text-3xl sm:text-5xl font-bold tracking-tight text-slate-900"
          >
            About <span className="text-sky-600">WISHI</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-6 text-base sm:text-lg text-slate-500 max-w-2xl mx-auto leading-relaxed"
          >
            WISHI is a demand-first marketplace platform designed to simplify how people buy.
          </motion.p>
        </div>
      </section>

      {/* Story */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="rounded-2xl border border-gray-100 bg-gray-50/50 p-6 sm:p-8"
        >
          <h2 className="text-lg sm:text-xl font-bold text-slate-900 mb-4">The Problem</h2>
          <p className="text-sm sm:text-base text-slate-500 leading-relaxed">
            Today, buyers spend hours searching across multiple websites to find the right product.
            At the same time, sellers don't know what buyers actually want.
          </p>

          <div className="my-6 flex items-center gap-3">
            <div className="flex-1 h-px bg-gray-200" />
            <span className="text-xs font-bold tracking-wider text-sky-500">WISHI SOLVES THIS BY FLIPPING THE MODEL</span>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          <h2 className="text-lg sm:text-xl font-bold text-slate-900 mb-4">The Solution</h2>
          <p className="text-sm sm:text-base text-slate-500 leading-relaxed">
            Instead of browsing listings, users simply tell us what they are looking for.
            We aggregate this demand and surface relevant listings from across the web.
          </p>
        </motion.div>

        {/* Goal */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="mt-8 rounded-2xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-600 p-6 sm:p-8 text-center relative overflow-hidden"
        >
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.4),_transparent_40%)]" />
          <div className="relative">
            <p className="text-xs uppercase tracking-[0.3em] text-white/60 font-semibold">Our Goal</p>
            <h3 className="mt-3 text-xl sm:text-2xl font-bold text-white">
              Make buying faster, smarter, and more efficient.
            </h3>
            <p className="mt-3 text-sm text-white/70 max-w-lg mx-auto">
              We believe the future of marketplaces is not about more listings — it's about better matching.
            </p>
          </div>
        </motion.div>

        {/* Values */}
        <div className="mt-12">
          <h2 className="text-center text-xl sm:text-2xl font-bold text-slate-900 mb-8">What We Stand For</h2>
          <motion.div
            className="grid gap-4 sm:grid-cols-2"
            variants={stagger}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: '-50px' }}
          >
            {values.map((item) => (
              <motion.div key={item.title} variants={fadeUp} className="rounded-2xl border border-gray-100 p-5 hover:shadow-lg hover:border-gray-200 transition-all">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${item.color} flex items-center justify-center mb-3 shadow-lg`}>
                  <item.icon className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">{item.title}</h3>
                <p className="mt-1.5 text-sm text-slate-400 leading-relaxed">{item.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="mt-14 text-center"
        >
          <p className="text-sm text-slate-400 mb-4">Ready to try a smarter way to buy?</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              onClick={() => router.push(isLoggedIn ? '/wishlist' : '/')}
              className="rounded-full bg-sky-600 hover:bg-sky-700 active:scale-[0.98] text-white px-8 py-3.5 text-sm font-semibold transition-all shadow-lg shadow-sky-600/25 inline-flex items-center gap-2"
            >
              Create Your First Wish
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => router.push('/how-it-works')}
              className="rounded-full border border-gray-200 hover:border-gray-300 text-slate-600 hover:text-slate-900 px-7 py-3.5 text-sm font-medium transition-all"
            >
              See How It Works
            </button>
          </div>
        </motion.div>
      </section>
      <Footer />
    </div>
  )
}
