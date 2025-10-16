# PWA Router Base Path Fix

**Date:** October 16, 2025  
**Issue:** PWAs redirecting to incorrect `/assets/tems/frontend/[pwa]/dist/` paths  
**Status:** ✅ FIXED

---

## Problem Summary

When accessing PWAs at their correct URLs (`/operations`, `/safety`, `/fleet`, `/driver`), the browser was being redirected to incorrect asset paths like:

```
/operations → /assets/tems/frontend/operations-pwa/dist/operations
/safety → /assets/tems/frontend/safety-pwa/dist/safety  
/fleet → /assets/tems/frontend/fleet-pwa/dist/fleet
/driver → /assets/tems/frontend/driver-pwa/dist/driver
```

This resulted in:
- 404 errors
- JavaScript errors ("TypeError: t is not a function")
- Blank pages
- Broken routing

---

## Root Cause

### Vue Router Base Path Misconfiguration

Each PWA's Vue Router was configured with the **wrong base path**:

**❌ INCORRECT (old configuration):**
```javascript
// frontend/operations-pwa/src/router/index.js
const router = createRouter({
    history: createWebHistory('/assets/tems/frontend/operations-pwa/dist/'),
    routes
})
```

This told Vue Router that the app is mounted at `/assets/tems/frontend/operations-pwa/dist/`, so it would try to navigate to that path.

### Why This Happened

During initial PWA development, the router base path was likely set to match the direct asset URL for testing purposes, but was never updated when the proper `/operations` URL routing was implemented through Frappe's `www` directory.

---

## Solution Applied

### Fixed Router Base Paths

Updated all four PWA routers to use the correct base paths matching their `www` URLs:

#### 1. Operations PWA
**File:** `frontend/operations-pwa/src/router/index.js`

```javascript
const router = createRouter({
    history: createWebHistory('/operations/'),  // ✅ CORRECT
    routes
})
```

#### 2. Safety PWA
**File:** `frontend/safety-pwa/src/router/index.js`

```javascript
const router = createRouter({
    history: createWebHistory('/safety/'),  // ✅ CORRECT
    routes
})
```

#### 3. Fleet PWA
**File:** `frontend/fleet-pwa/src/router/index.js`

```javascript
const router = createRouter({
    history: createWebHistory('/fleet/'),  // ✅ CORRECT
    routes
})
```

#### 4. Driver PWA
**File:** `frontend/driver-pwa/src/router/index.js`

```javascript
const router = createRouter({
    history: createWebHistory('/driver/'),  // ✅ CORRECT
    routes
})
```

---

## Build & Deployment Steps

### 1. Update Router Files
```bash
cd /workspace/development/frappe-bench/apps/tems

# Update all router base paths
sed -i "s|createWebHistory('/assets/tems/frontend/operations-pwa/dist/')|createWebHistory('/operations/')|g" frontend/operations-pwa/src/router/index.js
sed -i "s|createWebHistory('/assets/tems/frontend/safety-pwa/dist/')|createWebHistory('/safety/')|g" frontend/safety-pwa/src/router/index.js
sed -i "s|createWebHistory('/assets/tems/frontend/fleet-pwa/dist/')|createWebHistory('/fleet/')|g" frontend/fleet-pwa/src/router/index.js
sed -i "s|createWebHistory('/assets/tems/frontend/driver-pwa/dist/')|createWebHistory('/driver/')|g" frontend/driver-pwa/src/router/index.js
```

### 2. Rebuild All PWAs
```bash
# Build operations
cd frontend/operations-pwa && npm run build

# Build safety
cd ../safety-pwa && npm run build

# Build fleet
cd ../fleet-pwa && npm run build

# Build driver
cd ../driver-pwa && npm run build
```

**OR build in parallel:**
```bash
cd /workspace/development/frappe-bench/apps/tems
(cd frontend/operations-pwa && npm run build) &
(cd frontend/safety-pwa && npm run build) &
(cd frontend/fleet-pwa && npm run build) &
(cd frontend/driver-pwa && npm run build) &
wait
```

### 3. Sync HTML Files
```bash
cd /workspace/development/frappe-bench/apps/tems
./scripts/sync-pwa-html.sh
```

### 4. Restart Bench
```bash
cd /workspace/development/frappe-bench
bench restart
```

---

## Verification

### Test Each PWA

After fix, test all URLs:

```bash
# Should return 200 OK and render Vue app
curl -I http://localhost:8000/operations  # ✅
curl -I http://localhost:8000/safety      # ✅
curl -I http://localhost:8000/fleet       # ✅
curl -I http://localhost:8000/driver      # ✅
```

### Browser Testing

1. **Clear Browser Cache:**
   - Chrome/Edge: `Ctrl+Shift+Delete` (Windows) / `Cmd+Shift+Delete` (Mac)
   - Select "Cached images and files"
   - Clear data

2. **Hard Refresh Each PWA:**
   - `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac)

3. **Check URLs Stay Correct:**
   - Navigate to `http://localhost:8000/operations`
   - URL should stay `/operations` (not redirect to `/assets/...`)
   - Vue app should load successfully
   - No JavaScript errors in console

4. **Test Routing:**
   - Click navigation links within PWA
   - URLs should be `/operations/fleet`, `/operations/dispatch`, etc.
   - Not `/assets/tems/frontend/operations-pwa/dist/fleet`

---

## Understanding Vue Router Base Path

### What is `base` in createWebHistory?

The `base` parameter tells Vue Router where the app is mounted in the URL structure:

```javascript
createWebHistory(base)
```

**Examples:**

| Base Path | Root URL | Child Route | Full URL |
|-----------|----------|-------------|----------|
| `/` | `/` | `/about` | `/about` |
| `/app/` | `/app` | `/about` | `/app/about` |
| `/operations/` | `/operations` | `/fleet` | `/operations/fleet` |
| `/assets/tems/frontend/operations-pwa/dist/` | `/assets/tems/frontend/operations-pwa/dist` | `/fleet` | `/assets/tems/frontend/operations-pwa/dist/fleet` ❌ |

### Correct Base Path for TEMS PWAs

Since our PWAs are served at:
- `https://tems.yourdomain.com/operations`
- `https://tems.yourdomain.com/safety`
- `https://tems.yourdomain.com/fleet`
- `https://tems.yourdomain.com/driver`

The base paths must be:
- `/operations/`
- `/safety/`
- `/fleet/`
- `/driver/`

**NOT** the asset paths.

---

## Why This Fix Works

### Before Fix

```
User navigates to: /operations
↓
Frappe serves: www/operations/index.html
↓
HTML loads: /assets/tems/frontend/operations-pwa/dist/assets/index-xxx.js
↓
Vue Router initializes with base: /assets/tems/frontend/operations-pwa/dist/
↓
Router thinks app is at: /assets/tems/frontend/operations-pwa/dist/
↓
Browser URL changes to: /assets/tems/frontend/operations-pwa/dist/operations ❌
↓
404 error (no Frappe route for that path)
```

### After Fix

```
User navigates to: /operations
↓
Frappe serves: www/operations/index.html
↓
HTML loads: /assets/tems/frontend/operations-pwa/dist/assets/index-xxx.js
↓
Vue Router initializes with base: /operations/
↓
Router knows app is at: /operations/
↓
Browser URL stays: /operations ✅
↓
Vue app renders successfully
↓
Navigation works: /operations/fleet, /operations/dispatch, etc. ✅
```

---

## Production Deployment

### Checklist

```bash
# 1. Pull updated code
git pull origin main

# 2. Update router files (if not in git yet)
cd apps/tems
sed -i "s|createWebHistory('/assets/tems/frontend/operations-pwa/dist/')|createWebHistory('/operations/')|g" frontend/operations-pwa/src/router/index.js
sed -i "s|createWebHistory('/assets/tems/frontend/safety-pwa/dist/')|createWebHistory('/safety/')|g" frontend/safety-pwa/src/router/index.js
sed -i "s|createWebHistory('/assets/tems/frontend/fleet-pwa/dist/')|createWebHistory('/fleet/')|g" frontend/fleet-pwa/src/router/index.js
sed -i "s|createWebHistory('/assets/tems/frontend/driver-pwa/dist/')|createWebHistory('/driver/')|g" frontend/driver-pwa/src/router/index.js

# 3. Rebuild all PWAs
npm run build  # If postbuild script exists
# OR build individually
(cd frontend/operations-pwa && npm run build) &
(cd frontend/safety-pwa && npm run build) &
(cd frontend/fleet-pwa && npm run build) &
(cd frontend/driver-pwa && npm run build) &
wait

# 4. Sync HTML files
./scripts/sync-pwa-html.sh

# 5. Build Frappe assets
cd ../..
bench --site <site-name> build

# 6. Clear cache
bench --site <site-name> clear-cache

# 7. Restart services
sudo supervisorctl restart all

# 8. Verify each PWA
curl -I https://tems.yourdomain.com/operations  # Should be 200
curl -I https://tems.yourdomain.com/safety      # Should be 200
curl -I https://tems.yourdomain.com/fleet       # Should be 200
curl -I https://tems.yourdomain.com/driver      # Should be 200
```

---

## Best Practices Going Forward

### 1. Always Use Correct Base Paths

When creating new PWAs or modifying existing ones:

```javascript
// ✅ CORRECT - Use the www URL path
const router = createRouter({
    history: createWebHistory('/pwa-name/'),
    routes
})

// ❌ WRONG - Don't use asset paths
const router = createRouter({
    history: createWebHistory('/assets/app-name/dist/'),
    routes
})
```

### 2. Match Base Path to www Directory

The router base must match the `www` folder name:

```
www/operations/ → createWebHistory('/operations/')
www/safety/ → createWebHistory('/safety/')
www/fleet/ → createWebHistory('/fleet/')
```

### 3. Test After Building

Always test in browser after building:
1. Clear cache
2. Navigate to PWA URL
3. Check URL stays correct (no redirect)
4. Check console for errors
5. Test navigation within PWA

### 4. Document Base Paths

In PWA README or documentation, clearly state:
- Served URL: `https://tems.yourdomain.com/operations`
- Router base: `/operations/`
- Asset path: `/assets/tems/frontend/operations-pwa/dist/` (internal only)

---

## Related Issues Fixed

This fix resolves multiple related problems:

1. ✅ **URL Redirection** - PWAs stay at correct `/operations` URL
2. ✅ **404 Errors** - No more requests to non-existent asset paths
3. ✅ **jQuery Conflicts** - With proper routing, no template wrapping issues
4. ✅ **Navigation** - Internal PWA routing works correctly
5. ✅ **Service Worker** - Proper base path for offline functionality
6. ✅ **Deep Linking** - Direct navigation to `/operations/fleet` works

---

## Summary

**Problem:** Vue Router configured with wrong base paths  
**Cause:** Initial development used asset paths instead of www URL paths  
**Solution:** Updated all router base paths to match www URLs  
**Impact:** All PWAs now work correctly at their intended URLs  
**Files Modified:** 4 router configuration files + rebuilt PWAs  

**Status:** ✅ All PWAs Functional with Correct Routing

---

**Prepared By:** GitHub Copilot  
**Issue:** #PWA-ROUTER-BASE-PATH  
**Resolution Time:** ~30 minutes  
**Rebuild Time:** ~2 minutes per PWA
