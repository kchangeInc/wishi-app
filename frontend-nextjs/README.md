# WISHI Frontend

A Pinterest-inspired, mobile-first PWA for the AI-powered deal marketplace.

## Features

- 🎨 **Pinterest-style Design**: Masonry layout with beautiful card animations
- 📱 **Mobile-First PWA**: Installable app with offline capabilities
- ⚡ **Lightning Fast**: Optimized for speed with limited animations
- 🎯 **Responsive**: Perfect on all devices from mobile to desktop
- 🎭 **Beautiful Animations**: Subtle, tasteful animations using Framer Motion
- 🛍️ **E-commerce Focused**: Wishlist creation and deal discovery

## Tech Stack

- **Next.js 14** - React framework with app router
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Masonry CSS** - Pinterest-style grid layout
- **Next PWA** - Progressive Web App support
- **Lucide React** - Beautiful icons

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Open http://localhost:3000
```

## PWA Features

- **Installable**: Add to home screen on mobile devices
- **Offline Ready**: Service worker for caching
- **Fast Loading**: Optimized bundle with code splitting
- **Native Feel**: Smooth animations and transitions

## Design Philosophy

- **Pinterest-inspired**: Masonry grid with hover effects
- **Minimal Animations**: Subtle bounce and fade effects
- **Color Palette**: Pinterest red (#E60023) with gradients
- **Typography**: System fonts for speed
- **Mobile-First**: Responsive design that works everywhere

## Component Structure

```
app/
├── layout.js          # Root layout with PWA meta tags
├── globals.css        # Tailwind + custom Pinterest styles
├── page.js           # Homepage with masonry grid
└── components/       # Reusable components
```

## Performance Optimizations

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js built-in optimization
- **CSS Optimization**: Tailwind purging and minification
- **Font Loading**: System fonts for instant loading
- **Bundle Analysis**: Optimized dependencies

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow the existing Pinterest-inspired design patterns
2. Use Tailwind classes for styling
3. Add subtle animations with Framer Motion
4. Ensure mobile responsiveness
5. Test PWA functionality

## Deployment

The app is configured for static export and can be deployed to:

- Vercel
- Netlify
- Any static hosting service
- Docker containers

```bash
# Build for production
npm run build

# Export static files (optional)
npm run export
```