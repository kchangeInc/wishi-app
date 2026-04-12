'use client'

import { Briefcase, Code, Megaphone, HeartHandshake, Zap, Globe, Users, Rocket, ArrowRight, Mail } from 'lucide-react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import Header from '../../components/Header'
import Footer from '../../components/Footer'

const values = [
  { icon: Zap, title: 'Move Fast', description: 'Ship early, learn often. We value progress over perfection.', color: 'bg-amber-50 text-amber-600' },
  { icon: Users, title: 'User First', description: "Every decision starts with what's best for the people using WISHI.", color: 'bg-sky-50 text-sky-600' },
  { icon: Globe, title: 'Think Big', description: "We're building for millions of buyers across India and beyond.", color: 'bg-emerald-50 text-emerald-600' },
  { icon: HeartHandshake, title: 'Stay Kind', description: 'Kindness and respect are non-negotiable in how we work together.', color: 'bg-pink-50 text-pink-600' },
]

const openRoles = [
  { title: 'Full-Stack Engineer', team: 'Engineering', type: 'Full-time', location: 'Remote / India', icon: Code },
  { title: 'Product Designer', team: 'Design', type: 'Full-time', location: 'Remote / India', icon: Rocket },
  { title: 'Growth Marketer', team: 'Marketing', type: 'Full-time', location: 'Remote / India', icon: Megaphone },
  { title: 'Business Development', team: 'Operations', type: 'Full-time', location: 'Remote / India', icon: Briefcase },
]

const perks = [
  'Remote-first culture',
  'Competitive salary',
  'Health insurance',
  'Flexible hours',
  'Learning budget',
  'Team offsites',
]

const cardStagger = { hidden: {}, show: { transition: { staggerChildren: 0.06 } } }
const cardItem = { hidden: { opacity: 0, y: 16 }, show: { opacity: 1, y: 0, transition: { duration: 0.3 } } }

export default function CareersPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50/80 to-white">
        <div className="absolute top-10 -left-40 w-80 h-80 bg-sky-100/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 -right-40 w-80 h-80 bg-violet-100/30 rounded-full blur-3xl" />
        <div className="relative max-w-3xl mx-auto px-4 sm:px-6 pt-16 sm:pt-24 pb-12 sm:pb-16 text-center">
          <motion.p initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="text-sm uppercase tracking-[0.4em] text-sky-600 font-semibold">
            Careers
          </motion.p>
          <motion.h1 initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.1 }} className="mt-4 text-3xl sm:text-5xl font-bold tracking-tight text-slate-900">
            Join the <span className="text-sky-600">WISHI</span> Team
          </motion.h1>
          <motion.p initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.2 }} className="mt-6 text-base sm:text-lg text-slate-500 max-w-2xl mx-auto leading-relaxed">
            Help us build the future of demand-first marketplaces. We're looking for passionate people who want to change how India buys.
          </motion.p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 pb-16 sm:pb-20">

        {/* Values */}
        <section className="mb-12">
          <h2 className="text-center text-xl sm:text-2xl font-bold text-slate-900 mb-8">What We Believe In</h2>
          <motion.div className="grid gap-4 sm:grid-cols-2" variants={cardStagger} initial="hidden" animate="show">
            {values.map((v) => (
              <motion.div key={v.title} variants={cardItem} className="rounded-2xl border border-gray-100 p-5 hover:shadow-lg hover:border-gray-200 transition-all">
                <div className={`w-10 h-10 rounded-xl ${v.color} flex items-center justify-center mb-3`}>
                  <v.icon className="w-5 h-5" />
                </div>
                <h3 className="text-sm font-bold text-slate-900">{v.title}</h3>
                <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{v.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* Open Roles */}
        <section className="mb-12">
          <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-2">Open Positions</h2>
          <p className="text-sm text-slate-400 mb-6">Interested? Send your resume to <a href="mailto:careers@wishi.in" className="text-sky-600 hover:underline">careers@wishi.in</a></p>
          <motion.div className="space-y-3" variants={cardStagger} initial="hidden" animate="show">
            {openRoles.map((role) => (
              <motion.a
                key={role.title}
                href={`mailto:careers@wishi.in?subject=Application: ${role.title}`}
                variants={cardItem}
                className="group flex items-center gap-4 rounded-2xl border border-gray-100 p-4 hover:shadow-lg hover:border-gray-200 transition-all"
              >
                <div className="w-10 h-10 rounded-xl bg-sky-50 flex items-center justify-center flex-shrink-0">
                  <role.icon className="w-5 h-5 text-sky-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-semibold text-slate-900">{role.title}</h3>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-slate-400">{role.team}</span>
                    <span className="text-slate-200">|</span>
                    <span className="text-xs text-slate-400">{role.type}</span>
                    <span className="text-slate-200">|</span>
                    <span className="text-xs text-slate-400">{role.location}</span>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-300 group-hover:text-sky-500 transition flex-shrink-0" />
              </motion.a>
            ))}
          </motion.div>
        </section>

        {/* Perks */}
        <section className="mb-12">
          <h2 className="text-xl sm:text-2xl font-bold text-slate-900 mb-6">Why Join Us</h2>
          <div className="rounded-2xl border border-gray-100 p-6">
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {perks.map((perk) => (
                <div key={perk} className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-sky-500 flex-shrink-0" />
                  <span className="text-sm text-slate-600">{perk}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4, delay: 0.5 }} className="rounded-2xl bg-gradient-to-br from-sky-600 via-sky-500 to-indigo-600 p-8 sm:p-10 text-center relative overflow-hidden">
          <div className="absolute inset-0 opacity-10 bg-[radial-gradient(circle_at_top_left,_rgba(255,255,255,0.4),_transparent_40%)]" />
          <div className="relative">
            <h2 className="text-2xl sm:text-3xl font-bold text-white">Ready to make an impact?</h2>
            <p className="mt-3 text-sm sm:text-base text-white/80 max-w-lg mx-auto">
              Send your resume and a short intro about yourself.
            </p>
            <div className="mt-6">
              <a
                href="mailto:careers@wishi.in"
                className="rounded-full bg-white text-sky-600 hover:bg-sky-50 px-8 py-3.5 text-sm font-semibold transition shadow-lg inline-flex items-center gap-2"
              >
                <Mail className="w-4 h-4" />
                careers@wishi.in
              </a>
            </div>
          </div>
        </motion.div>
      </div>

      <Footer />
    </div>
  )
}
