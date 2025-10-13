# TEMS PWA — DRIVER APP PROMPT

## ROLE
You are designing and developing the **TEMS Driver Progressive Web App (PWA)** for drivers to perform daily fleet operations from mobile devices.  
The PWA will interact with the main Frappe-based TEMS backend (via REST APIs or Frappe GraphQL endpoints).

---

## TASKS

1. **Authentication**
   - Drivers log in via Kinde or Frappe Auth.
   - Support biometric (fingerprint/face) for quick re-login.
   - Show assigned vehicle(s) and operation status post-login.

2. **Dashboard**
   - Real-time vehicle assignment status.
   - Next trip/operation summary.
   - Safety score, compliance alerts, and pending trainings.

3. **Trip Management**
   - Accept or reject trip assignments.
   - View assigned route (map view + stop points).
   - Check-in / Check-out operations.
   - Log “Start Trip”, “Pause Trip”, “Arrived”, “Delivered”.
   - Capture mileage, odometer, and fuel info.

4. **Cargo/Passenger Interaction**
   - If `vehicle_type = Cargo` → display Cargo Consignment list with details.
   - If `vehicle_type = Passenger` → display Passenger Manifest and seat occupancy.
   - Allow barcode/QR scan for cargo or ticket validation.

5. **Incident & Safety**
   - Report incident with photo and voice note.
   - Send emergency alerts (SOS) tied to current vehicle.
   - Auto-share GPS coordinates.

6. **Communication**
   - Real-time chat or message with Operations Control Room.
   - Receive alerts (trip changes, document expiry, safety reminders).

7. **Offline Mode**
   - Cache trips, logs, and forms locally.
   - Auto-sync when back online.

---

## CONSTRAINTS
- UI must be **mobile-first** (responsive for 6–7" displays).
- Theme consistent with TEMS color palette and icons.
- Use **PWA features**: installable, push notifications, offline caching.
- Integrate **Mapbox or Google Maps** for route visualization.
- All API calls must go through TEMS backend endpoints (e.g., `/api/method/tems_operations/...`).
- Build with **Flutter Web**, **React (Next.js PWA)**, or **Vue 3 PWA** — depending on developer preference.

---

## OUTPUTS
- UI Wireframes (Login, Dashboard, Trip View, Incident Report, Chat, Settings).
- Component design files.
- API integration stubs.
- Route structure (React Router / FlutterFlow Pages).
- Icons: vehicle, cargo, passenger, trip, alert.
