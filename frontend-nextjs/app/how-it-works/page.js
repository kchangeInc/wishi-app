'use client'

import { motion } from 'framer-motion'
import { ClipboardList, Radar, Bell, ExternalLink, ArrowRight } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../contexts/AuthContext'

const steps = [
  {
    num: '01',
    icon: ClipboardList,
    title: 'Tell Us What You Want',
    desc: 'Create a wishlist by entering details like product, budget, and location.',
    color: 'from-sky-500 to-sky-600',
    bg: 'bg-sky-50',
    text: 'text-sky-600',
    border: 'border-sky-100',
  },
  {
    num: '02',
    icon: Radar,
    title: 'We Find Matches for You',
    desc: 'Our system continuously scans publicly available listings across the web and finds matches based on your exact requirements.',
    color: 'from-violet-500 to-violet-600',
    bg: 'bg-violet-50',
    text: 'text-violet-600',
    border: 'border-violet-100',
  },
  {
    num: '03',
    icon: Bell,
    title: 'Get Real-Time Updates',
    desc: 'New matches are added regularly, so you never miss an opportunity.',
    color: 'from-emerald-500 to-emerald-600',
    bg: 'bg-emerald-50',
    text: 'text-emerald-600',
    border: 'border-emerald-100',
  },
  {
    num: '04',
    icon: ExternalLink,
    title: 'Click and Connect',
    desc: 'When you find something you like, click the link and connect directly with the seller on their platform.',
    color: 'from-amber-500 to-amber-600',
    bg: 'bg-amber-50',
    text: 'text-amber-600',
    border: 'border-amber-100',
  },
]

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.12 } } }
const fadeUp = { hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.45 } } }

export default function HowItWorksPage() {
  const router = useRouter()
  const { isLoggedIn } = useAuth()

  return (
    <div className="min-h-screen bg-white">
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
            How WISHI Works
          </motion.p>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="mt-4 text-3xl sm:text-5xl font-bold tracking-tight text-slate-900"
          >
            From Wish to Match<br />
            <span className="text-sky-600">in 4 Simple Steps</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto"
          >
            Stop scrolling through endless listings. Tell us what you need and let WISHI do the heavy lifting.
          </motion.p>
        </div>
      </section>

      {/* Steps */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-24">
        <motion.div
          className="space-y-6"
          variants={stagger}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: '-60px' }}
        >
          {steps.map((step, i) => (
            <motion.div key={step.num} variants={fadeUp}>
              <div className={`relative rounded-2xl border ${step.border} bg-white p-6 sm:p-8 hover:shadow-lg transition-shadow`}>
                {/* Connector line */}
                {i < steps.length - 1 && (
                  <div className="absolute left-10 sm:left-12 -bottom-6 w-px h-6 bg-gray-200" />
                )}

                <div className="flex gap-5 sm:gap-6">
                  {/* Icon */}
                  <div className={`w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center flex-shrink-0 shadow-lg`}>
                    <step.icon className="w-6 h-6 sm:w-7 sm:h-7 text-white" />
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs font-bold tracking-wider ${step.text}`}>STEP {step.num}</span>
                    </div>
                    <h3 className="text-lg sm:text-xl font-bold text-slate-900">{step.title}</h3>
                    <p className="mt-2 text-sm sm:text-base text-slate-500 leading-relaxed">{step.desc}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="mt-16 rounded-3xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-600 p-8 sm:p-10 text-center relative overflow-hidden"
        >
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.4),_transparent_40%)]" />
          <div className="relative">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">Ready to create your first wish?</h2>
            <p className="mt-3 text-sm sm:text-base text-white/80 max-w-lg mx-auto">
              It takes less than a minute. No endless browsing. No missed deals.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={() => router.push(isLoggedIn ? '/wishlist' : '/')}
                className="rounded-full bg-white text-sky-600 hover:bg-sky-50 px-8 py-3.5 text-sm font-semibold transition-all shadow-lg active:scale-[0.98] inline-flex items-center gap-2"
              >
                Create Your First Wish
                <ArrowRight className="w-4 h-4" />
              </button>
              <button
                onClick={() => router.push('/')}
                className="rounded-full border border-white/30 text-white hover:bg-white/10 px-7 py-3.5 text-sm font-medium transition-all"
              >
                Back to Home
              </button>
            </div>
          </div>
        </motion.div>
      </section>
    </div>
  )
}
