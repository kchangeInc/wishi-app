'use client'

import { motion } from 'framer-motion'
import { Shield, XCircle, Lock, UserCheck } from 'lucide-react'
import Header from '../../components/Header'
import Footer from '../../components/Footer'

const doNots = [
  { icon: XCircle, text: 'Sell your personal data' },
  { icon: XCircle, text: 'Store unnecessary personal information' },
  { icon: XCircle, text: 'Access your data without consent' },
]

const practices = [
  {
    icon: UserCheck,
    title: 'Minimal Data Collection',
    desc: 'WISHI only collects the information required to provide you with relevant matches, such as your wishlist preferences and login details via Google Sign-In.',
  },
  {
    icon: Lock,
    title: 'Trusted Security',
    desc: 'We use trusted authentication providers and industry-standard security practices to keep your data safe.',
  },
  {
    icon: Shield,
    title: 'Your Data, Your Experience',
    desc: 'Any data collected is used solely to improve your experience on the platform.',
  },
]

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } }
const fadeUp = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } }

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />

        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 pt-16 sm:pt-24 pb-12 sm:pb-16 text-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 rounded-full bg-emerald-50 border border-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-600 mb-5"
          >
            <Shield className="w-3 h-3" />
            Your privacy matters
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="text-3xl sm:text-5xl font-bold tracking-tight text-slate-900"
          >
            Privacy Policy
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto"
          >
            Your privacy is important to us.
          </motion.p>
        </div>
      </section>

      {/* Content */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-24">

        {/* What we collect */}
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: '-50px' }}
          className="space-y-4"
        >
          {practices.map((item) => (
            <motion.div key={item.title} variants={fadeUp} className="rounded-2xl border border-gray-100 p-5 sm:p-6 hover:shadow-lg hover:border-gray-200 transition-all">
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl bg-sky-50 flex items-center justify-center flex-shrink-0">
                  <item.icon className="w-5 h-5 text-sky-600" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">{item.title}</h3>
                  <p className="mt-1.5 text-sm text-slate-500 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* We do not */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="mt-10 rounded-2xl border border-red-100 bg-red-50/30 p-6 sm:p-8"
        >
          <h2 className="text-base font-bold text-slate-900 mb-4">We do not:</h2>
          <div className="space-y-3">
            {doNots.map((item) => (
              <div key={item.text} className="flex items-center gap-3">
                <item.icon className="w-5 h-5 text-red-400 flex-shrink-0" />
                <span className="text-sm font-medium text-slate-700">{item.text}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Last updated */}
        <p className="mt-10 text-center text-xs text-slate-300">Last updated: April 2026</p>
      </section>
      <Footer />
    </div>
  )
}
