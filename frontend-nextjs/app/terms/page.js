'use client'

import { motion } from 'framer-motion'
import { FileText, ExternalLink, UserCheck, AlertTriangle, Scale, Globe } from 'lucide-react'
import Header from '../../components/Header'
import Footer from '../../components/Footer'

const terms = [
  {
    icon: Globe,
    title: 'No Direct Sales',
    desc: 'WISHI does not host or sell products directly. All listings are provided via external platforms.',
  },
  {
    icon: UserCheck,
    title: 'User Responsibility',
    desc: 'Users are responsible for verifying the authenticity of listings before making any transaction.',
  },
  {
    icon: Scale,
    title: 'Liability Disclaimer',
    desc: 'WISHI is not liable for transactions, disputes, or interactions between buyers and sellers.',
  },
  {
    icon: ExternalLink,
    title: 'External Sources',
    desc: 'We aim to provide accurate and relevant matches, but availability and listing accuracy depend on external sources.',
  },
]

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } }
const fadeUp = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } }

export default function TermsPage() {
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
            className="inline-flex items-center gap-2 rounded-full bg-amber-50 border border-amber-100 px-3 py-1 text-xs font-semibold text-amber-600 mb-5"
          >
            <FileText className="w-3 h-3" />
            Legal
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="text-3xl sm:text-5xl font-bold tracking-tight text-slate-900"
          >
            Terms of Use
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto"
          >
            By using WISHI, you agree to the following:
          </motion.p>
        </div>
      </section>

      {/* Terms */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-24">
        <motion.div
          className="space-y-4"
          variants={stagger}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: '-50px' }}
        >
          {terms.map((item, i) => (
            <motion.div key={item.title} variants={fadeUp} className="rounded-2xl border border-gray-100 p-5 sm:p-6 hover:shadow-lg hover:border-gray-200 transition-all">
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center flex-shrink-0">
                  <item.icon className="w-5 h-5 text-amber-600" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[11px] font-bold tracking-wider text-amber-400">{String(i + 1).padStart(2, '0')}</span>
                    <h3 className="text-sm font-bold text-slate-900">{item.title}</h3>
                  </div>
                  <p className="text-sm text-slate-500 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Notice */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="mt-10 rounded-2xl border border-amber-100 bg-amber-50/30 p-6 sm:p-8 flex gap-4"
        >
          <AlertTriangle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="text-sm font-bold text-slate-900 mb-1">Please Note</h3>
            <p className="text-sm text-slate-500 leading-relaxed">
              WISHI acts as a discovery platform only. We connect demand with publicly available supply but do not facilitate or guarantee any transaction. Always exercise caution and verify details independently before proceeding with any purchase.
            </p>
          </div>
        </motion.div>

        <p className="mt-10 text-center text-xs text-slate-300">Last updated: April 2026</p>
      </section>
      <Footer />
    </div>
  )
}
