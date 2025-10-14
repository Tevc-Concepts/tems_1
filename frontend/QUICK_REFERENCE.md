# TEMS Frontend - Quick Reference

## 📁 Project Structure
```
frontend/
├── shared/              → @tems/shared - Common code
├── driver-pwa/          → @tems/driver-pwa - Driver portal
├── operations-pwa/      → @tems/operations-pwa - Operations control
├── safety-pwa/          → @tems/safety-pwa - Safety & compliance
└── fleet-pwa/           → @tems/fleet-pwa - Fleet management
```

## 🚀 Commands

### Development
```bash
npm run dev:driver        # Port 5173
npm run dev:operations    # Port 5174
npm run dev:safety        # Port 5175
npm run dev:fleet         # Port 5176
npm run dev:all          # All PWAs concurrently
```

### Build
```bash
npm run build:driver      # Build driver PWA
npm run build:all        # Build all PWAs
```

### Code Quality
```bash
npm run lint             # Check code quality
npm run lint:fix         # Auto-fix issues
npm run format           # Format code
npm run type-check       # Check TypeScript
```

### Maintenance
```bash
npm install              # Install dependencies
npm run clean            # Remove node_modules and builds
```

## 📦 Imports

### Shared Utilities
```javascript
import { frappeClient } from '@shared'
import { formatDate, formatCurrency } from '@shared/utils/formatters'
import { isValidEmail, rules } from '@shared/utils/validators'
import { debounce, isEmpty } from '@shared/utils/helpers'
```

### Shared Stores
```javascript
import { useAuthStore } from '@shared/stores/auth'
import { useOfflineStore } from '@shared/stores/offline'
```

### Shared Composables
```javascript
import { useAuth } from '@shared/composables/useAuth'
import { useOfflineSync } from '@shared/composables/useOfflineSync'
import { useGeolocation } from '@shared/composables/useGeolocation'
```

### Shared Components
```javascript
import Button from '@shared/components/common/Button.vue'
import Modal from '@shared/components/common/Modal.vue'
import AppLayout from '@shared/components/layout/AppLayout.vue'
```

## 🔌 Frappe API Usage

### Get Document
```javascript
const vehicle = await frappeClient.getDoc('Vehicle', 'VEH-001')
```

### Get List
```javascript
const trips = await frappeClient.getList(
  'Journey Plan',
  ['name', 'route', 'status'],
  [['driver', '=', user]],
  20  // limit
)
```

### Create Document
```javascript
const doc = await frappeClient.createDoc('Safety Incident', {
  incident_type: 'Accident',
  severity: 'High'
})
```

### Update Document
```javascript
await frappeClient.setDoc('Journey Plan', 'JP-001', {
  status: 'Completed'
})
```

### Call RPC Method
```javascript
const result = await frappeClient.call(
  'tems.api.pwa.driver.get_trips',
  { status: 'Active' }
)
```

### Upload File
```javascript
const file = await frappeClient.uploadFile(
  fileObject,
  true,              // isPrivate
  'Safety/Incidents', // folder
  'Safety Incident',  // doctype
  'SI-001'           // docname
)
```

## 🎨 Theme Colors

```javascript
// Primary - Neon Green
primary-500: '#39ff14'
primary-600: '#2ecc10'

// Charcoal Gray
charcoal-500: '#36454f'
charcoal-600: '#2b373f'

// Background
background: '#e0e2db'

// Status
success: '#39ff14'
warning: '#ffcc00'
danger: '#ff3366'
info: '#00ccff'
```

## 🧩 Component Examples

### Button
```vue
<Button variant="primary" @click="handleClick">
  Save
</Button>
```

### Input with Validation
```vue
<Input
  v-model="email"
  type="email"
  :rules="[rules.required(), rules.email()]"
  label="Email Address"
/>
```

### Modal
```vue
<Modal v-model:open="isOpen" title="Confirm">
  <p>Are you sure?</p>
  <template #footer>
    <Button @click="confirm">Yes</Button>
    <Button variant="secondary" @click="isOpen = false">No</Button>
  </template>
</Modal>
```

## 🔒 Authentication

```javascript
// In component
import { useAuth } from '@shared/composables/useAuth'

const { user, isAuthenticated, userName, logout } = useAuth()

// Check role
if (hasRole('Driver')) {
  // Driver-specific logic
}
```

## 📡 Offline Support

```javascript
import { useOfflineSync } from '@shared/composables/useOfflineSync'

const { isOnline, hasPendingChanges, sync } = useOfflineSync()

// Manual sync
await sync()
```

## 🗺️ Geolocation

```javascript
import { useGeolocation } from '@shared/composables/useGeolocation'

const { coords, getCurrentPosition, startWatching } = useGeolocation()

await getCurrentPosition()
console.log(coords.value.latitude, coords.value.longitude)
```

## 📸 Camera

```javascript
import { useCamera } from '@shared/composables/useCamera'

const { capturePhoto } = useCamera()

const imageData = await capturePhoto('front') // or 'back'
```

## 🔔 Notifications

```javascript
import { useToast } from '@shared/composables/useToast'

const toast = useToast()

toast.success('Operation completed!')
toast.error('Something went wrong')
toast.warning('Please be careful')
toast.info('New message received')
```

## 📊 Formatters

```javascript
import { formatDate, formatCurrency, formatDistance } from '@shared/utils/formatters'

formatDate(new Date(), 'MMM dd, yyyy')         // "Oct 14, 2025"
formatCurrency(1234.56, 'USD')                 // "$1,234.56"
formatDistance(5432)                           // "5.43km"
```

## ✅ Validators

```javascript
import { isValidEmail, rules, createValidator } from '@shared/utils/validators'

// Single validation
if (isValidEmail(email)) { }

// Form validation
const validator = createValidator({
  email: [rules.required(), rules.email()],
  password: [rules.required(), rules.minLength(8)]
})

const { valid, errors } = validator(formData)
```

## 🛣️ Router Setup

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@shared/composables/useAuth'

const router = createRouter({
  history: createWebHistory('/driver/'),  // Change per PWA
  routes: [/* ... */]
})

// Auth guard
router.beforeEach(async (to, from, next) => {
  const { isAuthenticated, fetchUserInfo } = useAuth()
  
  if (!isAuthenticated.value) {
    try {
      await fetchUserInfo()
    } catch {
      window.location.href = '/login'
      return
    }
  }
  
  next()
})
```

## 🏗️ Creating New View

```vue
<template>
  <AppLayout>
    <template #header>
      <h1>My View</h1>
    </template>
    
    <div class="p-4">
      <Card>
        <h2>Content</h2>
      </Card>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { frappeClient } from '@shared'
import AppLayout from '@shared/components/layout/AppLayout.vue'
import Card from '@shared/components/common/Card.vue'

const data = ref([])

onMounted(async () => {
  data.value = await frappeClient.getList('DocType')
})
</script>
```

## 🔧 Vite Config (Per PWA)

```javascript
import { createPWAConfig } from '../vite.config.base.js'

export default createPWAConfig(
  'pwa-name',      // Base path
  'Display Name',  // PWA name
  '#36454f'       // Theme color
)
```

## 📝 Common Patterns

### Loading State
```javascript
const loading = ref(false)

async function fetchData() {
  loading.value = true
  try {
    const data = await frappeClient.getList('DocType')
    return data
  } finally {
    loading.value = false
  }
}
```

### Error Handling
```javascript
const error = ref(null)

try {
  await someOperation()
} catch (err) {
  error.value = err.message
  toast.error(err.message)
}
```

### Form Submission
```javascript
const form = ref({ name: '', email: '' })

async function submit() {
  try {
    await frappeClient.createDoc('DocType', form.value)
    toast.success('Saved successfully!')
  } catch (err) {
    toast.error('Save failed: ' + err.message)
  }
}
```

## 🐛 Debugging

### Check Build Output
```bash
ls -lh ../../tems/public/frontend/driver-pwa/dist/
```

### Check Frappe Logs
```bash
cd /workspace/development/frappe-bench
tail -f logs/frappe.log
```

### Network Issues
Open browser DevTools → Network tab → Check API calls

### State Issues
Install Vue Devtools extension → Inspect Pinia stores

## 📚 Documentation

- **Main**: `README.md`
- **Implementation**: `IMPLEMENTATION_GUIDE.md`
- **Progress**: `REFACTORING_PROGRESS.md`
- **Summary**: `REFACTORING_SUMMARY.md`
- **Frappe**: `../../tems/doc/doctype_reference.md`

## 🎯 Key Files

- **Root Config**: `package.json`, `tsconfig.json`, `tailwind.config.js`
- **Shared Utils**: `shared/src/utils/frappeClient.js`
- **Shared Stores**: `shared/src/stores/auth.js`
- **Base Config**: `vite.config.base.js`

---

**Need Help?** Check `IMPLEMENTATION_GUIDE.md` for detailed instructions.
