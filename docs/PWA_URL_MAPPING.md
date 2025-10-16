# TEMS PWA URL Mapping

**TEMS Platform - PWA Access Configuration**  
**Version:** 1.0  
**Date:** October 16, 2025

---

## Overview

All TEMS Progressive Web Applications (PWAs) are accessed through clean, integrated URLs under the main TEMS domain. The PWAs are properly integrated with the Frappe/ERPNext TEMS app using the `www` directory structure.

---

## PWA Access URLs

### Production URLs

| PWA | User Role | Access URL | www Path |
|-----|-----------|------------|----------|
| **Operations** | Operations Manager | `https://tems.yourdomain.com/operations` | `tems/www/operations/` |
| **Safety** | Safety Officer | `https://tems.yourdomain.com/safety` | `tems/www/safety/` |
| **Fleet** | Fleet Manager | `https://tems.yourdomain.com/fleet` | `tems/www/fleet/` |
| **Driver** | Driver | `https://tems.yourdomain.com/driver` | `tems/www/driver/` |

### Development/Local URLs

| PWA | Local Access URL |
|-----|------------------|
| **Operations** | `http://localhost:8000/operations` |
| **Safety** | `http://localhost:8000/safety` |
| **Fleet** | `http://localhost:8000/fleet` |
| **Driver** | `http://localhost:8000/driver` |

---

## Architecture

### URL Routing

The Frappe framework automatically routes URLs to the `www` directory:

```
Request: https://tems.yourdomain.com/operations
         ↓
Frappe Router
         ↓
Looks for: apps/tems/tems/www/operations/index.html
         ↓
Loads: index.html + index.py (context)
         ↓
HTML loads: /assets/tems/frontend/operations-pwa/dist/assets/index.js
         ↓
PWA Application Rendered
```

### Directory Structure

```
apps/tems/
├── tems/
│   ├── www/                          # Web-accessible pages
│   │   ├── operations/
│   │   │   ├── index.html           # Entry point HTML
│   │   │   └── index.py             # Server-side context
│   │   ├── safety/
│   │   │   ├── index.html
│   │   │   └── index.py
│   │   ├── fleet/
│   │   │   ├── index.html
│   │   │   └── index.py
│   │   └── driver/
│   │       ├── index.html
│   │       └── index.py
│   └── public/
│       └── frontend/                 # Built PWA assets
│           ├── operations-pwa/dist/
│           ├── safety-pwa/dist/
│           ├── fleet-pwa/dist/
│           └── driver-pwa/dist/
```

---

## Implementation Details

### 1. Entry Point HTML Files

Each PWA has an `index.html` file that:
- Sets appropriate meta tags (viewport, theme-color, PWA capabilities)
- References the PWA manifest
- Loads the compiled JavaScript bundle from `/assets/tems/frontend/`

**Example: `tems/www/operations/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0284c7">
    <title>TEMS Operations</title>
    <link rel="manifest" href="/assets/tems/frontend/operations-pwa/dist/manifest.webmanifest">
</head>
<body>
    <div id="app"></div>
    <script type="module" src="/assets/tems/frontend/operations-pwa/dist/assets/index.js"></script>
</body>
</html>
```

### 2. Server-Side Context (Python)

Each PWA has an `index.py` file that:
- Provides server-side context to the template
- Can enforce authentication (currently disabled for PWA-based auth)
- Sets cache and breadcrumb options

**Example: `tems/www/operations/index.py`**
```python
import frappe
from frappe import _

def get_context(context):
    """Context for operations portal page"""
    context.no_cache = 1
    context.no_breadcrumbs = True
    
    # Authentication handled by PWA
    # Uncomment to enforce server-side login
    # if frappe.session.user == "Guest":
    #     frappe.local.flags.redirect_location = "/login?redirect-to=/operations"
    #     raise frappe.Redirect
    
    return context
```

### 3. Asset Loading

Built PWA assets are served from:
```
/assets/tems/frontend/<pwa-name>/dist/
```

These are automatically available because:
1. Files in `tems/public/` are served at `/assets/tems/`
2. Frappe's build system compiles and places assets in `public/frontend/`
3. The `bench build` command processes all frontend assets

---

## Authentication Flow

### Current Implementation

**Client-Side Authentication (PWA-Based):**
1. User navigates to clean URL (e.g., `/operations`)
2. HTML page loads immediately (no server auth check)
3. PWA JavaScript initializes
4. PWA checks for session via API call
5. If no session, PWA redirects to login screen
6. After login, API returns session token
7. PWA stores token and proceeds

**Advantages:**
- Fast initial load (no server redirect)
- Better PWA experience
- Offline-friendly architecture
- Consistent with modern SPAs

### Optional Server-Side Authentication

To enable server-side authentication enforcement, uncomment the following in each `index.py`:

```python
if frappe.session.user == "Guest":
    frappe.local.flags.redirect_location = "/login?redirect-to=/operations"
    raise frappe.Redirect
```

**When to Use:**
- Stricter security requirements
- Enterprise SSO integration
- Prevent HTML page access before authentication

---

## Build & Deployment

### Building PWAs

```bash
# Build all PWAs
cd apps/tems
npm run build

# Or build individually
cd apps/tems/frontend/operations-pwa && npm run build
cd apps/tems/frontend/safety-pwa && npm run build
cd apps/tems/frontend/fleet-pwa && npm run build
cd apps/tems/frontend/driver-pwa && npm run build
```

### Deploying to Production

```bash
# Build assets
bench --site <site-name> build

# Clear cache
bench --site <site-name> clear-cache

# Restart services
sudo supervisorctl restart all
```

---

## URL Configuration

### Setting Your Domain

Replace `yourdomain.com` with your actual domain in:

1. **Production Environment:**
   - DNS: Point domain to server IP
   - Nginx: Configure server_name
   - SSL: Install certificate for domain
   - Frappe: Set site_config.json `host_name`

2. **User Documentation:**
   - Update all user guides with actual domain
   - Provide bookmarks or shortcuts
   - Include in onboarding materials

### Multi-Site Setup

If running multiple sites on same server:

```
Site 1: https://company1.example.com/operations
Site 2: https://company2.example.com/operations
```

Each site accesses the same app code but separate databases.

---

## Testing URLs

### Manual Testing

```bash
# Test each URL returns HTML page
curl http://localhost:8000/operations
curl http://localhost:8000/safety
curl http://localhost:8000/fleet
curl http://localhost:8000/driver

# Test PWA assets are accessible
curl http://localhost:8000/assets/tems/frontend/operations-pwa/dist/manifest.webmanifest
```

### Browser Testing

1. Open each URL in browser
2. Check network tab for successful asset loading
3. Verify service worker registration (DevTools → Application → Service Workers)
4. Test offline functionality (DevTools → Network → Offline)
5. Test on mobile devices

---

## Troubleshooting

### Issue: 404 Error on PWA URL

**Cause:** Frappe not finding www directory files

**Solution:**
```bash
# Verify files exist
ls -la apps/tems/tems/www/operations/

# Rebuild and restart
bench --site <site-name> build
bench restart
```

### Issue: Assets Not Loading

**Cause:** Built assets missing or incorrect paths

**Solution:**
```bash
# Verify assets exist
ls -la apps/tems/tems/public/frontend/operations-pwa/dist/

# Rebuild PWAs
cd apps/tems
npm run build

# Rebuild bench assets
bench --site <site-name> build
```

### Issue: Blank Page Loads

**Cause:** JavaScript errors or API connection issues

**Solution:**
1. Open browser DevTools Console
2. Check for errors
3. Verify API endpoint URLs in PWA config
4. Check CORS settings if API on different domain

---

## Best Practices

### 1. Clean URLs
✅ **DO:** Use clean, memorable URLs (`/operations`, `/safety`)  
❌ **DON'T:** Use long asset paths in documentation

### 2. Consistent Naming
- URL path matches `www` directory name
- PWA build output directory matches URL context
- Clear relationship between URL and functionality

### 3. Documentation
- Always document user-facing URLs in user guides
- Keep internal asset paths in technical docs only
- Update documentation when URLs change

### 4. Security
- Use HTTPS in production
- Implement proper authentication
- Set secure headers in Nginx
- Enable CORS only for necessary domains

---

## Mobile App Integration

### Add to Home Screen

Users can install PWAs as apps:

**iOS (Safari):**
1. Visit PWA URL
2. Tap Share button
3. Tap "Add to Home Screen"
4. Icon appears on home screen

**Android (Chrome):**
1. Visit PWA URL
2. Chrome shows "Add to Home Screen" banner
3. Or tap menu → "Install app"
4. Icon appears in app drawer

**Result:** App launches in standalone mode without browser UI

---

## Migration Notes

### From Old URLs to New URLs

If you previously documented or communicated different URLs:

**Old Format (INCORRECT):**
```
https://tems.yourdomain.com/assets/tems/frontend/operations-pwa/dist/index.html
```

**New Format (CORRECT):**
```
https://tems.yourdomain.com/operations
```

**Migration Steps:**
1. ✅ Update all user documentation (COMPLETED)
2. Communicate URL change to users
3. Consider adding redirects (optional)
4. Update bookmarks and links
5. Update onboarding materials

**Redirect Setup (Optional):**
Can add in `hooks.py` if needed:
```python
website_redirects = [
    {"source": "/assets/tems/frontend/operations-pwa/dist/index.html", "target": "/operations"},
    # ... add others
]
```

---

## Summary

✅ All PWAs accessible via clean URLs under main domain  
✅ Proper integration with Frappe `www` directory  
✅ Built assets served from `/assets/tems/frontend/`  
✅ Authentication handled by PWA (optional server-side)  
✅ All user documentation updated with correct URLs  
✅ Mobile-friendly and installable as apps  

**Access URLs:**
- Operations: `https://tems.yourdomain.com/operations`
- Safety: `https://tems.yourdomain.com/safety`
- Fleet: `https://tems.yourdomain.com/fleet`
- Driver: `https://tems.yourdomain.com/driver`

---

**Document Version:** 1.0  
**Last Updated:** October 16, 2025  
**Maintained By:** TEMS Technical Team
