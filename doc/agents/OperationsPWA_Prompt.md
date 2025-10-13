# TEMS PWA — OPERATIONS CONTROL APP PROMPT

## ROLE
You are designing the **Operations Manager PWA** — a control and coordination interface for managing daily vehicle movements, driver assignments, and logistics flow.

---

## TASKS

1. **Authentication**
   - Kinde / Frappe login (role = Operations Manager).
   - Role-based workspace.

2. **Dashboard**
   - Fleet overview (active, idle, maintenance).
   - Trip tracking (live map view with vehicle pins).
   - Alerts for delays, diversions, or incidents.
   - KPIs: On-Time %, Distance Covered, Cost per Km.

3. **Trip Planning**
   - Create and schedule Operation Plans.
   - Assign Vehicles + Drivers.
   - For Cargo: attach Consignments.
   - For Passenger: attach Passenger Trips.
   - Approve or reschedule trips.

4. **Live Operations Control**
   - View trip status in real-time.
   - Send broadcast or private messages to drivers.
   - Acknowledge incidents or route deviations.
   - Log route diversions and vehicle swaps.

5. **Analytics & Reporting**
   - Vehicle performance dashboard.
   - Trip cost/revenue summary.
   - Vehicle profitability (Cargo vs Passenger).
   - Daily Movement Log summary.

---

## CONSTRAINTS
- PWA must load on tablets and desktops.
- Support push notifications for trip updates and incident alerts.
- Integrate live GPS feed from Driver App.
- Use dark/light themes.
- Respect existing TEMS backend data model (Vehicle, Operation Plan, Consignment, Trip, Movement Log).

---

## OUTPUTS
- UI Pages: Dashboard, Trip Planning, Live Map, Fleet Analytics, Reports.
- Real-time data grid and charts (Recharts or Chart.js).
- REST API integration plan.
- WebSocket or MQTT-based live data channel mockup.
