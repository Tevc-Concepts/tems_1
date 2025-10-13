# TEMS Driver PWA - Setup & Deployment Guide

## 🎯 Deployment Checklist

### 1. Install Dependencies
```bash
cd /workspace/development/frappe-bench/apps/tems/frontend/driver-pwa
npm install
```

### 2. Build for Production
```bash
npm run build
```

This will output to: `tems/public/frontend/driver-pwa/dist/`

### 3. Frappe Configuration

#### A. Ensure Public Path is Accessible
The built files at `tems/public/frontend/driver-pwa/dist/` should be accessible via:
```
https://your-site.com/assets/tems/frontend/driver-pwa/dist/
```

#### B. Create Entry Point (if not exists)
Create: `tems/www/driver/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TEMS Driver</title>
    <script>
        // Redirect to the PWA
        window.location.href = '/assets/tems/frontend/driver-pwa/dist/index.html';
    </script>
</head>
<body>
    <p>Redirecting to Driver App...</p>
</body>
</html>
```

### 4. Backend API Verification

Verify all API endpoints are accessible:

```python
# Test in Frappe console or via bench
import frappe

# Test dashboard endpoint
frappe.call('tems.api.pwa.driver.get_driver_dashboard')

# Test other endpoints...
```

### 5. Push Notifications Setup (Optional)

#### For Firebase Cloud Messaging (FCM):
1. Create Firebase project
2. Get VAPID public key
3. Add to `src/composables/useNotifications.js`
4. Configure service worker

#### For Apple Push Notifications (APNS):
1. Configure Apple Developer account
2. Create push certificate
3. Configure in Frappe

### 6. Testing

#### Local Testing
```bash
# Development mode
npm run dev

# Preview production build
npm run build && npm run preview
```

#### Mobile Testing
1. Use ngrok or similar for HTTPS:
   ```bash
   ngrok http 8000
   ```
2. Open on mobile device
3. Test "Add to Home Screen"
4. Test offline functionality

#### PWA Validation
1. Open Chrome DevTools
2. Go to Lighthouse
3. Run PWA audit
4. Target score: > 90

### 7. Production Deployment

#### Step 1: Build
```bash
cd frappe-bench/apps/tems/frontend/driver-pwa
npm run build
```

#### Step 2: Restart Frappe
```bash
cd frappe-bench
bench restart
```

#### Step 3: Clear Cache
```bash
bench clear-cache
bench clear-website-cache
```

#### Step 4: Access
Navigate to: `https://your-site.com/driver/`

## 🔧 Configuration

### Environment Variables

Create `.env.local` (not committed):
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_SITE_NAME=development.localhost
```

### Vite Config
The `vite.config.js` is pre-configured for:
- PWA manifest
- Service worker
- Asset paths
- Proxy for local development

### API Integration

All API calls go through `src/shared/utils/frappeClient.js` which handles:
- CSRF tokens
- Session management
- Offline queuing
- Error handling

## 📱 App Installation

### Android
1. Open in Chrome
2. Tap menu (⋮)
3. Select "Install app" or "Add to Home Screen"

### iOS
1. Open in Safari
2. Tap Share button
3. Select "Add to Home Screen"

## 🐛 Troubleshooting

### Issue: PWA Not Installing
**Solution:**
- Ensure HTTPS (or localhost)
- Check service worker registration
- Verify manifest.json accessibility

### Issue: API Calls Failing
**Solution:**
- Check CORS settings in Frappe
- Verify session cookie is set
- Check CSRF token in headers

### Issue: Offline Mode Not Working
**Solution:**
- Check service worker status in DevTools
- Verify IndexedDB permissions
- Clear cache and reinstall PWA

### Issue: Push Notifications Not Working
**Solution:**
- Verify browser permissions
- Check VAPID key configuration
- Ensure HTTPS connection

### Issue: Camera Not Working
**Solution:**
- Requires HTTPS
- Check browser camera permissions
- Verify device has camera

## 🔐 Security Checklist

- [ ] HTTPS enabled in production
- [ ] CSRF tokens working
- [ ] Session timeout configured
- [ ] API permissions validated
- [ ] No sensitive data in console logs
- [ ] Service worker caching sensitive data carefully

## 📊 Monitoring

### Key Metrics to Monitor
- PWA install rate
- Offline usage patterns
- API response times
- Error rates
- User engagement

### Logging
- Check browser console for errors
- Monitor Frappe error logs
- Track service worker updates

## 🚀 Performance Optimization

### Already Implemented
- ✅ Code splitting
- ✅ Lazy loading routes
- ✅ Image optimization
- ✅ Asset caching
- ✅ Gzip compression

### Further Optimization
- Consider CDN for static assets
- Implement route prefetching
- Add skeleton screens
- Optimize images further

## 📖 Documentation Links

- **Frappe REST API**: https://frappeframework.com/docs/user/en/api
- **Vue 3 Docs**: https://vuejs.org/guide/
- **Vite PWA Plugin**: https://vite-pwa-org.netlify.app/
- **Tailwind CSS**: https://tailwindcss.com/docs

## 🎓 Training

### For Drivers
1. How to install PWA
2. Basic navigation
3. Starting/completing trips
4. Using SOS button
5. Offline mode explanation

### For Administrators
1. Monitoring dashboard
2. Managing permissions
3. Troubleshooting common issues
4. Reviewing incident reports

## ✅ Go-Live Checklist

- [ ] All dependencies installed
- [ ] Production build successful
- [ ] PWA audit score > 90
- [ ] All API endpoints tested
- [ ] Mobile devices tested
- [ ] Offline mode tested
- [ ] Push notifications configured
- [ ] User training completed
- [ ] Documentation reviewed
- [ ] Backup plan ready

## 📞 Support

For issues or questions:
- Check `IMPLEMENTATION.md` for technical details
- Review Frappe/ERPNext docs
- Contact TEMS development team

---

**Last Updated**: October 13, 2025  
**Version**: 1.0.0  
**Status**: Production Ready