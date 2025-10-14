# TEMS Theme - Neon Green & Charcoal Gray

## 🎨 Color Palette

### Primary Colors
- **Neon Green**: `#39ff14` - Main brand color for CTAs, highlights, and interactive elements
- **Charcoal Gray**: `#36454f` - Secondary brand color for headers, navigation, and text
- **Light Gray**: `#e0e2db` - Background color for pages and sections

### Extended Palette

#### Neon Green Variants
```css
--tems-green-50: #e6ffe8    /* Lightest - backgrounds */
--tems-green-100: #ccffce   /* Light - subtle highlights */
--tems-green-200: #99ff9d   /* Soft - hover states */
--tems-green-300: #66ff6b   /* Medium - badges */
--tems-green-400: #4dff3a   /* Bright - attention */
--tems-green-500: #39ff14   /* MAIN - primary actions */
--tems-green-600: #2ecc10   /* Dark - pressed states */
--tems-green-700: #24990c   /* Darker - text */
--tems-green-800: #196607   /* Very dark - emphasis */
--tems-green-900: #0f3304   /* Darkest - headers */
```

#### Charcoal Gray Variants
```css
--tems-charcoal-50: #e8eaeb   /* Lightest - backgrounds */
--tems-charcoal-100: #d1d5d7  /* Light - borders */
--tems-charcoal-200: #a3abb0  /* Soft - dividers */
--tems-charcoal-300: #758188  /* Medium - disabled states */
--tems-charcoal-400: #475761  /* Dark - secondary text */
--tems-charcoal-500: #36454f  /* MAIN - headers, navigation */
--tems-charcoal-600: #2b373f  /* Darker - hover states */
--tems-charcoal-700: #20292f  /* Very dark - emphasis */
--tems-charcoal-800: #161c20  /* Darkest - text */
--tems-charcoal-900: #0b0e10  /* Almost black - strong text */
```

### Status Colors
- **Success**: `#39ff14` (Neon Green)
- **Warning**: `#ffcc00` (Bright Yellow)
- **Danger**: `#ff3366` (Bright Red)
- **Info**: `#00ccff` (Bright Cyan)

## 🌟 Special Effects

### Neon Glow Shadows
```css
/* Subtle Glow */
box-shadow: 0 0 10px rgba(57, 255, 20, 0.5), 0 0 20px rgba(57, 255, 20, 0.3);

/* Strong Glow */
box-shadow: 0 0 20px rgba(57, 255, 20, 0.6), 0 0 40px rgba(57, 255, 20, 0.4);

/* Neon Text */
text-shadow: 0 0 10px rgba(57, 255, 20, 0.8), 0 0 20px rgba(57, 255, 20, 0.5);
```

### Gradients
```css
/* Primary Gradient (Neon Green) */
background: linear-gradient(135deg, #39ff14 0%, #2ecc10 100%);

/* Secondary Gradient (Charcoal) */
background: linear-gradient(135deg, #36454f 0%, #2b373f 100%);

/* Hero Gradient (Dark Charcoal) */
background: linear-gradient(135deg, #36454f 0%, #2b373f 50%, #20292f 100%);
```

## 📦 Implementation

### Driver PWA
Location: `/workspace/development/frappe-bench/apps/tems/frontend/driver-pwa/`

#### Tailwind Config
```javascript
// tailwind.config.js
colors: {
  primary: { /* Neon Green shades */ },
  charcoal: { /* Charcoal Gray shades */ },
  background: '#e0e2db',
}
```

#### Main CSS
```css
/* src/assets/styles/main.css */
:root {
  --primary-500: 57 255 20;      /* Neon Green */
  --charcoal-500: 54 69 79;      /* Charcoal Gray */
  --background: 224 226 219;     /* Light Gray */
}
```

### Global Theme CSS
Location: `/workspace/development/frappe-bench/apps/tems/tems/public/css/tems_theme.css`

This file contains reusable classes for all TEMS portals and pages.

#### Usage in Frappe Pages
```html
<!-- Add to your Frappe page template -->
<link rel="stylesheet" href="/assets/tems/css/tems_theme.css">

<!-- Apply theme to body or container -->
<body class="tems-theme">
  <!-- or -->
  <div class="tems-portal">
    <!-- Your content -->
  </div>
</body>
```

## 🎯 Component Guidelines

### Buttons
```html
<!-- Primary Action (Neon Green with Glow) -->
<button class="tems-btn-primary">Submit</button>

<!-- Secondary Action (Charcoal with Neon Border) -->
<button class="tems-btn-secondary">Cancel</button>

<!-- Frappe Integration -->
<button class="btn-primary tems-btn">Save</button>
```

### Cards
```html
<!-- Standard Card -->
<div class="card tems-card">
  <div class="card-header tems-card-header">
    <h3>Card Title</h3>
  </div>
  <div class="card-body">
    <!-- Content -->
  </div>
</div>
```

### Navigation
```html
<!-- Header/Navbar -->
<nav class="navbar tems-navbar">
  <a href="#" class="nav-link tems-nav-link">Home</a>
  <a href="#" class="nav-link tems-nav-link active">Dashboard</a>
</nav>
```

### Forms
```html
<!-- Input Fields -->
<input type="text" class="form-control tems-input" placeholder="Enter text">

<!-- Focus state automatically applies neon green glow -->
```

### Badges
```html
<!-- Success Badge -->
<span class="badge badge-success tems-badge">Active</span>

<!-- Warning Badge -->
<span class="badge badge-warning tems-badge">Pending</span>
```

### Typography
```html
<!-- Neon Text Effect -->
<h1 class="tems-neon-text">TEMS Driver Portal</h1>

<!-- Standard Heading -->
<h2 class="tems-heading">Section Title</h2>
```

## 🔧 Customization

### Override Colors
```css
/* In your custom CSS */
:root {
  --tems-neon-green: #your-green;
  --tems-charcoal-gray: #your-charcoal;
  --tems-light-gray: #your-background;
}
```

### Add Custom Variants
```css
.my-custom-btn {
  background: var(--tems-gradient-primary);
  color: var(--tems-charcoal-700);
  box-shadow: var(--tems-shadow-neon);
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 700;
}

.my-custom-btn:hover {
  box-shadow: var(--tems-shadow-neon-lg);
  transform: translateY(-2px);
}
```

## 📱 PWA Manifest
Location: `vite.config.js`

```javascript
manifest: {
  theme_color: '#36454f',        // Charcoal Gray
  background_color: '#e0e2db',   // Light Gray
  // ... other settings
}
```

## 🖼️ Icons & Logo

### PWA Icons
- **192x192**: `/frontend/driver-pwa/public/192x192.png`
- **512x512**: `/frontend/driver-pwa/public/512x512.png`

The icons feature the TEMS circuit/map pin design with neon green on charcoal background.

### Main Logo
- **Location**: `/workspace/development/frappe-bench/apps/tems/doc/logoTems.png`
- **Usage**: Primary brand logo with neon green circuit design

### Icon Guidelines
- Use neon green (#39ff14) for the main design elements
- Use charcoal gray (#36454f) for backgrounds
- Maintain high contrast for visibility
- Include glow effects where appropriate

## 🎨 Design Principles

1. **High Contrast**: Neon green on charcoal creates maximum visibility
2. **Glow Effects**: Use subtle neon glows for interactive elements
3. **Clean Backgrounds**: Light gray provides breathing room
4. **Bold Typography**: Use strong font weights with neon accents
5. **Consistent Spacing**: Maintain generous padding and margins
6. **Smooth Transitions**: Add subtle animations (200-300ms)

## 📋 Checklist for New Pages

- [ ] Add `tems_theme.css` to page head
- [ ] Apply `tems-theme` or `tems-portal` class to container
- [ ] Use `tems-btn-primary` for primary actions
- [ ] Use `tems-card` for content containers
- [ ] Apply `tems-navbar` to navigation elements
- [ ] Use neon green for interactive elements
- [ ] Use charcoal for text and structure
- [ ] Test on light and dark backgrounds
- [ ] Verify neon glow effects are visible
- [ ] Check mobile responsiveness

## 🚀 Build & Deploy

### Build Driver PWA
```bash
cd /workspace/development/frappe-bench/apps/tems/frontend/driver-pwa
./build.sh
```

### Clear Cache
```bash
cd /workspace/development/frappe-bench
bench --site tems.local clear-cache
bench --site tems.local clear-website-cache
```

### Access
- Driver Portal: `http://tems.local:8000/driver`

## 📊 Browser Support

- ✅ Chrome/Edge (Full neon glow support)
- ✅ Firefox (Full support)
- ✅ Safari (Full support)
- ✅ Mobile browsers (iOS/Android)

## 🎯 Accessibility

- **Contrast Ratio**: Neon green on charcoal exceeds WCAG AA standards
- **Focus States**: Clear focus indicators with neon glow
- **Screen Readers**: Semantic HTML maintained
- **Color Blindness**: High contrast works for most types

---

**Version**: 2.0  
**Last Updated**: October 14, 2025  
**Theme**: Neon Green & Charcoal Gray  
**Status**: ✅ Production Ready
