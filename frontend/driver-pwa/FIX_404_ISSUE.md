# ✅ FIXED: Driver PWA Access Issue

## Problem
Getting 404 error when accessing `http://tems.local:8000/driver`:
```
"GET /assets/tems/frontend/driver-pwa/dist/index.js HTTP/1.1" 404
```

## Root Cause
The template file `tems/www/driver/index.html` was trying to load a non-existent `index.js` file. Vite builds create hashed filenames like `index-PcK2SAYs.js` for cache busting.

## Solution Applied

### 1. Updated Template
**File**: `tems/www/driver/index.html`

Changed from:
```html
<script type="module" src="/assets/tems/frontend/driver-pwa/dist/index.js"></script>
```

To:
```html
<link rel="stylesheet" href="/assets/tems/frontend/driver-pwa/dist/assets/index-BootKDzc.css">
<script type="module" src="/assets/tems/frontend/driver-pwa/dist/assets/index-PcK2SAYs.js"></script>
<script src="/assets/tems/frontend/driver-pwa/dist/registerSW.js"></script>
```

### 2. Created Auto-Update Script
**File**: `update-template.sh`

This script automatically extracts the correct asset hashes from the build output and updates the Frappe template.

### 3. Enhanced Build Script
**File**: `build.sh`

Now automatically runs `update-template.sh` after each build to keep the template in sync.

## File Structure

```
tems/
├── www/
│   └── driver/
│       ├── index.html ← Frappe template (Jinja)
│       └── index.py   ← Python controller
│
└── public/
    └── frontend/
        └── driver-pwa/
            └── dist/
                ├── assets/
                │   ├── index-PcK2SAYs.js  ← Main bundle (hashed)
                │   └── index-BootKDzc.css ← Styles (hashed)
                ├── manifest.webmanifest
                ├── sw.js
                └── registerSW.js
```

## How to Use

### Build & Deploy
```bash
cd /workspace/development/frappe-bench/apps/tems/frontend/driver-pwa
./build.sh
```

This will:
1. Build the PWA
2. Auto-update the Frappe template
3. Show next steps

### Clear Cache
```bash
cd /workspace/development/frappe-bench
bench --site tems.local clear-cache
bench --site tems.local clear-website-cache
```

### Access
Visit: **http://tems.local:8000/driver**

## Verification

Check if assets are loading:
```bash
# Check CSS
curl -I http://tems.local:8000/assets/tems/frontend/driver-pwa/dist/assets/index-BootKDzc.css

# Check JS
curl -I http://tems.local:8000/assets/tems/frontend/driver-pwa/dist/assets/index-PcK2SAYs.js
```

Should return `200 OK` for both.

## Future Rebuilds

**Important**: After each rebuild, the asset hash changes!

### Manual Method
1. Build: `npm run build`
2. Check new hashes in: `tems/public/frontend/driver-pwa/dist/index.html`
3. Update: `tems/www/driver/index.html` manually
4. Clear cache

### Automatic Method (Recommended)
1. Build: `./build.sh` (includes auto-update)
2. Clear cache
3. Done!

## Status
✅ **RESOLVED**

- Asset paths corrected
- Auto-update script created
- Build process enhanced
- Ready for use at `http://tems.local:8000/driver`

---

**Date Fixed**: October 14, 2025
**Current Hash**: PcK2SAYs (JS), BootKDzc (CSS)
