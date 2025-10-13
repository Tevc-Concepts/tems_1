# TEMS Driver PWA - Quick Reference

## 🎯 One-Command Build & Deploy

```bash
cd /workspace/development/frappe-bench/apps/tems/frontend/driver-pwa
./build.sh
```

## 📍 Key Locations

| Item | Path |
|------|------|
| **Source Code** | `frappe-bench/apps/tems/frontend/driver-pwa/src/` |
| **Build Output** | `frappe-bench/apps/tems/tems/public/frontend/driver-pwa/dist/` |
| **Backend API** | `frappe-bench/apps/tems/tems/api/pwa/driver.py` |
| **Access URL** | `https://your-site.com/driver/` |

## 🔗 Important URLs

- **Dev Server**: http://localhost:5173
- **Preview Build**: http://localhost:4173
- **Production**: https://your-site.com/driver/

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Quick start guide |
| `IMPLEMENTATION.md` | Complete feature documentation |
| `DEPLOYMENT.md` | Setup & deployment instructions |
| `FILES_SUMMARY.md` | All files created/modified |

## 🛠️ Common Commands

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview build
npm run preview

# Run build script
./build.sh
```

## 🔌 API Endpoints

All endpoints: `/api/method/tems.api.pwa.driver.{function_name}`

### Core Operations
- `get_driver_dashboard()` - Dashboard data
- `start_trip()` - Start a trip
- `complete_trip()` - Complete a trip
- `send_sos_alert()` - Emergency SOS

### Cargo
- `get_cargo_consignments()` - Get cargo
- `scan_cargo_barcode()` - Scan barcode
- `update_delivery_status()` - Update delivery

### Passenger
- `get_passenger_manifest()` - Get passengers
- `scan_passenger_ticket()` - Scan ticket
- `update_boarding_status()` - Update boarding

### Communication
- `get_messages()` - Fetch messages
- `send_message()` - Send message
- `get_notifications()` - Get notifications

## 📱 Features Checklist

### ✅ Implemented
- [x] Authentication & Dashboard
- [x] Trip Management (Start/Complete)
- [x] Cargo Operations (Barcode)
- [x] Passenger Operations (Tickets)
- [x] Vehicle Inspection
- [x] Incident Reporting
- [x] SOS Emergency Button
- [x] Fuel Logging
- [x] Real-time Communication
- [x] Push Notifications
- [x] Offline Mode
- [x] GPS Tracking
- [x] Camera Capture
- [x] Settings & Preferences

## 🎨 Component Overview

### Common Components (9)
- EmptyState, LoadingSpinner, Modal, Toast
- CameraModal, SOSButton, StatusBadge
- OfflineIndicator

### Layout Components (3)
- AppLayout, AppHeader, AppBottomNav

### Feature Components
- TripCard, TripDetails, TripTimeline
- SpotCheckForm, PhotCapture
- IncidentReportForm

### Views (12)
- Dashboard, TripManagement, TripDetails
- CargoManagement, PassengerManagement
- VehicleInspection, IncidentReport
- FuelLog, Communication, Notifications
- Profile, Settings

## 🗂️ State Management (Pinia Stores)

| Store | Purpose |
|-------|---------|
| `auth` | Authentication & user |
| `trip` | Trip operations |
| `vehicle` | Vehicle data |
| `incident` | Incidents & SOS |
| `cargo` | Cargo operations |
| `passenger` | Passenger operations |
| `communication` | Messages & notifications |
| `offline` | Offline sync |

## 🧩 Composables

| Composable | Purpose |
|------------|---------|
| `useGeolocation` | GPS & location |
| `useMedia` | Camera & voice |
| `useNotifications` | Push notifications |
| `useCamera` | Camera utilities |
| `useOfflineSync` | Offline sync |

## 🎯 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| PWA won't install | Check HTTPS, service worker |
| API failing | Check CSRF token, session |
| Offline not working | Check IndexedDB, service worker |
| Camera not working | Needs HTTPS, permissions |

## 📊 Performance Targets

- First Paint: < 1.5s
- Interactive: < 3.5s
- Lighthouse PWA: > 90
- Bundle Size: < 500KB

## 🚀 Deployment Steps

1. **Build**: `./build.sh` or `npm run build`
2. **Restart**: `cd frappe-bench && bench restart`
3. **Cache**: `bench clear-cache`
4. **Test**: Visit `https://your-site.com/driver/`

## 🔐 Security Notes

- ✅ Session-based auth
- ✅ CSRF protection
- ✅ Employee validation
- ✅ Secure offline storage
- ✅ No sensitive logs

## 📞 Support

- **Technical Issues**: Check `IMPLEMENTATION.md`
- **Deployment Help**: Check `DEPLOYMENT.md`
- **API Reference**: See `tems/api/pwa/driver.py`

## ✨ Key Features

### Offline-First
- Works without internet
- Auto-sync when online
- Queue pending actions

### Mobile-Responsive
- 320px to 1920px
- Touch-optimized
- Bottom navigation

### PWA Features
- Installable app
- Push notifications
- Background sync
- Offline caching

### Safety
- Emergency SOS button
- GPS location sharing
- Incident reporting
- Photo/voice capture

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: October 13, 2025