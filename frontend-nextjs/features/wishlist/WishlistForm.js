'use client'

import { useState, useRef, useEffect } from 'react'
import { ChevronDown, ChevronLeft, Car, Smartphone, Home, Shirt, Sofa, Check, Search, MapPin, Store, Bike, Monitor, Camera, Headphones, Key, Building2, LandPlot, BedDouble, ShoppingBag, Baby, Watch, Armchair, WashingMachine, PaintBucket, CookingPot } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { CATEGORIES, CATEGORY_LIST, getSubcategories, getFields } from './wishlistFieldConfig'
import { MARKETPLACE_SOURCES } from './mockMatches'

const inputClass = 'w-full border-0 border-b border-gray-200 bg-transparent px-0 py-2 text-sm text-slate-900 placeholder:text-slate-300 focus:outline-none focus:border-sky-500 transition-colors'
const selectClass = 'w-full appearance-none border-0 border-b border-gray-200 bg-transparent px-0 py-2 text-sm text-slate-900 focus:outline-none focus:border-sky-500 transition-colors pr-6'

const categoryIcons = { Automobile: Car, Electronics: Smartphone, 'Real Estate': Home, Fashion: Shirt, 'Home & Living': Sofa }

const categorySubtitles = {
  Automobile: 'Car, Bike, Scooter',
  Electronics: 'Phones, Laptops, Gadgets',
  'Real Estate': 'Rent, Buy, Plot',
  Fashion: 'Men, Women, Kids',
  'Home & Living': 'Furniture, Decor, Kitchen',
}

const subcategoryIcons = {
  Car, Bike, Scooter: Bike,
  Mobile: Smartphone, Laptop: Monitor, TV: Monitor, Camera, Audio: Headphones,
  Buy: Home, Rent: Key, Plot: LandPlot, PG: BedDouble, Commercial: Building2,
  Men: Shirt, Women: ShoppingBag, Kids: Baby, Watches: Watch,
  Furniture: Armchair, Appliances: WashingMachine, Decor: PaintBucket, Kitchen: CookingPot,
}

const stepVariants = {
  enter: (d) => ({ x: d > 0 ? 60 : -60, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (d) => ({ x: d > 0 ? -60 : 60, opacity: 0 }),
}

const stagger = { hidden: {}, show: { transition: { staggerChildren: 0.04 } } }
const fadeUp = { hidden: { opacity: 0, y: 12 }, show: { opacity: 1, y: 0 } }

function formatPrice(value, unit) {
  if (!value && value !== 0) return `${unit}0`
  return `${unit}${Number(value).toLocaleString('en-IN')}`
}

// ── Step Indicator ──
function StepIndicator({ step }) {
  const labels = ['Category', 'Subcategory', 'Details']
  return (
    <div className="flex items-center justify-center gap-0 mb-8">
      {labels.map((label, i) => {
        const s = i + 1
        const done = step > s
        const active = step === s
        return (
          <div key={label} className="flex items-center">
            {i > 0 && (
              <div className={`w-8 sm:w-12 h-px mx-1 transition-colors ${done ? 'bg-sky-500' : 'bg-gray-200'}`} />
            )}
            <div className="flex flex-col items-center gap-1.5">
              <div className={`w-2.5 h-2.5 rounded-full transition-colors ${done ? 'bg-sky-500' : active ? 'bg-sky-500 ring-4 ring-sky-100' : 'bg-gray-200'}`} />
              <span className={`text-[11px] ${active ? 'text-sky-600 font-medium' : 'text-slate-400'}`}>{label}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

// ── Field Components ──
function Field({ label, children, required }) {
  return (
    <div>
      <label className="block text-[13px] font-medium text-slate-600 mb-1">
        {label}{required && <span className="text-sky-500 ml-0.5">*</span>}
      </label>
      {children}
    </div>
  )
}

function TextField({ field, value, onChange }) {
  return (
    <Field label={field.label} required={field.required}>
      <input
        type={field.type === 'number' ? 'number' : 'text'}
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={field.placeholder || ''}
        className={inputClass}
        min={field.type === 'number' ? 0 : undefined}
      />
    </Field>
  )
}

function SelectField({ field, value, onChange, formFields }) {
  let options = field.options || []
  let disabled = false

  if (field.dependsOn && field.optionsByParent) {
    const parentVal = formFields?.[field.dependsOn]
    if (parentVal && field.optionsByParent[parentVal]) {
      options = field.optionsByParent[parentVal]
    } else {
      options = []
      disabled = true
    }
  }

  return (
    <Field label={field.label} required={field.required}>
      <div className="relative">
        <select
          value={options.includes(value) ? value : ''}
          onChange={(e) => onChange(e.target.value)}
          className={`${selectClass} ${disabled ? 'text-slate-300' : ''}`}
          disabled={disabled}
        >
          <option value="">{disabled ? `Select ${field.dependsOn} first` : 'Select'}</option>
          {options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
        </select>
        <ChevronDown className="absolute right-0 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300 pointer-events-none" />
      </div>
    </Field>
  )
}

function SliderField({ field, value, onChange }) {
  const val = value ?? field.min
  return (
    <Field label={field.label}>
      <div className="pt-1">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-400">{formatPrice(field.min, field.unit)}</span>
          <span className="text-sm font-medium text-sky-600">{formatPrice(val, field.unit)}</span>
          <span className="text-xs text-slate-400">{formatPrice(field.max, field.unit)}</span>
        </div>
        <input
          type="range"
          min={field.min}
          max={field.max}
          step={field.step}
          value={val}
          onChange={(e) => onChange(Number(e.target.value))}
          className="wishi-slider"
        />
      </div>
    </Field>
  )
}

function ToggleField({ field, value, onChange }) {
  const checked = !!value
  return (
    <div className="flex items-center justify-between py-2">
      <span className="text-sm text-slate-700">{field.label}</span>
      <button
        type="button"
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${checked ? 'bg-sky-600' : 'bg-gray-200'}`}
      >
        <span className={`inline-block h-4 w-4 transform rounded-full bg-white shadow-sm transition-transform ${checked ? 'translate-x-6' : 'translate-x-1'}`} />
      </button>
    </div>
  )
}

function AutocompleteField({ field, value, onChange }) {
  const [query, setQuery] = useState(value || '')
  const [open, setOpen] = useState(false)
  const [focused, setFocused] = useState(-1)
  const wrapRef = useRef(null)
  const listRef = useRef(null)

  const filtered = query
    ? field.options.filter((o) => o.toLowerCase().includes(query.toLowerCase())).slice(0, 8)
    : field.options.slice(0, 8)

  useEffect(() => {
    function handleClick(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  useEffect(() => {
    setQuery(value || '')
  }, [value])

  const select = (val) => {
    onChange(val)
    setQuery(val)
    setOpen(false)
    setFocused(-1)
  }

  const handleKey = (e) => {
    if (!open) return
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setFocused((f) => Math.min(f + 1, filtered.length - 1))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setFocused((f) => Math.max(f - 1, 0))
    } else if (e.key === 'Enter' && focused >= 0) {
      e.preventDefault()
      select(filtered[focused])
    } else if (e.key === 'Escape') {
      setOpen(false)
    }
  }

  return (
    <Field label={field.label} required={field.required}>
      <div ref={wrapRef} className="relative">
        <div className="relative">
          <MapPin className="absolute left-0 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-300" />
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value)
              setOpen(true)
              setFocused(-1)
              if (!e.target.value) onChange('')
            }}
            onFocus={() => setOpen(true)}
            onKeyDown={handleKey}
            placeholder={field.placeholder || 'Search city...'}
            className={`${inputClass} pl-5`}
            autoComplete="off"
          />
          <Search className="absolute right-0 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-300" />
        </div>

        {open && filtered.length > 0 && (
          <div
            ref={listRef}
            className="absolute z-20 left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg max-h-48 overflow-y-auto"
          >
            {filtered.map((city, i) => (
              <button
                key={city}
                type="button"
                onMouseDown={() => select(city)}
                className={`w-full text-left px-3 py-2.5 text-sm transition-colors flex items-center gap-2 ${
                  i === focused ? 'bg-sky-50 text-sky-700' : 'text-slate-700 hover:bg-gray-50'
                } ${city === value ? 'font-medium text-sky-600' : ''}`}
              >
                <MapPin className="w-3 h-3 text-slate-300 flex-shrink-0" />
                {city}
              </button>
            ))}
          </div>
        )}

        {open && query && filtered.length === 0 && (
          <div className="absolute z-20 left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg px-3 py-3 text-sm text-slate-400">
            No cities found
          </div>
        )}
      </div>
    </Field>
  )
}

function renderField(field, value, onChange, formFields) {
  switch (field.type) {
    case 'text':
    case 'number':
      return <TextField key={field.name} field={field} value={value} onChange={onChange} />
    case 'select':
      return <SelectField key={field.name} field={field} value={value} onChange={onChange} formFields={formFields} />
    case 'slider':
      return <SliderField key={field.name} field={field} value={value} onChange={onChange} />
    case 'toggle':
      return <ToggleField key={field.name} field={field} value={value} onChange={onChange} />
    case 'autocomplete':
      return <AutocompleteField key={field.name} field={field} value={value} onChange={onChange} />
    default:
      return null
  }
}

// ── Main Form ──
export default function WishlistForm({ onSubmit }) {
  const [step, setStep] = useState(1)
  const [direction, setDirection] = useState(1)
  const [notes, setNotes] = useState('')
  const [preferredMarketplaces, setPreferredMarketplaces] = useState([])
  const [formData, setFormData] = useState({ category: '', subcategory: '', fields: {} })

  const goNext = () => { setDirection(1); setStep((s) => s + 1) }
  const goBack = () => {
    setDirection(-1)
    if (step === 3) {
      setFormData((d) => ({ ...d, fields: {} }))
      setNotes('')
      setPreferredMarketplaces([])
    }
    if (step === 2) {
      setFormData((d) => ({ ...d, subcategory: '', fields: {} }))
      setNotes('')
      setPreferredMarketplaces([])
    }
    setStep((s) => s - 1)
  }

  const selectCategory = (cat) => {
    setFormData({ category: cat, subcategory: '', fields: {} })
    setNotes('')
    setPreferredMarketplaces([])
    setDirection(1)
    setStep(2)
  }

  const selectSubcategory = (sub) => {
    setFormData((d) => ({ ...d, subcategory: sub, fields: {} }))
    setNotes('')
    setPreferredMarketplaces([])
    setDirection(1)
    setStep(3)
  }

  const updateField = (name, value) => {
    setFormData((d) => {
      const updated = { ...d.fields, [name]: value }
      // Clear dependent fields when parent changes
      const config = getFields(d.category, d.subcategory)
      config.forEach((f) => {
        if (f.dependsOn === name) {
          updated[f.name] = ''
        }
      })
      return { ...d, fields: updated }
    })
  }

  const fieldConfig = getFields(formData.category, formData.subcategory)
  const requiredFilled = fieldConfig.filter((f) => f.required).every((f) => {
    const v = formData.fields[f.name]
    return v !== undefined && v !== ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!requiredFilled) return
    const fields = { ...formData.fields }
    if (notes.trim()) fields.notes = notes.trim()
    onSubmit({ category: formData.category, subcategory: formData.subcategory, fields, preferredMarketplaces })
    setFormData({ category: '', subcategory: '', fields: {} })
    setNotes('')
    setPreferredMarketplaces([])
    setStep(1)
  }

  // Separate toggles from other fields
  const regularFields = fieldConfig.filter((f) => f.type !== 'toggle')
  const toggleFields = fieldConfig.filter((f) => f.type === 'toggle')

  return (
    <form onSubmit={handleSubmit} className="relative min-h-[420px] pb-24">
      <StepIndicator step={step} />

      <AnimatePresence mode="wait" custom={direction}>
        {/* ── Step 1: Category ── */}
        {step === 1 && (
          <motion.div
            key="step1"
            custom={direction}
            variants={stepVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
          >
            <div className="text-center mb-8">
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900">Create Wishlist</h2>
              <p className="mt-1 text-sm text-slate-400">Select a category to start wishing:</p>
            </div>
            <motion.div className="grid grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-4 max-w-lg mx-auto" variants={stagger} initial="hidden" animate="show">
              {CATEGORY_LIST.map((cat) => {
                const Icon = categoryIcons[cat] || Car
                const active = formData.category === cat
                return (
                  <motion.button
                    key={cat}
                    type="button"
                    variants={fadeUp}
                    whileTap={{ scale: 0.97 }}
                    onClick={() => selectCategory(cat)}
                    className={`flex flex-col items-center text-center rounded-2xl px-3 py-5 sm:py-6 transition-all shadow-sm ${
                      active
                        ? 'bg-gradient-to-b from-sky-50 to-white border-2 border-sky-300 shadow-lg shadow-sky-100/50'
                        : 'bg-white border border-gray-100 hover:border-gray-200 hover:shadow-md'
                    }`}
                  >
                    <div className={`w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mb-3 ${
                      active ? 'bg-sky-100' : 'bg-gray-50'
                    }`}>
                      <Icon className={`w-7 h-7 sm:w-8 sm:h-8 ${active ? 'text-sky-500' : 'text-slate-400'}`} />
                    </div>
                    <span className={`text-sm font-bold ${active ? 'text-sky-700' : 'text-slate-800'}`}>{cat}</span>
                    <span className="text-[11px] text-slate-400 mt-0.5">{categorySubtitles[cat]}</span>
                  </motion.button>
                )
              })}
            </motion.div>
          </motion.div>
        )}

        {/* ── Step 2: Subcategory ── */}
        {step === 2 && (
          <motion.div
            key="step2"
            custom={direction}
            variants={stepVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
          >
            <button type="button" onClick={goBack} className="flex items-center gap-1 text-xs text-sky-600 mb-4 hover:text-sky-700 transition">
              <ChevronLeft className="w-3.5 h-3.5" />
              {formData.category}
            </button>
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 text-center mb-6">Select Sub-Category</h2>
            <motion.div className="space-y-3 max-w-md mx-auto" variants={stagger} initial="hidden" animate="show">
              {getSubcategories(formData.category).map((sub) => {
                const active = formData.subcategory === sub
                const SubIcon = subcategoryIcons[sub] || categoryIcons[formData.category] || Car
                return (
                  <motion.button
                    key={sub}
                    type="button"
                    variants={fadeUp}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => selectSubcategory(sub)}
                    className={`flex items-center gap-4 w-full rounded-2xl px-5 py-4 text-left transition-all shadow-sm ${
                      active
                        ? 'bg-gradient-to-r from-sky-500/15 via-sky-400/5 to-transparent border border-sky-200 shadow-md'
                        : 'bg-white border border-gray-100 hover:border-gray-200 hover:shadow-md'
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                      active ? 'bg-sky-500 shadow-lg shadow-sky-500/30' : 'bg-gray-100'
                    }`}>
                      <SubIcon className={`w-5 h-5 ${active ? 'text-white' : 'text-slate-400'}`} />
                    </div>
                    <span className={`text-sm font-semibold ${active ? 'text-sky-700' : 'text-slate-700'}`}>{sub}</span>
                  </motion.button>
                )
              })}
            </motion.div>
          </motion.div>
        )}

        {/* ── Step 3: Dynamic Fields ── */}
        {step === 3 && (
          <motion.div
            key="step3"
            custom={direction}
            variants={stepVariants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
          >
            <button type="button" onClick={goBack} className="flex items-center gap-1 text-xs text-sky-600 mb-1 hover:text-sky-700 transition">
              <ChevronLeft className="w-3.5 h-3.5" />
              {formData.category}
            </button>
            <p className="text-lg font-semibold text-slate-900 mb-6">{formData.subcategory}</p>

            <div className="grid gap-6 sm:grid-cols-2">
              {regularFields.map((field) =>
                renderField(field, formData.fields[field.name], (val) => updateField(field.name, val), formData.fields)
              )}
            </div>

            {toggleFields.length > 0 && (
              <div className="mt-6 pt-4 border-t border-gray-100 space-y-1">
                <p className="text-[13px] font-medium text-slate-600 mb-2">Amenities</p>
                {toggleFields.map((field) =>
                  renderField(field, formData.fields[field.name], (val) => updateField(field.name, val), formData.fields)
                )}
              </div>
            )}

            <div className="mt-6 pt-4 border-t border-gray-100">
              <Field label="Notes">
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Anything else you'd like to mention..."
                  rows={2}
                  className={`${inputClass} resize-none`}
                />
              </Field>
            </div>

            {/* Preferred Marketplaces */}
            {formData.category && MARKETPLACE_SOURCES[formData.category] && (
              <div className="mt-6 pt-4 border-t border-gray-100">
                <div className="flex items-center gap-2 mb-3">
                  <Store className="w-4 h-4 text-slate-400" />
                  <span className="text-[13px] font-medium text-slate-600">Preferred Marketplaces</span>
                  <span className="text-[11px] text-slate-400">(optional)</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {MARKETPLACE_SOURCES[formData.category].map((src) => {
                    const selected = preferredMarketplaces.includes(src.name)
                    return (
                      <button
                        key={src.name}
                        type="button"
                        onClick={() => {
                          setPreferredMarketplaces((prev) =>
                            selected ? prev.filter((n) => n !== src.name) : [...prev, src.name]
                          )
                        }}
                        className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium border transition-all ${
                          selected
                            ? 'border-sky-500 bg-sky-50 text-sky-700'
                            : 'border-gray-200 text-slate-500 hover:border-gray-300'
                        }`}
                      >
                        <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: src.color }} />
                        {src.name}
                        {selected && <Check className="w-3 h-3" />}
                      </button>
                    )
                  })}
                </div>
                {preferredMarketplaces.length === 0 && (
                  <p className="text-[11px] text-slate-300 mt-2">All marketplaces will be searched if none selected</p>
                )}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Fixed Bottom Bar ── */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-sm border-t border-gray-100 px-4 py-4 z-10">
        <div className="max-w-2xl mx-auto flex gap-3">
          {step > 1 && (
            <button
              type="button"
              onClick={goBack}
              className="flex-1 rounded-full bg-gradient-to-r from-slate-100 to-slate-200 hover:from-slate-200 hover:to-slate-300 px-5 py-3 text-sm font-semibold text-slate-600 transition-all active:scale-[0.98]"
            >
              Back
            </button>
          )}
          {step === 3 && (
            <button
              type="submit"
              disabled={!requiredFilled}
              className={`flex-1 rounded-full py-3 text-sm font-semibold text-white transition-all active:scale-[0.98] ${
                requiredFilled
                  ? 'bg-gradient-to-r from-sky-500 to-violet-500 hover:from-sky-600 hover:to-violet-600 shadow-lg shadow-violet-500/25'
                  : 'bg-gradient-to-r from-sky-300 to-violet-300 cursor-not-allowed'
              }`}
            >
              Create Wishlist
            </button>
          )}
        </div>
      </div>
    </form>
  )
}
