# TEMS Driver PWA - Access Guide

## 🌐 Access URLs

### Development
- **URL**: http://tems.local:8000/driver
- **Alternative**: http://localhost:8000/driver

### Production
- **URL**: https://your-domain.com/driver

## 📁 File Structure

```
tems/
├── www/
│   └── driver/
│       ├── index.html     # Main entry page (Jinja template)
│       └── index.py       # Python context controller
├── public/
│   └── frontend/
│       └── driver-pwa/
│           └── dist/      # Built PWA files
│               ├── index.html (not used)
│               ├── assets/
│               │   ├── index-PcK2SAYs.js  (main bundle)
│               │   └── index-BootKDzc.css  (styles)
│               ├── manifest.webmanifest
│               ├── sw.js  (service worker)
│               └── registerSW.js
```

## 🔧 How It Works

1. **User visits** `http://tems.local:8000/driver`
2. **Frappe routes** to `tems/www/driver/index.html`
3. **index.html** (Jinja template) loads:
   - CSS: `/assets/tems/frontend/driver-pwa/dist/assets/index-BootKDzc.css`
   - JS: `/assets/tems/frontend/driver-pwa/dist/assets/index-PcK2SAYs.js`
   - Service Worker: `registerSW.js`
4. **Vue app** mounts to `<div id="app"></div>`
5. **PWA** is ready to use!

## ⚠️ Important Notes

### Asset Hashing
The built files have content hashes in their names (e.g., `index-PcK2SAYs.js`). 

**After each rebuild**, you must update `www/driver/index.html` with new hash values from `public/frontend/driver-pwa/dist/index.html`.

### Automated Update Script
Create a post-build script to automatically update the Jinja template:

```bash
#!/bin/bash
# update-driver-template.sh

SRC_HTML="/workspace/development/frappe-bench/apps/tems/tems/public/frontend/driver-pwa/dist/index.html"
DEST_HTML="/workspace/development/frappe-bench/apps/tems/tems/www/driver/index.html"

# Extract asset paths from build
CSS_PATH=$(grep -oP '(?<=href=")[^"]*index-[^"]*\.css' $SRC_HTML)
JS_PATH=$(grep -oP '(?<=src=")[^"]*index-[^"]*\.js' $SRC_HTML | head -1)

echo "Updating template with:"
echo "  CSS: $CSS_PATH"
echo "  JS: $JS_PATH"

# Update template (would need proper sed commands)
```

### Manual Update Process
1. Run `npm run build`
2. Open `tems/public/frontend/driver-pwa/dist/index.html`
3. Copy asset filenames (the hashed parts)
4. Update `tems/www/driver/index.html` with new filenames
5. Run `bench clear-cache`

## 🔄 After Updates

Always run after making changes:
```bash
cd /workspace/development/frappe-bench
bench --site tems.local clear-cache
bench --site tems.local clear-website-cache
```

## 🐛 Troubleshooting

### 404 on assets
- Check asset filenames match in index.html
- Verify files exist in `tems/public/frontend/driver-pwa/dist/assets/`
- Clear browser cache (Ctrl+F5)

### Blank page
- Check browser console for errors
- Verify service worker is not causing issues
- Try in incognito mode

### Changes not reflecting
- Clear Frappe cache: `bench --site tems.local clear-cache`
- Clear browser cache
- Restart bench if needed: `bench restart`

## 📱 PWA Installation

1. Visit `http://tems.local:8000/driver` on mobile
2. Look for "Add to Home Screen" prompt
3. Install the PWA
4. Open from home screen icon

## 🎯 Next Steps

1. ✅ Build completed successfully
2. ✅ Assets deployed to correct location
3. ✅ Template updated with asset paths
4. ⏳ Test on mobile devices
5. ⏳ Create PWA icons (192x192, 512x512)
6. ⏳ Set up push notifications
7. ⏳ Production SSL certificate

---

**Status**: ✅ Ready for Testing
**Last Build**: October 13, 2025
**Build Hash**: PcK2SAYs (JS), BootKDzc (CSS)
