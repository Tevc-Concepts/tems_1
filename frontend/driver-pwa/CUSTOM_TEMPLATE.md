# 🎨 TEMS Custom Template Architecture

## Overview

The TEMS Driver Portal now uses a **fully custom HTML template** instead of Frappe's default `templates/web.html`. This gives you complete control over branding, theme colors, loading experience, and mobile behavior.

## 🎯 Key Benefits

### 1. **No Frappe Template Dependencies**
- ❌ No more `{% extends "templates/web.html" %}`
- ✅ Pure standalone HTML with TEMS branding
- ✅ Complete control over meta tags, colors, and structure

### 2. **Mobile-First Theme Color**
- 🎨 `theme-color: #36454f` (Charcoal Gray) - visible in mobile browser chrome
- 📱 iOS status bar styling with `black-translucent`
- 💚 Proper PWA manifest integration

### 3. **Branded Loading Experience**
- 🌟 Custom neon green animated loader with glow effects
- 🗺️ Circuit-style TEMS map pin logo (animated pulse)
- ⚡ Smooth fade-out transition when app loads
- 🎭 Fallback timeout ensures loader never gets stuck

### 4. **Progressive Enhancement**
- 📦 Global TEMS theme CSS loaded first
- 🎨 PWA-specific styles layered on top
- 🚀 Service worker for offline capability
- ⚠️ Graceful `<noscript>` fallback

## 📁 File Structure

```
apps/tems/
├── www/driver/
│   └── index.html              # Custom standalone template (NOT Jinja)
├── public/css/
│   └── tems_theme.css          # Global TEMS theme (reusable)
└── frontend/driver-pwa/
    ├── dist/                   # Build output
    │   ├── assets/
    │   │   ├── index-*.css     # Hashed PWA styles
    │   │   └── index-*.js      # Hashed PWA bundle
    │   ├── manifest.webmanifest
    │   └── registerSW.js
    └── update-template.sh      # Auto-updates template with new hashes
```

## 🔄 Build Process

### Automatic Updates

When you run `npm run build` or `./build.sh`, the build process:

1. **Builds PWA** → Generates hashed assets (e.g., `index-Cs1EDRBj.css`)
2. **Extracts Hashes** → Reads filenames from `dist/index.html`
3. **Updates Template** → Regenerates custom `www/driver/index.html` with new asset paths
4. **Preserves Custom Code** → All loading animation, styles, and branding stay intact

### Manual Build Steps

```bash
cd /workspace/development/frappe-bench/apps/tems/frontend/driver-pwa

# Build the PWA
npm run build

# Update the template (auto-run by build.sh)
./update-template.sh

# Clear Frappe cache
cd /workspace/development/frappe-bench
bench --site tems.local clear-cache
bench --site tems.local clear-website-cache
```

## 🎨 Theme Colors

### Primary Colors
```css
--tems-neon-green: #39ff14;      /* Primary actions, accents, glow */
--tems-charcoal-gray: #36454f;   /* Backgrounds, structure, theme-color */
--tems-light-gray: #e0e2db;      /* Page background, subtle areas */
```

### Mobile Theme Color
```html
<meta name="theme-color" content="#36454f">
```
This makes the mobile browser chrome (address bar, status bar) match your charcoal brand color.

### iOS Status Bar
```html
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```
Provides an immersive experience with transparent status bar overlay.

## 🌟 Loading Screen

### Visual Design
```
┌─────────────────────────────┐
│                             │
│     [Circuit Map Pin]       │  ← Animated pulse (neon green)
│          ⚡                  │
│                             │
│     [Spinner Ring]          │  ← Rotating with glow
│                             │
│  Loading TEMS Driver        │  ← Text with neon shadow
│        Portal...            │
│                             │
└─────────────────────────────┘
Background: Charcoal gradient (135deg)
```

### Animation Behavior
1. **Page Load** → Loader visible with animations
2. **App Ready** → `window.load` event triggers fade-out (1s delay)
3. **Fade Out** → 500ms opacity transition
4. **Remove** → Loader removed from DOM
5. **Fallback** → Auto-hide after 5s max (prevents stuck loader)

### Customization
Edit the inline `<style>` block in `index.html`:

```css
.tems-loading {
    background: linear-gradient(135deg, #36454f 0%, #2b373f 50%, #20292f 100%);
}

.tems-loader {
    border-top-color: #39ff14;  /* Spinner color */
    box-shadow: 0 0 20px rgba(57, 255, 20, 0.4);  /* Glow intensity */
}

.tems-loading-text {
    color: #39ff14;
    text-shadow: 0 0 10px rgba(57, 255, 20, 0.6);  /* Text glow */
}
```

## 🔧 Applying to Other Portals

### Step 1: Copy Template Structure
```bash
# Create new portal directory
mkdir -p apps/tems/www/fleet-manager

# Copy and customize the template
cp apps/tems/www/driver/index.html apps/tems/www/fleet-manager/index.html
```

### Step 2: Customize Portal-Specific Elements
Edit the new `index.html`:

```html
<title>TEMS Fleet Manager Portal</title>

<!-- Update loading text -->
<div class="tems-loading-text">Loading Fleet Manager Portal...</div>

<!-- Update PWA paths -->
<link rel="stylesheet" href="/assets/tems/frontend/fleet-pwa/dist/assets/index-*.css">
<script src="/assets/tems/frontend/fleet-pwa/dist/assets/index-*.js"></script>
```

### Step 3: Keep Global Theme
All portals share the same base theme:
```html
<!-- This stays the same across all portals -->
<link rel="stylesheet" href="/assets/tems/css/tems_theme.css">
```

## 📱 PWA Manifest Integration

The template properly links to the PWA manifest:

```html
<link rel="manifest" href="/assets/tems/frontend/driver-pwa/dist/manifest.webmanifest">
```

### Manifest Theme Alignment
Ensure `vite.config.js` manifest matches template:

```javascript
manifest: {
  theme_color: '#36454f',           // ← Matches meta theme-color
  background_color: '#e0e2db',      // ← Matches body background
  icons: [
    {
      src: 'pwa-192x192.png',
      sizes: '192x192',
      type: 'image/png'
    },
    {
      src: 'pwa-512x512.png',
      sizes: '512x512',
      type: 'image/png'
    }
  ]
}
```

## 🧪 Testing

### Desktop Browser
```bash
# Visit in browser
http://tems.local:8000/driver
```

**Expected Behavior:**
1. ✅ Charcoal gradient loading screen appears
2. ✅ Neon green circuit logo pulses
3. ✅ Spinner rotates with glow effect
4. ✅ "Loading..." text with neon shadow
5. ✅ Loader fades out smoothly
6. ✅ PWA app loads with theme colors

### Mobile Testing (iOS/Android)

#### iOS Safari:
```bash
1. Open Safari → http://tems.local:8000/driver
2. Tap Share → "Add to Home Screen"
3. Check:
   ✓ Icon shows circuit map pin design
   ✓ Launch screen has charcoal background
   ✓ Status bar is black-translucent
   ✓ No browser chrome (full-screen app)
```

#### Android Chrome:
```bash
1. Open Chrome → http://tems.local:8000/driver
2. Check address bar:
   ✓ Should be charcoal gray (#36454f)
3. Menu → "Add to Home screen"
4. Launch app:
   ✓ Splash screen shows charcoal background
   ✓ Theme color persists
```

### DevTools Inspection
```javascript
// Open browser console and check:

// 1. Theme color applied
document.querySelector('meta[name="theme-color"]').content
// Expected: "#36454f"

// 2. Manifest loaded
navigator.serviceWorker.getRegistrations()
// Should show service worker registered

// 3. Assets loaded correctly
performance.getEntriesByType('resource')
  .filter(r => r.name.includes('driver-pwa'))
// Should show CSS and JS with hashed filenames
```

## 🔍 Troubleshooting

### Issue: Theme Color Not Showing in Mobile

**Diagnosis:**
```bash
# Check template has correct meta tag
grep 'theme-color' apps/tems/www/driver/index.html
```

**Fix:**
```html
<!-- Should be: -->
<meta name="theme-color" content="#36454f">

<!-- NOT: -->
<meta name="theme-color" content="#0970a0">  <!-- Old blue -->
```

### Issue: Loading Screen Never Disappears

**Diagnosis:**
Open browser console and check for JavaScript errors.

**Fix:**
The template includes a 5-second failsafe:
```javascript
// Fallback: Hide loader after 5 seconds regardless
setTimeout(function() {
    const loader = document.getElementById('tems-loading');
    if (loader && !loader.classList.contains('hidden')) {
        loader.classList.add('hidden');
    }
}, 5000);
```

### Issue: Assets Not Loading (404 Errors)

**Diagnosis:**
```bash
# Check build output exists
ls -la apps/tems/public/frontend/driver-pwa/dist/assets/

# Check template references correct hashes
grep 'index-.*\.css' apps/tems/www/driver/index.html
grep 'index-.*\.js' apps/tems/www/driver/index.html
```

**Fix:**
```bash
# Rebuild and update template
cd apps/tems/frontend/driver-pwa
npm run build
./update-template.sh

# Clear cache
cd /workspace/development/frappe-bench
bench --site tems.local clear-cache
```

## 📋 Checklist for New Portals

When creating a new TEMS portal, use this checklist:

- [ ] Copy `www/driver/index.html` as template
- [ ] Update `<title>` tag
- [ ] Update loading text (e.g., "Loading Fleet Manager Portal...")
- [ ] Update PWA asset paths (CSS/JS)
- [ ] Keep global theme CSS link
- [ ] Update manifest path if needed
- [ ] Create corresponding PWA in `frontend/`
- [ ] Build PWA and run update script
- [ ] Test loading screen animations
- [ ] Test mobile theme-color
- [ ] Test "Add to Home Screen"
- [ ] Verify service worker registration

## 🎓 Best Practices

### 1. **Never Edit Frappe Core Templates**
✅ Use custom standalone templates in `apps/tems/www/`
❌ Don't modify `frappe/templates/` or `erpnext/templates/`

### 2. **Keep Theme Consistent**
✅ Use global `tems_theme.css` for shared styles
✅ Apply `.tems-theme` class to `<body>`
✅ Use consistent color variables

### 3. **Optimize Loading Experience**
✅ Inline critical CSS for loading screen
✅ Preload essential assets
✅ Use smooth fade transitions
✅ Include failsafe timeouts

### 4. **Test on Real Devices**
✅ Test iOS Safari PWA install
✅ Test Android Chrome theme color
✅ Test offline functionality
✅ Test loading screen on slow connections

## 📚 Additional Resources

- [THEME_GUIDE.md](./THEME_GUIDE.md) - Complete color system documentation
- [THEME_UPDATE_SUMMARY.md](./THEME_UPDATE_SUMMARY.md) - Recent theme changes
- [THEME_CHECKLIST.md](./THEME_CHECKLIST.md) - Verification checklist
- [DriverPWA_Prompt.md](./DriverPWA_Prompt.md) - Original feature requirements

## 🚀 Quick Start Commands

```bash
# Build and deploy
cd /workspace/development/frappe-bench/apps/tems/frontend/driver-pwa
./build.sh

# Manual cache clear
cd /workspace/development/frappe-bench
bench --site tems.local clear-cache
bench --site tems.local clear-website-cache

# Test
open http://tems.local:8000/driver
```

---

**Last Updated:** October 14, 2025  
**TEMS Version:** v0.1.0  
**Author:** TEMS Development Team
