# TEMS Frontend Monorepo - Implementation Guide

This guide provides step-by-step instructions for completing the monorepo refactoring.

## 📋 Current Status

**Phase 1 (Core Infrastructure)**: ✅ **COMPLETED**
- Root workspace configuration
- Shared module structure
- Enhanced Frappe API client
- Utility libraries (helpers, validators, formatters)
- Base stores (auth, offline)

**Phase 2-6**: 🚧 **IN PROGRESS**

## 🎯 Implementation Steps

### Step 1: Complete Shared Composables

Create the following files in `shared/src/composables/`:

#### `useAuth.js`
```javascript
import { useAuthStore } from '@shared/stores/auth'
import { storeToRefs } from 'pinia'

export function useAuth() {
  const authStore = useAuthStore()
  const { user, employee, isAuthenticated, userName, userInitials } = storeToRefs(authStore)
  
  return {
    user,
    employee,
    isAuthenticated,
    userName,
    userInitials,
    fetchUserInfo: authStore.fetchUserInfo,
    hasRole: authStore.hasRole,
    hasAnyRole: authStore.hasAnyRole,
    logout: authStore.logout
  }
}
```

#### `useOfflineSync.js`
```javascript
import { useOfflineStore } from '@shared/stores/offline'
import { storeToRefs } from 'pinia'

export function useOfflineSync() {
  const offlineStore = useOfflineStore()
  const { isOnline, hasPendingChanges, queueCount, isSyncing } = storeToRefs(offlineStore)
  
  return {
    isOnline,
    hasPendingChanges,
    queueCount,
    isSyncing,
    sync: offlineStore.syncOfflineData,
    clearCache: offlineStore.clearOfflineData
  }
}
```

#### `useGeolocation.js`
Copy from `driver-pwa/src/composables/useGeolocation.js` with enhancements:
- Add distance calculation utility
- Add bearing calculation
- Add format helpers

#### `useCamera.js`
Copy from `driver-pwa/src/composables/useCamera.js` with enhancements:
- Support both front and back camera
- Add image compression
- Add upload integration

#### `useToast.js`
```javascript
import { ref } from 'vue'

const toasts = ref([])
let id = 0

export function useToast() {
  function show(message, type = 'info', duration = 3000) {
    const toast = {
      id: id++,
      message,
      type,
      visible: true
    }
    
    toasts.value.push(toast)
    
    if (duration > 0) {
      setTimeout(() => dismiss(toast.id), duration)
    }
    
    return toast.id
  }
  
  function dismiss(toastId) {
    const index = toasts.value.findIndex(t => t.id === toastId)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  function success(message, duration) {
    return show(message, 'success', duration)
  }
  
  function error(message, duration) {
    return show(message, 'error', duration)
  }
  
  function warning(message, duration) {
    return show(message, 'warning', duration)
  }
  
  function info(message, duration) {
    return show(message, 'info', duration)
  }
  
  return {
    toasts,
    show,
    dismiss,
    success,
    error,
    warning,
    info
  }
}
```

### Step 2: Create Shared UI Components

#### Component Library Structure
```
shared/src/components/
├── layout/
│   ├── AppHeader.vue       # Top navigation bar
│   ├── AppSidebar.vue      # Side navigation (desktop)
│   ├── AppBottomNav.vue    # Bottom navigation (mobile)
│   └── AppLayout.vue       # Main layout wrapper
├── common/
│   ├── Button.vue          # Styled button with variants
│   ├── Input.vue           # Form input with validation
│   ├── Select.vue          # Dropdown select
│   ├── Modal.vue           # Modal dialog
│   ├── Toast.vue           # Toast notification
│   ├── Loading.vue         # Loading spinner
│   ├── Badge.vue           # Status badge
│   ├── Card.vue            # Content card
│   └── Icon.vue            # Icon wrapper (lucide-vue-next)
└── index.js                # Export all components
```

### Step 3: Refactor Driver PWA

1. **Update `driver-pwa/package.json`**:
   ```json
   {
     "name": "@tems/driver-pwa",
     "dependencies": {
       "@tems/shared": "workspace:*"
     }
   }
   ```

2. **Update `driver-pwa/vite.config.js`**:
   ```javascript
   import { createPWAConfig } from '../vite.config.base.js'
   export default createPWAConfig('driver-pwa', 'Driver', '#36454f')
   ```

3. **Refactor imports**:
   - Replace `@/utils/frappeClient` with `@shared/utils/frappeClient`
   - Replace local stores with shared stores
   - Replace local composables with shared composables

4. **Update main.js**:
   ```javascript
   import { createApp } from 'vue'
   import { createPinia } from 'pinia'
   import App from './App.vue'
   import router from './router'
   import '@shared/assets/styles/main.css' // If shared styles exist
   import './assets/styles/main.css'
   
   const app = createApp(App)
   const pinia = createPinia()
   
   app.use(pinia)
   app.use(router)
   app.mount('#app')
   ```

5. **Test**:
   ```bash
   npm run dev:driver
   npm run build:driver
   ```

### Step 4: Create Operations PWA

1. **Create directory structure**:
   ```bash
   cd frontend
   mkdir -p operations-pwa/src/{components,composables,router,stores,views,assets/styles}
   mkdir -p operations-pwa/public
   ```

2. **Copy base files from driver-pwa**:
   ```bash
   cp driver-pwa/package.json operations-pwa/
   cp driver-pwa/index.html operations-pwa/
   cp driver-pwa/postcss.config.js operations-pwa/
   cp driver-pwa/tailwind.config.js operations-pwa/
   ```

3. **Update `operations-pwa/package.json`**:
   ```json
   {
     "name": "@tems/operations-pwa",
     "version": "1.0.0",
     "scripts": {
       "dev": "vite --port 5174",
       "build": "vite build",
       "preview": "vite preview"
     }
   }
   ```

4. **Create `operations-pwa/vite.config.js`**:
   ```javascript
   import { createPWAConfig } from '../vite.config.base.js'
   export default createPWAConfig('operations-pwa', 'Operations', '#0284c7')
   ```

5. **Create `operations-pwa/src/main.js`**:
   ```javascript
   import { createApp } from 'vue'
   import { createPinia } from 'pinia'
   import App from './App.vue'
   import router from './router'
   import './assets/styles/main.css'
   
   const app = createApp(App)
   app.use(createPinia())
   app.use(router)
   app.mount('#app')
   ```

6. **Create `operations-pwa/src/App.vue`**:
   ```vue
   <template>
     <router-view />
   </template>
   
   <script setup>
   import { onMounted } from 'vue'
   import { useAuth } from '@shared/composables/useAuth'
   import { useOfflineSync } from '@shared/composables/useOfflineSync'
   
   const { fetchUserInfo, isAuthenticated } = useAuth()
   const offlineSync = useOfflineSync()
   
   onMounted(async () => {
     await fetchUserInfo()
     offlineSync.init()
   })
   </script>
   ```

7. **Create `operations-pwa/src/router/index.js`**:
   ```javascript
   import { createRouter, createWebHistory } from 'vue-router'
   import { useAuth } from '@shared/composables/useAuth'
   
   const routes = [
     {
       path: '/',
       name: 'Dashboard',
       component: () => import('../views/Dashboard.vue')
     },
     {
       path: '/fleet-tracking',
       name: 'FleetTracking',
       component: () => import('../views/FleetTracking.vue')
     },
     {
       path: '/dispatch',
       name: 'Dispatch',
       component: () => import('../views/Dispatch.vue')
     }
   ]
   
   const router = createRouter({
     history: createWebHistory('/operations/'),
     routes
   })
   
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
   
   export default router
   ```

8. **Create minimal views**:
   - `operations-pwa/src/views/Dashboard.vue`
   - `operations-pwa/src/views/FleetTracking.vue`
   - `operations-pwa/src/views/Dispatch.vue`

9. **Test**:
   ```bash
   npm run dev:operations
   ```

### Step 5: Create Safety PWA

Follow same pattern as Operations PWA:
- Port: 5175
- Theme color: #ef4444 (red)
- Base path: /safety/
- Key views: Dashboard, Incidents, Audits, Compliance

### Step 6: Create Fleet PWA

Follow same pattern as Operations PWA:
- Port: 5176
- Theme color: #10b981 (green)
- Base path: /fleet/
- Key views: Dashboard, Maintenance, Assets, Utilization

### Step 7: Update Frappe Backend

#### Update `tems/hooks.py`

Add web routes:
```python
web_include_js = [
    "tems_web.bundle.js"
]

web_include_css = [
    "tems_theme.css"
]

website_route_rules = [
    {"from_route": "/driver/<path:app_path>", "to_route": "driver"},
    {"from_route": "/operations/<path:app_path>", "to_route": "operations"},
    {"from_route": "/safety/<path:app_path>", "to_route": "safety"},
    {"from_route": "/fleet/<path:app_path>", "to_route": "fleet"},
]
```

#### Create WWW Entry Points

**`tems/www/operations/index.html`**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#0284c7">
  <title>TEMS Operations</title>
  <link rel="stylesheet" href="/assets/tems/frontend/operations-pwa/dist/assets/index-[hash].css">
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/assets/tems/frontend/operations-pwa/dist/assets/index-[hash].js"></script>
</body>
</html>
```

Repeat for safety and fleet PWAs.

#### Create API Endpoints

**`tems/api/pwa/operations.py`**:
```python
import frappe
from frappe import _

@frappe.whitelist()
def get_active_trips():
    """Get all active trips for operations dashboard"""
    trips = frappe.get_all(
        "Journey Plan",
        filters={"status": "Active"},
        fields=["name", "route", "driver", "vehicle", "start_time", "eta"]
    )
    return trips

@frappe.whitelist()
def get_fleet_status():
    """Get real-time fleet status"""
    # Implementation
    pass

@frappe.whitelist()
def create_dispatch():
    """Create new dispatch assignment"""
    # Implementation
    pass
```

Repeat for safety and fleet.

### Step 8: Testing Checklist

- [ ] All PWAs build without errors
- [ ] No circular dependencies
- [ ] TypeScript compiles successfully
- [ ] Shared components work across all PWAs
- [ ] Frappe API integration works
- [ ] Offline functionality works
- [ ] Authentication flow works
- [ ] Routing works correctly
- [ ] Build outputs in correct directories
- [ ] PWA manifests generated correctly
- [ ] Service workers registered
- [ ] Frappe Desk unaffected
- [ ] File sizes under 200KB initial load
- [ ] Development HMR works

### Step 9: Documentation

Create documentation for:
- [ ] Architecture overview
- [ ] Development workflow
- [ ] Component API documentation
- [ ] Deployment process
- [ ] Troubleshooting guide

## 🚀 Quick Commands Reference

```bash
# Install everything
npm install

# Development
npm run dev:driver        # Port 5173
npm run dev:operations    # Port 5174
npm run dev:safety        # Port 5175
npm run dev:fleet         # Port 5176
npm run dev:all          # All concurrent

# Build
npm run build:driver
npm run build:operations
npm run build:safety
npm run build:fleet
npm run build:all

# Code Quality
npm run lint
npm run format
npm run type-check

# Clean
npm run clean
```

## 📝 Migration Checklist

### Driver PWA Migration
- [ ] Update package.json dependencies
- [ ] Update vite.config.js to use base config
- [ ] Replace frappeClient imports
- [ ] Replace store imports
- [ ] Replace composable imports
- [ ] Test all features work
- [ ] Test offline sync
- [ ] Test build output

### Operations PWA Creation
- [ ] Create directory structure
- [ ] Configure package.json
- [ ] Configure vite.config.js
- [ ] Create router
- [ ] Create Dashboard view
- [ ] Create Fleet Tracking view
- [ ] Create Dispatch view
- [ ] Create Frappe www entry point
- [ ] Create API endpoints
- [ ] Test functionality

### Safety PWA Creation
- [ ] Create directory structure
- [ ] Configure package.json
- [ ] Configure vite.config.js
- [ ] Create router
- [ ] Create Dashboard view
- [ ] Create Incidents view
- [ ] Create Audits view
- [ ] Create Frappe www entry point
- [ ] Create API endpoints
- [ ] Test functionality

### Fleet PWA Creation
- [ ] Create directory structure
- [ ] Configure package.json
- [ ] Configure vite.config.js
- [ ] Create router
- [ ] Create Dashboard view
- [ ] Create Maintenance view
- [ ] Create Assets view
- [ ] Create Frappe www entry point
- [ ] Create API endpoints
- [ ] Test functionality

## 🎉 Success Criteria

The refactoring is complete when:

1. ✅ All 4 PWAs build successfully
2. ✅ Shared code has zero duplication
3. ✅ All PWAs use @shared imports
4. ✅ Offline functionality works across all PWAs
5. ✅ Type safety maintained
6. ✅ Bundle sizes optimized (< 200KB)
7. ✅ HMR works in development
8. ✅ Frappe Desk completely unaffected
9. ✅ Documentation complete
10. ✅ All tests passing

## 🐛 Common Issues & Solutions

### Issue: Module not found '@shared'
**Solution**: Check tsconfig.json paths and vite.config.js aliases

### Issue: Build fails with Frappe path error
**Solution**: Verify outDir in vite.config.js points to correct Frappe directory

### Issue: HMR not working
**Solution**: Ensure dev server proxy configured correctly

### Issue: Offline sync not working
**Solution**: Check service worker registration and cache configuration

---

**Next**: Start with Step 1 (Complete Shared Composables) and proceed sequentially.
