'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { HelpCircle, MessageCircle, Mail, ChevronDown, Search, ArrowRight, FileText, Shield, Clock, CreditCard, Package, UserCog } from 'lucide-react'
import { useRouter } from 'next/navigation'
import Header from '../../components/Header'
import Footer from '../../components/Footer'

const faqCategories = [
  {
    icon: Package,
    title: 'Wishlists & Matching',
    color: 'from-sky-500 to-sky-600',
    bg: 'bg-sky-50',
    faqs: [
      {
        q: 'How do I create a wishlist?',
        a: 'Click the "Create Wishlist" button on the Wishlist page or homepage. Select a category, subcategory, fill in your preferences, and submit. Our system will start finding matches for you automatically.',
      },
      {
        q: 'How does matching work?',
        a: 'WISHI aggregates listings from multiple marketplaces (OLX, Amazon, Flipkart, 99acres, etc.) and uses smart matching to find products that meet your wishlist criteria. Matches are ranked by relevance, price, and condition.',
      },
      {
        q: 'Can I filter matches by marketplace?',
        a: 'Yes! On the matches page, you can filter results by specific marketplaces using the filter chips at the top. You can also set preferred marketplaces when creating your wishlist.',
      },
      {
        q: 'How long does a wishlist stay active?',
        a: 'Each wishlist is active for 30 days from creation. You can see the expiry date on your wishlist card. After expiry, you can always create a new wishlist with the same preferences.',
      },
      {
        q: 'Can I favourite or remove matches?',
        a: 'Yes! Click the heart icon on any match card to favourite it. Click the X icon to remove matches you are not interested in. Favourited matches appear first when you sort by "Favourites First".',
      },
    ],
  },
  {
    icon: UserCog,
    title: 'Account & Profile',
    color: 'from-violet-500 to-violet-600',
    bg: 'bg-violet-50',
    faqs: [
      {
        q: 'How do I create an account?',
        a: 'Click the "Signup" button and sign in with your Google account. No passwords needed — just one click with Google Sign-In.',
      },
      {
        q: 'Can I change my profile information?',
        a: 'Yes, go to your Profile page by clicking your avatar in the header and selecting "My Profile". From there you can update your name, location, and notification preferences.',
      },
      {
        q: 'Is my data secure?',
        a: 'Absolutely. We use Google Sign-In for secure authentication, collect minimal data, and never sell your personal information to third parties. See our Privacy Policy for full details.',
      },
    ],
  },
  {
    icon: CreditCard,
    title: 'Pricing & Payments',
    color: 'from-emerald-500 to-emerald-600',
    bg: 'bg-emerald-50',
    faqs: [
      {
        q: 'Is WISHI free to use?',
        a: 'Yes! Creating wishlists and receiving matches is completely free. WISHI is a discovery platform — we help you find what you want, and you connect directly with sellers.',
      },
      {
        q: 'Does WISHI handle payments?',
        a: 'No. WISHI is not an e-commerce platform. When you find a match, you are redirected to the original marketplace (OLX, Amazon, etc.) to complete the transaction directly with the seller.',
      },
    ],
  },
  {
    icon: Clock,
    title: 'Notifications & Alerts',
    color: 'from-amber-500 to-amber-600',
    bg: 'bg-amber-50',
    faqs: [
      {
        q: 'How do notifications work?',
        a: 'When new matches are found for your active wishlists, you receive alerts via the bell icon in the header. You can manage notification preferences from your profile settings.',
      },
      {
        q: 'Can I get email notifications?',
        a: 'Email notification support is coming soon. Currently, all alerts are delivered within the WISHI app through the notification bell in the header.',
      },
    ],
  },
]

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.08 } } }
const fadeUp = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0, transition: { duration: 0.4 } } }

function FAQItem({ faq }) {
  const [open, setOpen] = useState(false)

  return (
    <div className="border border-gray-100 rounded-xl overflow-hidden hover:border-gray-200 transition">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-3 w-full px-5 py-4 text-left"
      >
        <HelpCircle className="w-4 h-4 text-sky-500 flex-shrink-0" />
        <span className="flex-1 text-sm font-medium text-slate-800">{faq.q}</span>
        <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-5 pb-4 pl-12">
              <p className="text-sm text-slate-500 leading-relaxed">{faq.a}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function HelpPage() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState('')

  const allFaqs = faqCategories.flatMap((cat) =>
    cat.faqs.map((faq) => ({ ...faq, category: cat.title }))
  )

  const filteredFaqs = searchQuery.trim().length >= 2
    ? allFaqs.filter(
        (faq) =>
          faq.q.toLowerCase().includes(searchQuery.toLowerCase()) ||
          faq.a.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : null

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
            className="w-16 h-16 rounded-2xl bg-gradient-to-br from-sky-500 to-violet-600 flex items-center justify-center mx-auto mb-5 shadow-lg"
          >
            <HelpCircle className="w-8 h-8 text-white" />
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className="text-3xl sm:text-5xl font-bold tracking-tight text-slate-900"
          >
            Help & <span className="text-sky-600">Support</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="mt-4 text-base sm:text-lg text-slate-500 max-w-xl mx-auto"
          >
            Find answers to your questions or reach out to our team.
          </motion.p>

          {/* Search */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
            className="mt-8 max-w-lg mx-auto"
          >
            <div className="flex items-center border border-gray-200 rounded-xl overflow-hidden bg-white shadow-sm focus-within:ring-2 focus-within:ring-sky-500/20 focus-within:border-sky-500 transition">
              <Search className="w-4 h-4 text-slate-300 ml-4 flex-shrink-0" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search help articles..."
                className="flex-1 px-3 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
              />
            </div>
          </motion.div>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">

        {/* Search Results */}
        {filteredFaqs !== null ? (
          <div className="mb-12">
            <p className="text-sm text-slate-400 mb-4">
              {filteredFaqs.length} result{filteredFaqs.length !== 1 ? 's' : ''} for &ldquo;{searchQuery}&rdquo;
            </p>
            {filteredFaqs.length > 0 ? (
              <div className="space-y-2">
                {filteredFaqs.map((faq, i) => (
                  <FAQItem key={i} faq={faq} />
                ))}
              </div>
            ) : (
              <div className="text-center py-10 rounded-2xl border border-gray-100 bg-gray-50/50">
                <HelpCircle className="w-10 h-10 text-slate-200 mx-auto mb-3" />
                <p className="text-sm text-slate-500">No results found. Try a different search term or browse the categories below.</p>
              </div>
            )}
          </div>
        ) : null}

        {/* Quick Actions */}
        <motion.div
          className="grid sm:grid-cols-3 gap-4 mb-12"
          variants={stagger}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
        >
          <motion.a
            href="mailto:support@wishi.in"
            variants={fadeUp}
            className="flex items-center gap-3 p-4 rounded-2xl border border-gray-100 hover:border-sky-200 hover:shadow-lg hover:bg-sky-50/30 transition-all group cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-sky-600 flex items-center justify-center shadow-lg flex-shrink-0">
              <Mail className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Email Us</h3>
              <p className="text-xs text-slate-400">support@wishi.in</p>
            </div>
          </motion.a>

          <motion.button
            variants={fadeUp}
            className="flex items-center gap-3 p-4 rounded-2xl border border-gray-100 hover:border-violet-200 hover:shadow-lg hover:bg-violet-50/30 transition-all group cursor-pointer text-left"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-violet-600 flex items-center justify-center shadow-lg flex-shrink-0">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Chat with AI</h3>
              <p className="text-xs text-slate-400">Ask WISHI AI</p>
            </div>
          </motion.button>

          <motion.div
            variants={fadeUp}
            onClick={() => router.push('/terms')}
            className="flex items-center gap-3 p-4 rounded-2xl border border-gray-100 hover:border-emerald-200 hover:shadow-lg hover:bg-emerald-50/30 transition-all group cursor-pointer"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-600 flex items-center justify-center shadow-lg flex-shrink-0">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Policies</h3>
              <p className="text-xs text-slate-400">Terms & Privacy</p>
            </div>
          </motion.div>
        </motion.div>

        {/* FAQ Categories */}
        <div className="space-y-10">
          {faqCategories.map((cat) => (
            <motion.div
              key={cat.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
            >
              <div className="flex items-center gap-3 mb-4">
                <div className={`w-9 h-9 rounded-xl bg-gradient-to-br ${cat.color} flex items-center justify-center shadow-lg`}>
                  <cat.icon className="w-4.5 h-4.5 text-white" />
                </div>
                <h2 className="text-lg font-bold text-slate-900">{cat.title}</h2>
              </div>
              <div className="space-y-2">
                {cat.faqs.map((faq, i) => (
                  <FAQItem key={i} faq={faq} />
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Safety Banner */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="mt-12 rounded-2xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-600 p-6 sm:p-8 text-center relative overflow-hidden"
        >
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.4),_transparent_40%)]" />
          <div className="relative">
            <Shield className="w-8 h-8 text-white/80 mx-auto mb-3" />
            <h3 className="text-xl sm:text-2xl font-bold text-white">
              Your Safety Matters
            </h3>
            <p className="mt-3 text-sm text-white/70 max-w-lg mx-auto leading-relaxed">
              WISHI is a discovery platform. We redirect you to trusted marketplaces. Always verify seller details before making any payment. Never share OTPs or banking passwords.
            </p>
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="mt-14 text-center"
        >
          <p className="text-sm text-slate-400 mb-4">Still have questions?</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <a
              href="mailto:support@wishi.in"
              className="rounded-full bg-sky-600 hover:bg-sky-700 active:scale-[0.98] text-white px-8 py-3.5 text-sm font-semibold transition-all shadow-lg shadow-sky-600/25 inline-flex items-center gap-2"
            >
              Contact Support
              <ArrowRight className="w-4 h-4" />
            </a>
            <button
              onClick={() => router.push('/about')}
              className="rounded-full border border-gray-200 hover:border-gray-300 text-slate-600 hover:text-slate-900 px-7 py-3.5 text-sm font-medium transition-all"
            >
              About WISHI
            </button>
          </div>
        </motion.div>
      </section>

      <Footer />
    </div>
  )
}
