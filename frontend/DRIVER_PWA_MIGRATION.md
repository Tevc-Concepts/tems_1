# Driver PWA Migration to Shared Code - Step by Step Guide

## ✅ Phase 4.1: Driver PWA Migration (In Progress)

### Files Updated

#### 1. Configuration Files ✅
- [x] `package.json` - Added `@tems/shared` workspace dependency
- [x] `vite.config.js` - Using shared `createPWAConfig`
- [x] `App.vue` - Using shared `Toast` and `useOfflineSync`

### Migration Strategy

#### Step 1: Replace Duplicate Stores
**Action**: Remove local stores that duplicate shared functionality

**Files to Update**:
- `src/stores/auth.js` → DELETE (use `@shared` useAuthStore)
- `src/stores/offline.js` → DELETE (use `@shared` useOfflineStore)

**Keep Local Stores**:
- `src/stores/trip.js` - Driver-specific
- `src/stores/vehicle.js` - Driver-specific  
- `src/stores/cargo.js` - Driver-specific
- `src/stores/passenger.js` - Driver-specific
- `src/stores/incident.js` - Driver-specific
- `src/stores/communication.js` - Driver-specific

#### Step 2: Replace Duplicate Composables
**Action**: Remove local composables that duplicate shared functionality

**Files to Update**:
- `src/composables/useGeolocation.js` → DELETE (use `@shared`)
- `src/composables/useCamera.js` → DELETE (use `@shared`)
- `src/composables/useNotifications.js` → DELETE (use `@shared`)
- `src/composables/useToast.js` → DELETE (use `@shared`)
- `src/composables/useOfflineSync.js` → DELETE (use `@shared`)

**Keep Local Composables**:
- `src/composables/useMedia.js` - If driver-specific
- `src/composables/useNotification.js` - Review if different from shared

#### Step 3: Replace Duplicate Utils
**Action**: Remove local utils that duplicate shared functionality

**Files to Update**:
- `src/utils/frappeClient.js` → DELETE (use `@shared` frappeClient)
- `src/utils/helpers.js` → REVIEW and merge unique helpers to shared or keep driver-specific ones

#### Step 4: Update Component Imports
**Action**: Replace local layout/common components with shared ones

**Files to Check**:
- All files in `src/components/layout/` - Can be replaced with shared `AppLayout`, `AppHeader`, etc.
- All files in `src/components/common/` - Can be replaced with shared `Button`, `Input`, etc.

**Keep Domain Components**:
- `src/components/trip/` - Trip-specific components
- `src/components/inspection/` - Inspection-specific
- `src/components/Incident/` - Incident-specific

#### Step 5: Update Views
**Action**: Update all views to use shared components

**Pattern**:
```vue
<!-- OLD -->
<script setup>
import { useAuthStore } from '@/stores/auth'
import LocalButton from '@/components/common/Button.vue'
</script>

<!-- NEW -->
<script setup>
import { useAuth, Button, Card, AppLayout } from '@shared'
</script>
```

**Files to Update** (12 views):
- [ ] `src/views/Dashboard.vue`
- [ ] `src/views/TripManagement.vue`
- [ ] `src/views/TripDetails.vue`
- [ ] `src/views/VehicleInspection.vue`
- [ ] `src/views/CargoManagement.vue`
- [ ] `src/views/PassengerManagement.vue`
- [ ] `src/views/IncidentReport.vue`
- [ ] `src/views/FuelLog.vue`
- [ ] `src/views/Communication.vue`
- [ ] `src/views/Notifications.vue`
- [ ] `src/views/Profile.vue`
- [ ] `src/views/Settings.vue`

#### Step 6: Update Router
**Action**: Ensure router uses auth from shared

**File**: `src/router/index.js`
- Update `useAuthStore` import to use `@shared`

#### Step 7: Clean Up
**Action**: Remove unused files

**Files to Delete**:
- Duplicate stores (auth.js, offline.js)
- Duplicate composables (5 files)
- Duplicate utils (frappeClient.js)
- Local layout components (if fully replaced)
- Local common components (if fully replaced)

#### Step 8: Test
**Action**: Verify functionality

**Tests**:
- [ ] `npm install` runs successfully
- [ ] `npm run dev` starts without errors
- [ ] App loads in browser
- [ ] Authentication works
- [ ] Navigation works
- [ ] Offline sync works
- [ ] Toast notifications appear
- [ ] All views render correctly
- [ ] Build completes: `npm run build`

---

## Current Progress

### ✅ Completed
1. Updated `package.json` with workspace dependency
2. Simplified `vite.config.js` using shared base
3. Updated `App.vue` with Toast and useOfflineSync

### 🚧 In Progress
4. Delete duplicate stores
5. Delete duplicate composables
6. Update view imports

### ⏳ Pending
7. Test full functionality
8. Build and deploy

---

## Import Patterns

### OLD Pattern (Local)
```vue
<script setup>
import { useAuthStore } from '@/stores/auth'
import { useOfflineStore } from '@/stores/offline'
import { useGeolocation } from '@/composables/useGeolocation'
import frappeClient from '@/utils/frappeClient'
import Button from '@/components/common/Button.vue'
</script>
```

### NEW Pattern (Shared)
```vue
<script setup>
import {
  // Stores/Composables
  useAuth,
  useOfflineSync,
  useGeolocation,
  useCamera,
  useToast,
  
  // Utils
  frappeClient,
  
  // Components
  AppLayout,
  Button,
  Input,
  Card,
  Modal,
  Loading
} from '@shared'

// Keep driver-specific stores
import { useTripStore } from '@/stores/trip'
import { useVehicleStore } from '@/stores/vehicle'
</script>
```

---

## Benefits After Migration

✅ **Reduced Code**: ~2,000+ lines of duplicate code removed  
✅ **Consistency**: Same UI/UX across all PWAs  
✅ **Maintainability**: Bug fixes in shared code benefit all PWAs  
✅ **Performance**: Better tree-shaking, smaller bundles  
✅ **Development Speed**: No need to reimplement common features  

---

## Next Phase After Driver Migration

Once driver-pwa migration is complete and tested:

1. **Operations PWA** - Create from scratch using shared code
2. **Safety PWA** - Create from scratch using shared code  
3. **Fleet PWA** - Create from scratch using shared code

Each new PWA will take ~2 hours instead of 2 weeks because of shared foundation!

---

*Migration started: October 14, 2025*
