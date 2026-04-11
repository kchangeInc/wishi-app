'use client'

import { motion } from 'framer-motion'

const searchResults = [
  { title: 'Hyundai i20 under ₹6L', subtitle: 'Chennai', price: '₹5.5L' },
  { title: 'iPhone 15 Pro Max', subtitle: 'Delhi, NCR', price: '₹1.2L' },
  { title: 'Royal Enfield Classic 350', subtitle: 'Bangalore', price: '₹2.1L' },
  { title: 'MacBook Pro M3', subtitle: 'Chennai', price: '₹2.5L' },
  { title: '3BHK Apartment in Pune', subtitle: 'Pune', price: '₹85L' },
  { title: 'Samsung 65" QLED TV', subtitle: 'Hyderabad', price: '₹1.8L' },
  { title: 'Nike Sports Shoes', subtitle: 'Mumbai', price: '₹3,999' },
  { title: 'Premium Leather Jacket', subtitle: 'Bangalore', price: '₹14,999' },
]

export default function SearchPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <header className="mb-10">
          <p className="text-sm uppercase tracking-[0.4em] text-pinterest-red font-semibold">Search results</p>
          <h1 className="mt-4 text-4xl font-bold text-slate-900">Discover more deals and wishlists</h1>
          <p className="mt-4 text-gray-600 max-w-2xl">A Pinterest-inspired search page for browsing additional items, with infinite-load style sections and filters.</p>
        </header>

        <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          {searchResults.map((result, index) => (
            <motion.article
              key={result.title}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + index * 0.05 }}
              className="rounded-3xl overflow-hidden bg-white shadow-lg border border-gray-200"
            >
              <div className="h-72 bg-cover bg-center" style={{ backgroundImage: `linear-gradient(180deg, rgba(0,0,0,0.1), rgba(0,0,0,0.25)), url('https://images.unsplash.com/photo-1515169067865-5387ec356754?auto=format&fit=crop&w=900&q=80')` }} />
              <div className="p-6">
                <p className="text-xs uppercase tracking-[0.25em] text-pinterest-red font-semibold mb-3">{result.subtitle}</p>
                <h2 className="text-2xl font-semibold text-slate-900 mb-3">{result.title}</h2>
                <p className="text-sm text-gray-600 mb-6">Browse detailed listings, seller ratings, and related wishlist matches in a Pinterest-style feed.</p>
                <div className="flex items-center justify-between text-sm text-gray-700">
                  <span className="font-semibold">{result.price}</span>
                  <button className="rounded-full border border-gray-200 px-4 py-2 text-xs font-semibold text-gray-700 hover:border-pinterest-red hover:text-pinterest-red transition">View listing</button>
                </div>
              </div>
            </motion.article>
          ))}
        </div>

        <div className="mt-12 text-center">
          <button className="pinterest-btn px-8 py-4">Load more results</button>
        </div>
      </div>
    </div>
  )
}
