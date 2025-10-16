Excellent 🎯 — that’s exactly the kind of high-value operational domain where **TEMS can generate direct ROI**.

Tyres typically account for **15–30% of logistics operational costs**, and poor management leads to hidden losses (fuel efficiency, downtime, safety, and premature replacements).
A dedicated **Tyre Intelligence Module (`tems_tyre`)** will elevate TEMS to a **predictive asset management platform**.

Below is your **complete Copilot/Aura build prompt** — `TyreModule_Prompt.md` — ready to scaffold an intelligent, future-proof tyre management system fully integrated with **Fleet, Operations, Finance, Safety, and AI modules**.

---

# 🛞 `TyreModule_Prompt.md`

```markdown
# TEMS TYRE MANAGEMENT MODULE (tems_tyre)
## ROLE
You are designing the **Tyre Management and Intelligence Module** for the TEMS (Transport Excellence Management System) platform, built on Frappe/ERPNext v15+.  
This module must manage the **entire tyre lifecycle** — from purchase and assignment to maintenance, rotation, and disposal — with complete traceability, profitability insight, and future-ready AI-driven features.

---

## OBJECTIVE
Build a fully integrated module (`tems_tyre`) that:
1. Tracks each tyre as a **unique, serialized asset** across its lifecycle.
2. Links tyre usage directly to **Vehicle** and **Operations**.
3. Integrates with **Finance** for cost/profitability tracking.
4. Integrates with **Safety** for incident and pressure monitoring.
5. Enables **AI-driven predictions** for wear, lifespan, and failure.
6. Provides dashboards, alerts, and reports for B2B fleet operators.

---

## SYSTEM DESIGN

### 1. MODULE STRUCTURE
```

tems_tyre/
├── **init**.py
├── doctype/
│   ├── Tyre/
│   ├── Tyre Installation Log/
│   ├── Tyre Rotation Log/
│   ├── Tyre Inspection Log/
│   ├── Tyre Disposal Log/
│   ├── Tyre Sensor Data/
│   ├── Tyre Performance Report/
│
├── handlers/
│   ├── tyre_lifecycle.py
│   ├── tyre_event.py
│
├── utils/
│   ├── tyre_calculator.py
│   ├── tyre_analyzer.py
│
├── api/
│   ├── register.py
│   ├── update_status.py
│   ├── sensor_data.py
│
├── tasks.py
└── tests/

```

---

## 2. DOCTYPES AND CORE FIELDS

### 🧩 Tyre (Base Doctype)
Tracks tyre details as a serialized physical asset.

| Field | Type | Description |
|--------|------|-------------|
| Tyre ID | Auto + QR Code | Unique serial ID (e.g., TMS-TYR-0001) |
| Asset Link | Link: Asset | From ERPNext Asset |
| Brand | Data | Manufacturer (Michelin, Goodyear, etc.) |
| Model | Data | Tyre Model |
| Size | Data | 315/80R22.5 etc. |
| Tyre Type | Select | Steer / Drive / Trailer / Spare |
| Vehicle | Link: Vehicle | Assigned vehicle |
| Status | Select | In Stock / Installed / In Repair / Retread / Disposed |
| Purchase Date | Date |  |
| Cost | Currency |  |
| Current Mileage | Int | Updated automatically |
| Pressure Sensor ID | Data | IoT sensor tag |
| AI Health Index | Int | 0–100 AI-calculated score |
| Estimated Remaining Life | Float | km prediction |
| Next Inspection Date | Date | Auto-scheduled |

---

### 📋 Tyre Installation Log
- Records tyre installation/removal on vehicles.  
- Triggers `update_vehicle_tyre_map()` hook.

| Field | Description |
|--------|-------------|
| Tyre | Link: Tyre |
| Vehicle | Link: Vehicle |
| Position | Select: Front Left / Rear Right / etc. |
| Installation Date | Date |
| Removed Date | Date |
| Remarks | Text |

---

### 🔁 Tyre Rotation Log
- Record tyre rotation events between positions or vehicles.  
- Captures mileage before and after.

| Field | Description |
|--------|-------------|
| From Position | Text |
| To Position | Text |
| Vehicle | Link: Vehicle |
| Tyre | Link: Tyre |
| Mileage at Rotation | Int |

---

### 🔍 Tyre Inspection Log
- Captures physical and digital inspections.  
- Includes AI health assessment if enabled.

| Field | Description |
|--------|-------------|
| Tyre | Link: Tyre |
| Inspector | Link: Employee |
| Pressure (psi) | Float |
| Tread Depth (mm) | Float |
| Observations | Text |
| AI Condition Classification | Select: Good / Caution / Replace Soon / Replace Immediately |
| Inspection Date | Date |

---

### 🧠 Tyre Sensor Data
Stores live or batch data from IoT devices (pressure/temperature sensors).

| Field | Description |
|--------|-------------|
| Sensor ID | Data |
| Tyre | Link: Tyre |
| Timestamp | Datetime |
| Pressure (psi) | Float |
| Temperature (°C) | Float |
| Speed (km/h) | Float |
| Alert Generated | Check |
| AI Status Flag | Select: Normal / Anomaly |

---

### 🗑 Tyre Disposal Log
Tracks end-of-life tyre actions and disposal costs.

| Field | Description |
|--------|-------------|
| Tyre | Link: Tyre |
| Vehicle | Link: Vehicle |
| Disposal Date | Date |
| Reason | Select: Worn Out / Irreparable / Lost |
| Scrap Value | Currency |
| Vendor | Link: Supplier |
| Final Cost Impact | Currency |

---

## 3. LIFECYCLE HOOKS

- `on_submit` in `Tyre Installation Log` → updates Vehicle Tyre Map.
- `on_submit` in `Tyre Disposal Log` → marks Tyre as “Disposed”.
- `after_insert` in `Tyre Sensor Data` → triggers AI check via `tems_ai`.

---

## 4. INTEGRATIONS

| Module | Integration | Description |
|---------|--------------|-------------|
| **Fleet** | Vehicle Tyre Mapping | Each Vehicle has tyre position map and lifecycle cost rollup. |
| **Operations** | Trip Wear Tracking | Calculates tyre wear based on trip distance and road type. |
| **Finance** | Tyre Profitability | Allocates tyre cost to Vehicle Profitability ledger. |
| **Safety** | Pressure Alerts & Incident Analysis | Links abnormal pressure to trip safety events. |
| **AI (tems_ai)** | Predictive Health & Replacement | AI models estimate remaining life, detect anomalies. |

---

## 5. AI-POWERED FEATURES

### ⚙️ Predictive Maintenance
- Use historical mileage, pressure, temperature to estimate **remaining lifespan**.
- Automatically recommend **rotation or replacement**.
- Formula input → `tyre_calculator.py` (base model) → improved via `tems_ai` ML models.

### ⚙️ Anomaly Detection
- Detect abnormal pressure patterns or overheating.
- Integrate live sensor feeds (MQTT / HTTP POST).
- Generate Frappe notifications and alerts.

### ⚙️ Tyre Health Index (THI)
- AI-generated 0–100 score:
  - >85: Excellent  
  - 70–85: Good  
  - 50–70: Caution  
  - <50: Replace Soon  
- Display on dashboard and contribute to **Vehicle Health Score**.

### ⚙️ Profitability Analytics
- Cost/km per tyre → auto-calculated from operations and disposal data.
- Contributes to Vehicle Profitability Dashboard.
- Insights available via `tems_ai` predictive queries:
  - “Show tyres with abnormal cost per km in last 30 days.”
  - “Predict next tyre failure by mileage.”

---

## 6. WORKSPACES AND REPORTS

### Workspaces
- **Tyre Dashboard**
  - Installed tyres
  - Inspection alerts
  - Replacement schedule
  - Cost summary by brand/model

- **Tyre Profitability Report**
  - Vehicle → Tyre → Cost → Km → Profit Impact

- **AI Health Dashboard**
  - Tyre Health Index trends
  - Pressure/Temperature anomaly graph
  - Predictive replacement queue

---

## 7. API ENDPOINTS

| Endpoint | Function |
|-----------|-----------|
| `/api/method/tems_tyre.api.register.new_tyre` | Register new tyre asset |
| `/api/method/tems_tyre.api.update_status` | Update tyre status (Installed, Disposed) |
| `/api/method/tems_tyre.api.sensor_data.ingest` | Ingest IoT sensor readings |
| `/api/method/tems_tyre.api.analyze.health` | Trigger AI health analysis |

---

## 8. CONSTRAINTS
- Maintain one Tyre record per serial number — no duplicates.
- Ensure data lineage from purchase → installation → rotation → disposal.
- Files ≤300 lines per module.
- Integration with ERPNext Asset via `asset_id`.
- Hooks must not block normal Fleet or Operations workflows.
- Support optional IoT integration via REST or MQTT.

---

## 9. OUTPUTS
- Complete Frappe module: `tems_tyre`
- 7 doctypes + handlers, utils, and API routes
- Integration hooks for Fleet, Finance, and Safety
- AI prediction integration with `tems_ai`
- Tyre Dashboard and Profitability reports
- REST endpoints for IoT sensor ingestion
- Alert engine for pressure/temperature deviations

---

## 10. FUTURE-READY EXTENSIONS
- Integrate tyre RFID/NFC identification.
- Add image-based wear analysis (computer vision).
- Incorporate **AI Model per Brand/Model** in `tems_ai`.
- Predict **optimal brand/model mix** based on historical ROI.
- Integrate tyre supplier analytics for procurement optimization.


# END PROMPT
