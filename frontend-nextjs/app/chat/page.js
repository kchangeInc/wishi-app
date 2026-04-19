'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, Send, User, Sparkles, ArrowRight, RotateCcw } from 'lucide-react'
import Link from 'next/link'

const WISHI_KNOWLEDGE = {
  greeting: "Hi! I'm WISHI AI — your smart buying assistant. I can help you with creating wishlists, understanding how WISHI works, finding categories, and more. What would you like to know?",

  responses: [
    {
      keywords: ['what is wishi', 'about wishi', 'what does wishi do', 'tell me about', 'about this', 'what is this'],
      answer: "**WISHI** is a demand-first marketplace platform. Instead of browsing hundreds of listings, you simply tell us what you want — and we find matches from OLX, Amazon, Flipkart, 99acres, Cars24, and more.\n\nWe flip the traditional marketplace model: **you describe, we deliver.**\n\n[Learn more → /about](/about)",
    },
    {
      keywords: ['how it works', 'how does it work', 'how to use', 'steps', 'process'],
      answer: "WISHI works in **4 simple steps**:\n\n1. **Tell us what you want** — Create a wishlist with your preferences\n2. **We find matches** — Our system scans multiple marketplaces\n3. **Get real-time updates** — Receive alerts when new matches appear\n4. **Click and connect** — Visit the seller directly on their platform\n\n[See full guide → /how-it-works](/how-it-works)",
    },
    {
      keywords: ['create wishlist', 'new wishlist', 'make a wish', 'how to create', 'start wishlist'],
      answer: "To create a wishlist:\n\n1. Go to the **Wishlist** page\n2. Pick a **category** (Automobile, Electronics, Real Estate, Fashion, Home & Living)\n3. Select a **subcategory** (e.g., Car, Laptop, Rent)\n4. Fill in your **preferences** (brand, budget, location, etc.)\n5. Click **Create Wishlist**\n\nWe'll start finding matches immediately!\n\n[Create now → /wishlist](/wishlist)",
    },
    {
      keywords: ['categories', 'category', 'what can i search', 'what can i find', 'types'],
      answer: "WISHI supports **5 categories**:\n\n🚗 **Automobile** — Car, Bike, Scooter, Truck, Bus\n📱 **Electronics** — Mobile, Laptop, TV, Camera\n🏠 **Real Estate** — Rent, Buy, PG/Hostel, Plot\n👕 **Fashion** — Men, Women, Kids\n🛋️ **Home & Living** — Furniture, Appliances, Decor\n\nEach has detailed filters like brand, model, price, location, and more.",
    },
    {
      keywords: ['automobile', 'car', 'bike', 'scooter', 'vehicle', 'truck'],
      answer: "In the **Automobile** category you can find:\n\n- **Cars** — Maruti, Hyundai, Tata, Honda, Toyota, BMW, etc.\n- **Bikes** — Royal Enfield, Honda, Hero, Bajaj, KTM, etc.\n- **Scooters** — Activa, Jupiter, Ola, Ather, etc.\n- **Trucks & Buses**\n\nFilters include brand, model, year, fuel type, owners, and budget.\n\n[Create auto wishlist → /wishlist](/wishlist)",
    },
    {
      keywords: ['electronics', 'mobile', 'phone', 'laptop', 'tv', 'camera'],
      answer: "In the **Electronics** category:\n\n- **Mobiles** — Apple, Samsung, OnePlus, Xiaomi, Google, etc.\n- **Laptops** — MacBook, Dell, HP, Lenovo, Asus, etc.\n- **TVs** — Samsung, LG, Sony, OLED/QLED\n- **Cameras** — Canon, Sony, Nikon, GoPro\n\nFilter by brand, storage, RAM, condition, and budget.\n\n[Create electronics wishlist → /wishlist](/wishlist)",
    },
    {
      keywords: ['real estate', 'rent', 'buy', 'house', 'flat', 'apartment', 'pg', 'plot', 'property'],
      answer: "In **Real Estate** you can search for:\n\n- **Rent** — 1-4+ BHK, furnished options, with parking/lift\n- **Buy** — Apartments, villas, independent houses\n- **PG/Hostel** — Single/double rooms, food, AC options\n- **Plots** — Residential, commercial, agricultural\n\nFilter by city, pincode, BHK, budget, and amenities.\n\n[Create property wishlist → /wishlist](/wishlist)",
    },
    {
      keywords: ['fashion', 'clothes', 'clothing', 'shoes', 'men', 'women', 'kids'],
      answer: "The **Fashion** category covers:\n\n- **Men** — Shirts, T-shirts, Jeans, Shoes, Watches\n- **Women** — Dresses, Sarees, Kurtis, Bags, Jewelry\n- **Kids** — Clothing, Shoes, School Bags\n\nBrands include Nike, Zara, Levi's, FabIndia, and more.\n\n[Create fashion wishlist → /wishlist](/wishlist)",
    },
    {
      keywords: ['home', 'furniture', 'appliance', 'sofa', 'bed', 'decor', 'living'],
      answer: "In **Home & Living**:\n\n- **Furniture** — Sofa, Bed, Dining Table, Wardrobe, Desk\n- **Appliances** — Refrigerator, Washing Machine, AC, Microwave\n- **Decor** — Wall Art, Rugs, Curtains, Lamps\n\nFilter by material, brand, condition, and budget.\n\n[Create home wishlist → /wishlist](/wishlist)",
    },
    {
      keywords: ['marketplace', 'where', 'source', 'olx', 'amazon', 'flipkart'],
      answer: "WISHI aggregates listings from **9+ marketplaces**:\n\n🛒 **General** — OLX, Amazon, Flipkart\n🚗 **Auto** — CarDekho, Cars24\n🏠 **Property** — 99acres, MagicBricks\n👕 **Fashion** — Myntra\n🛋️ **Home** — Pepperfry\n\nYou can set **preferred marketplaces** when creating a wishlist, and filter matches by source.",
    },
    {
      keywords: ['price', 'cost', 'free', 'payment', 'pay', 'charge'],
      answer: "**WISHI is completely free!** 🎉\n\nCreating wishlists and receiving matches costs nothing. WISHI is a **discovery platform** — when you find a match, you're redirected to the original marketplace to deal with the seller directly.\n\nWe do not handle any payments or transactions.",
    },
    {
      keywords: ['match', 'matches', 'result', 'found'],
      answer: "When you create a wishlist, WISHI finds **matching listings** from multiple marketplaces based on your preferences.\n\nOn the matches page you can:\n- **Filter** by marketplace\n- **Sort** by relevance, price, or favourites\n- **Favourite** matches you like (heart icon)\n- **Remove** matches you don't want (X icon)\n- **Click through** to the seller's listing",
    },
    {
      keywords: ['expiry', 'expire', 'how long', 'duration', 'active'],
      answer: "Each wishlist stays **active for 30 days** from creation. You'll see the expiry date on your wishlist card.\n\n- 🟢 More than 7 days left — regular\n- 🟡 Less than 7 days — amber warning\n- 🔴 Expired — you'll need to create a new one\n\nYou'll get a notification before your wishlist expires.",
    },
    {
      keywords: ['notification', 'alert', 'notify', 'updates'],
      answer: "WISHI sends you notifications for:\n\n- 📦 **New matches** found for your wishlists\n- 💰 **Price drops** on matches\n- ⏰ **Expiry reminders** for your wishlists\n- ❤️ **Updates** on favourited items\n\nCheck them anytime at the **bell icon** in the header.\n\n[View notifications → /notifications](/notifications)",
    },
    {
      keywords: ['login', 'signup', 'sign in', 'register', 'account', 'google'],
      answer: "WISHI uses **Google Sign-In** for quick, secure authentication.\n\n- No passwords to remember\n- One-click signup with your Google account\n- Your data stays secure\n\nClick **Signup** in the header to get started!",
    },
    {
      keywords: ['privacy', 'data', 'secure', 'safe', 'information'],
      answer: "Your privacy is important to us:\n\n✅ Minimal data collection\n✅ Google Sign-In for secure auth\n✅ No selling personal data\n❌ No third-party tracking\n❌ No storing payment info\n\n[Read Privacy Policy → /privacy](/privacy)",
    },
    {
      keywords: ['terms', 'legal', 'rules', 'policy'],
      answer: "Key points from our Terms of Use:\n\n1. WISHI is a **discovery platform**, not a direct seller\n2. Users are responsible for verifying sellers\n3. We are not liable for third-party transactions\n4. Listings come from external marketplace sources\n\n[Read Terms → /terms](/terms)\n[Read Privacy Policy → /privacy](/privacy)",
    },
    {
      keywords: ['help', 'support', 'contact', 'issue', 'problem'],
      answer: "Need help? Here are your options:\n\n📧 **Email** — support@wishi.in\n🤖 **AI Chat** — You're already here!\n📋 **Help Center** — Browse FAQs and guides\n\n[Visit Help & Support → /help](/help)",
    },
    {
      keywords: ['favourite', 'favorite', 'save', 'heart', 'like'],
      answer: "You can **favourite** any match by clicking the ❤️ heart icon on the match card.\n\n- Favourites are saved per wishlist\n- Use **\"Favourites First\"** sort to see them at the top\n- Favourited count is shown next to the sort bar\n- You'll get alerts if a favourited item's price drops",
    },
    {
      keywords: ['location', 'city', 'where', 'area'],
      answer: "WISHI supports **150+ Indian cities** including Mumbai, Delhi, Bangalore, Chennai, Hyderabad, Pune, Kolkata, Jaipur, and many more.\n\nYou can:\n- Set your **location** in the header\n- Specify **city** in your wishlist\n- Search with **location context**\n\nLocation helps us find the most relevant local matches for you.",
    },
    {
      keywords: ['hi', 'hello', 'hey', 'good morning', 'good evening', 'hola'],
      answer: "Hello! 👋 Welcome to WISHI AI.\n\nI can help you with:\n- 📋 Creating wishlists\n- 🔍 Understanding categories\n- 🏪 Marketplace info\n- ❓ FAQs and support\n\nWhat would you like to know?",
    },
    {
      keywords: ['thank', 'thanks', 'thx', 'ty'],
      answer: "You're welcome! Happy to help. 😊\n\nIf you have more questions, just ask. Or you can:\n\n[Create a wishlist → /wishlist](/wishlist)\n[Browse help articles → /help](/help)",
    },
  ],

  fallback: "I'm not sure about that, but I can help with wishlists, categories, marketplaces, notifications, pricing, and more.\n\nTry asking me:\n- \"How does WISHI work?\"\n- \"What categories are available?\"\n- \"How do I create a wishlist?\"\n- \"Is WISHI free?\"\n\nOr visit our [Help & Support → /help](/help) page.",
}

function getResponse(input) {
  const lower = input.toLowerCase().trim()
  for (const item of WISHI_KNOWLEDGE.responses) {
    if (item.keywords.some((kw) => lower.includes(kw))) {
      return item.answer
    }
  }
  return WISHI_KNOWLEDGE.fallback
}

const quickQuestions = [
  'What is WISHI?',
  'How does it work?',
  'What categories are available?',
  'Is WISHI free?',
  'How to create a wishlist?',
  'Which marketplaces do you support?',
]

export default function ChatPage() {
  const [messages, setMessages] = useState([
    { id: 'greeting', role: 'bot', text: WISHI_KNOWLEDGE.greeting, time: Date.now() },
  ])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  const sendMessage = (text) => {
    if (!text.trim()) return

    const userMsg = { id: `u-${Date.now()}`, role: 'user', text: text.trim(), time: Date.now() }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsTyping(true)

    // Simulate typing delay
    setTimeout(() => {
      const response = getResponse(text)
      const botMsg = { id: `b-${Date.now()}`, role: 'bot', text: response, time: Date.now() }
      setMessages((prev) => [...prev, botMsg])
      setIsTyping(false)
    }, 600 + Math.random() * 800)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(input)
  }

  const resetChat = () => {
    setMessages([
      { id: 'greeting', role: 'bot', text: WISHI_KNOWLEDGE.greeting, time: Date.now() },
    ])
  }

  // Simple markdown-like rendering for bold and links
  const renderText = (text) => {
    const parts = text.split(/(\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\)|\n)/g)
    return parts.map((part, i) => {
      if (part === '\n') return <br key={i} />
      const boldMatch = part.match(/^\*\*(.+)\*\*$/)
      if (boldMatch) return <strong key={i} className="font-semibold text-slate-900">{boldMatch[1]}</strong>
      const linkMatch = part.match(/^\[(.+)\]\((.+)\)$/)
      if (linkMatch) {
        const [, label, href] = linkMatch
        const cleanLabel = label.replace(/→.*$/, '').trim()
        const cleanHref = href.replace(/\)$/, '')
        return (
          <Link key={i} href={cleanHref} className="inline-flex items-center gap-1 text-sky-600 hover:text-sky-700 font-medium underline-offset-2 hover:underline">
            {cleanLabel} <ArrowRight className="w-3 h-3 inline" />
          </Link>
        )
      }
      return part
    })
  }

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <div className="flex-1 flex flex-col max-w-3xl mx-auto w-full px-4 sm:px-6">
        {/* Chat Header */}
        <div className="flex items-center justify-between py-5 border-b border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-violet-600 flex items-center justify-center shadow-lg">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-900">WISHI AI</h1>
              <div className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-xs text-slate-400">Online — Ask me anything about WISHI</span>
              </div>
            </div>
          </div>
          <button
            onClick={resetChat}
            className="p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-gray-50 transition"
            title="Reset chat"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto py-6 space-y-4 min-h-0" style={{ maxHeight: 'calc(100vh - 320px)' }}>
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  msg.role === 'bot'
                    ? 'bg-gradient-to-br from-sky-500 to-violet-600'
                    : 'bg-slate-900'
                }`}>
                  {msg.role === 'bot'
                    ? <Sparkles className="w-4 h-4 text-white" />
                    : <User className="w-4 h-4 text-white" />
                  }
                </div>

                {/* Bubble */}
                <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === 'bot'
                    ? 'bg-gray-50 border border-gray-100'
                    : 'bg-sky-600 text-white'
                }`}>
                  <div className={`text-sm leading-relaxed whitespace-pre-line ${
                    msg.role === 'bot' ? 'text-slate-600' : 'text-white'
                  }`}>
                    {msg.role === 'bot' ? renderText(msg.text) : msg.text}
                  </div>
                  <p className={`text-[10px] mt-1.5 ${
                    msg.role === 'bot' ? 'text-slate-300' : 'text-sky-200'
                  }`}>
                    {new Date(msg.time).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-500 to-violet-600 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <div className="bg-gray-50 border border-gray-100 rounded-2xl px-4 py-3">
                <div className="flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-slate-300 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 rounded-full bg-slate-300 animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 rounded-full bg-slate-300 animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Quick Questions */}
        {messages.length <= 1 && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="pb-4"
          >
            <p className="text-xs text-slate-400 mb-2">Quick questions:</p>
            <div className="flex flex-wrap gap-2">
              {quickQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => sendMessage(q)}
                  className="text-xs font-medium text-sky-600 bg-sky-50 hover:bg-sky-100 px-3 py-1.5 rounded-full transition"
                >
                  {q}
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Input Bar */}
        <div className="border-t border-gray-100 py-4">
          <form onSubmit={handleSubmit} className="flex items-center gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask WISHI AI anything..."
              className="flex-1 px-4 py-3 rounded-xl border border-gray-200 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition"
              disabled={isTyping}
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="w-11 h-11 rounded-xl bg-sky-600 hover:bg-sky-700 disabled:bg-gray-200 disabled:cursor-not-allowed flex items-center justify-center transition flex-shrink-0"
            >
              <Send className="w-4 h-4 text-white" />
            </button>
          </form>
          <p className="text-[10px] text-slate-300 text-center mt-2">
            WISHI AI can answer questions about our platform. For specific product queries, create a wishlist.
          </p>
        </div>
      </div>
    </div>
  )
}
