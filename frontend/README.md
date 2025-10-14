# TEMS Frontend Monorepo

> Role-based Progressive Web Apps (PWAs) for Transportation Enterprise Management System

## 🏗️ Architecture

This monorepo contains 4 role-specific PWAs built with Vue 3 + Vite, sharing common components, utilities, and business logic.

```
frontend/
├── shared/              # Shared code library
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── composables/ # Vue composables
│   │   ├── stores/      # Pinia stores
│   │   ├── utils/       # Utility functions
│   │   └── types/       # TypeScript types
├── driver-pwa/          # Driver portal
├── operations-pwa/      # Operations control center
├── safety-pwa/          # Safety & compliance portal
└── fleet-pwa/           # Fleet management portal
```

## 🚀 Quick Start

### Prerequisites
- Node.js >= 18.0.0
- npm >= 9.0.0
- Frappe V15+ backend running on localhost:8000

### Installation

```bash
# From the frontend directory
cd /workspace/development/frappe-bench/apps/tems/frontend

# Install all dependencies (root + all workspaces)
npm install
```

### Development

```bash
# Run specific PWA
npm run dev:driver        # http://localhost:5173
npm run dev:operations    # http://localhost:5174
npm run dev:safety        # http://localhost:5175
npm run dev:fleet         # http://localhost:5176

# Run all PWAs concurrently
npm run dev:all
```

### Building for Production

```bash
# Build specific PWA
npm run build:driver
npm run build:operations
npm run build:safety
npm run build:fleet

# Build all PWAs
npm run build:all
```

Build outputs go to:
- `tems/public/frontend/driver-pwa/dist/`
- `tems/public/frontend/operations-pwa/dist/`
- `tems/public/frontend/safety-pwa/dist/`
- `tems/public/frontend/fleet-pwa/dist/`

## 📦 Workspaces

### Shared Library (`@tems/shared`)

Core library providing:
- **Frappe API Client**: Type-safe client with offline support
- **Utilities**: Helpers, validators, formatters
- **Stores**: Auth, offline sync
- **Composables**: Reusable Vue composition functions
- **Components**: UI component library

#### Usage in PWAs

```javascript
// Import shared utilities
import { frappeClient } from '@shared'
import { formatDate, formatCurrency } from '@shared/utils/formatters'
import { useAuth } from '@shared/composables/useAuth'

// Use in components
const { user, isAuthenticated } = useAuth()
const formatted = formatDate(new Date(), 'MMM dd, yyyy')
```

### Driver PWA

Features:
- Trip management
- Vehicle inspection
- Fuel logging
- Incident reporting
- Real-time navigation
- Offline-first operation

**Access**: `http://localhost:8000/driver/`

### Operations PWA

Features:
- Real-time fleet tracking
- Dispatch management
- Trip planning and allocation
- Movement logging
- Control exception handling
- Analytics dashboard

**Access**: `http://localhost:8000/operations/`

### Safety PWA

Features:
- Compliance tracking
- Incident management
- Risk assessments
- Vehicle spot checks
- Safety training records
- Audit checklists

**Access**: `http://localhost:8000/safety/`

### Fleet PWA

Features:
- Maintenance scheduling
- Asset utilization tracking
- Fuel consumption analytics
- Vehicle lifecycle management
- Spare parts inventory
- Cost tracking

**Access**: `http://localhost:8000/fleet/`

## 🎨 Design System

### Color Palette

```javascript
// Primary - Neon Green
primary: '#39ff14'
primary-light: '#66ff6b'
primary-dark: '#2ecc10'

// Charcoal Gray
charcoal: '#36454f'
charcoal-light: '#475761'
charcoal-dark: '#2b373f'

// Background
background: '#e0e2db'

// Status Colors
success: '#39ff14'
warning: '#ffcc00'
danger: '#ff3366'
info: '#00ccff'
```

### Typography

- **Font**: System font stack
- **Base Size**: 16px
- **Scale**: 1.25 (Major Third)

### Spacing

Based on 4px (0.25rem) unit:
- 4, 8, 12, 16, 24, 32, 48, 64

## 🔧 Development Guide

### Project Structure

Each PWA follows this structure:

```
pwa-name/
├── public/              # Static assets
├── src/
│   ├── assets/         # Images, styles
│   ├── components/     # PWA-specific components
│   ├── composables/    # PWA-specific composables
│   ├── router/         # Vue Router configuration
│   ├── stores/         # PWA-specific stores
│   ├── views/          # Page components
│   ├── App.vue         # Root component
│   └── main.js         # Entry point
├── index.html          # HTML entry point
├── package.json        # PWA dependencies
├── vite.config.js      # Vite configuration
└── README.md           # PWA documentation
```

### Path Aliases

```javascript
// Available in all PWAs
@/           → src/
@shared/     → ../shared/src/
@shared/components/* → ../shared/src/components/
@shared/composables/* → ../shared/src/composables/
@shared/stores/* → ../shared/src/stores/
@shared/utils/* → ../shared/src/utils/
```

### Adding New Shared Code

1. Add to `shared/src/` in appropriate directory
2. Export from `shared/src/index.js` if public API
3. Use in PWAs with `@shared` alias
4. Rebuild PWAs to test

### Creating New PWA

```bash
# 1. Copy template (use driver-pwa as reference)
cp -r driver-pwa new-pwa

# 2. Update package.json
cd new-pwa
# Edit name, description, etc.

# 3. Update vite.config.js
# Change build.outDir to tems/public/frontend/new-pwa/dist
# Change manifest name, scope, start_url

# 4. Add to root package.json workspaces
# Add "new-pwa" to workspaces array

# 5. Add scripts to root package.json
# Add dev:new-pwa and build:new-pwa

# 6. Install dependencies
cd ..
npm install

# 7. Test
npm run dev:new-pwa
```

## 🔌 Frappe Integration

### API Client Usage

```javascript
import frappeClient from '@shared/utils/frappeClient'

// Get single document
const vehicle = await frappeClient.getDoc('Vehicle', 'VEH-001')

// Get list with filters
const trips = await frappeClient.getList(
  'Journey Plan',
  ['name', 'route', 'status'],
  [['driver', '=', currentUser]],
  20
)

// Create document
const incident = await frappeClient.createDoc('Safety Incident', {
  incident_type: 'Accident',
  severity: 'High',
  description: 'Minor collision'
})

// Update document
await frappeClient.setDoc('Journey Plan', 'JP-001', {
  status: 'Completed'
})

// Call RPC method
const result = await frappeClient.call(
  'tems.api.pwa.driver.get_trips',
  { status: 'Active' }
)

// Upload file
const file = await frappeClient.uploadFile(
  fileObject,
  true, // isPrivate
  'Safety/Incidents', // folder
  'Safety Incident', // doctype
  'SI-001' // docname
)
```

### Offline Support

All read operations are automatically cached. Write operations are queued when offline.

```javascript
import { useOfflineStore } from '@shared/stores/offline'

const offlineStore = useOfflineStore()

// Check status
console.log(offlineStore.isOnline) // true/false
console.log(offlineStore.queueCount) // Number of pending operations

// Manual sync
await offlineStore.syncOfflineData()

// Clear cache
await offlineStore.clearOfflineData()
```

## 🧪 Testing

```bash
# Lint code
npm run lint

# Fix lint errors
npm run lint:fix

# Format code
npm run format

# Type check
npm run type-check
```

## 🏗️ Build Process

### Development Build
- Source maps enabled
- HMR (Hot Module Replacement)
- No minification
- Dev server proxies to Frappe backend

### Production Build
- Minified and optimized
- Code splitting
- Tree shaking
- PWA service worker generated
- Assets hashed for caching

### Build Output

```
tems/public/frontend/pwa-name/dist/
├── assets/
│   ├── index-[hash].js    # Main bundle
│   ├── index-[hash].css   # Styles
│   └── ...                # Other chunks
├── manifest.webmanifest   # PWA manifest
├── sw.js                  # Service worker
└── workbox-*.js           # Workbox runtime
```

## 📱 PWA Features

All PWAs support:
- ✅ Offline-first architecture
- ✅ Install to home screen
- ✅ Background sync
- ✅ Push notifications
- ✅ Cache-first for assets
- ✅ Network-first for API calls
- ✅ Automatic updates

## 🔒 Security

- CSRF tokens automatically included
- Session-based authentication
- XSS prevention via sanitization
- Secure file uploads
- Role-based access control

## 📊 Performance

Target metrics:
- **Initial load**: < 200KB gzipped
- **Time to Interactive**: < 3s on 3G
- **First Contentful Paint**: < 1.5s
- **Lighthouse Score**: > 90

Optimizations:
- Code splitting per route
- Lazy loading components
- Image optimization
- Virtual scrolling for lists
- Memoization where appropriate

## 🐛 Debugging

### Vue Devtools
Install Vue Devtools browser extension for component inspection.

### Vite Debug
```bash
# Enable debug logs
DEBUG=vite:* npm run dev:driver
```

### Network Issues
Check Frappe backend logs:
```bash
cd /workspace/development/frappe-bench
tail -f logs/frappe.log
```

## 📚 Documentation

- [Refactoring Progress](./REFACTORING_PROGRESS.md) - Current refactoring status
- [Monorepo Architecture](../doc/MonorepoAgent.md) - Detailed architecture spec
- [Frappe Context](../doc/frappe-context.md) - Frappe environment info
- [DocType Reference](../../tems/doc/doctype_reference.md) - API reference

## 🤝 Contributing

### Code Style
- Use Composition API with `<script setup>`
- Follow ESLint and Prettier rules
- Write JSDoc comments for public APIs
- Use TypeScript types where possible
- Keep components focused and small

### Commit Convention
```
type(scope): description

feat(driver): add fuel logging
fix(shared): resolve offline sync issue
docs(readme): update installation guide
refactor(operations): extract dispatch logic
```

## 🚀 Deployment

### Frappe Cloud / Bench

Build outputs are automatically in correct locations:
```bash
# Build all
npm run build:all

# Frappe will serve from tems/public/frontend/
```

### Manual Deployment
```bash
# 1. Build
npm run build:all

# 2. Commit built files
git add ../../tems/public/frontend/
git commit -m "chore: update PWA builds"

# 3. Deploy via bench
cd /workspace/development/frappe-bench
bench migrate
bench clear-cache
```

## 📝 License

Copyright © 2025 TEMS. All rights reserved.

## 💬 Support

- **Issues**: GitHub Issues
- **Docs**: `/workspace/development/frappe-bench/apps/tems/doc/`
- **Frappe Forum**: https://discuss.frappe.io

---

**Built with** ❤️ **using Vue 3 + Vite + Frappe**
