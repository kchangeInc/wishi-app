import Link from 'next/link'

const categories = [
  { title: 'CATEGORIES', links: [
    { label: 'Automobile', href: '/category/automobile' },
    { label: 'Electronics', href: '/category/electronics' },
    { label: 'Real Estate', href: '/category/real-estate' },
    { label: 'Fashion', href: '/category/fashion' },
    { label: 'Home & Living', href: '/category/home-living' },
  ]},
  { title: 'POPULAR CITIES', links: [
    { label: 'Mumbai', href: '/city/mumbai' },
    { label: 'Delhi', href: '/city/delhi' },
    { label: 'Bangalore', href: '/city/bangalore' },
    { label: 'Chennai', href: '/city/chennai' },
    { label: 'Hyderabad', href: '/city/hyderabad' },
  ]},
  { title: 'COMPANY', links: [
    { label: 'About Us', href: '/about' },
    { label: 'How It Works', href: '/how-it-works' },
    { label: 'Contact', href: '/contact' },
    // { label: 'Careers', href: '/careers' },
  ]},
  { title: 'LEGAL', links: [
    { label: 'Terms of Use', href: '/terms' },
    { label: 'Privacy Policy', href: '/privacy' },
    { label: 'Help & Support', href: '/help' },
  ]},
]

const marketplaces = ['OLX', 'Amazon', 'Flipkart', 'CarDekho', 'Cars24', '99acres', 'MagicBricks', 'Myntra', 'Pepperfry']

export default function Footer() {
  return (
    <footer>
      {/* Top section */}
      <div className="border-t border-gray-200 bg-gray-50/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-8">
            {categories.map((col) => (
              <div key={col.title}>
                <h4 className="text-xs font-bold text-slate-900 uppercase tracking-[0.15em] mb-4">{col.title}</h4>
                <ul className="space-y-2.5">
                  {col.links.map((link) => (
                    <li key={link.label}>
                      {link.href ? (
                        <Link href={link.href} className="text-sm text-slate-500 hover:text-sky-600 transition">
                          {link.label}
                        </Link>
                      ) : (
                        <span className="text-sm text-slate-500">{link.label}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom section */}
      <div className="bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
          {/* Marketplace partners */}
          <div className="flex flex-wrap items-center justify-center gap-x-6 sm:gap-x-10 gap-y-3 mb-6">
            {marketplaces.map((name) => (
              <span key={name} className="text-sm font-medium text-slate-400">{name}</span>
            ))}
          </div>

          <div className="border-t border-slate-800 pt-5 flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-white tracking-wide">WISHI</span>
              <span className="text-slate-600">|</span>
              <span className="text-xs text-slate-500">A smarter way to buy</span>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-500">
              <Link href="/terms" className="hover:text-sky-400 transition">Terms</Link>
              <Link href="/privacy" className="hover:text-sky-400 transition">Privacy</Link>
              <Link href="/help" className="hover:text-sky-400 transition">Help</Link>
              <Link href="/sitemap" className="hover:text-sky-400 transition">Sitemap</Link>
            </div>
            <p className="text-xs text-slate-600">All rights reserved &copy; 2026 WISHI</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
