/**
 * Generate PNG icons from SVG for full PWA compatibility.
 *
 * Usage: node scripts/generate-icons.js
 *
 * Requires the `sharp` package: npm install sharp --save-dev
 * If sharp is not available, SVG icons are used directly.
 */
const fs = require('fs')
const path = require('path')

const publicDir = path.join(__dirname, '..', 'public')
const svgSource = path.join(publicDir, 'icon-512x512.svg')

async function generate() {
  let sharp
  try {
    sharp = require('sharp')
  } catch {
    console.log('sharp not installed — SVG icons will be used directly.')
    console.log('For PNG generation: npm install sharp --save-dev')
    console.log('Then re-run: node scripts/generate-icons.js')
    return
  }

  const svgBuffer = fs.readFileSync(svgSource)

  const sizes = [
    { name: 'icon-192x192.png', size: 192 },
    { name: 'icon-512x512.png', size: 512 },
    { name: 'apple-touch-icon.png', size: 180 },
    { name: 'favicon-32x32.png', size: 32 },
    { name: 'favicon-16x16.png', size: 16 },
  ]

  for (const { name, size } of sizes) {
    await sharp(svgBuffer)
      .resize(size, size)
      .png()
      .toFile(path.join(publicDir, name))
    console.log(`Created ${name} (${size}x${size})`)
  }

  // Also create ICO from 32x32 PNG (just copy as favicon.ico for basic compat)
  await sharp(svgBuffer)
    .resize(32, 32)
    .png()
    .toFile(path.join(publicDir, 'favicon.ico'))
  console.log('Created favicon.ico')

  console.log('\nAll PNG icons generated successfully!')
}

generate().catch(console.error)
