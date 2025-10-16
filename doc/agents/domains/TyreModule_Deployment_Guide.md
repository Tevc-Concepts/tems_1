# TEMS Tyre Management Module - Comprehensive Deployment Guide

## 📋 Table of Contents
1. [Module Overview](#module-overview)
2. [Architecture](#architecture)
3. [DocType Specifications](#doctype-specifications)
4. [Custom Fields](#custom-fields)
5. [Workspace Configuration](#workspace-configuration)
6. [Reports & Dashboards](#reports--dashboards)
7. [Scheduled Tasks](#scheduled-tasks)
8. [API Endpoints](#api-endpoints)
9. [Installation Steps](#installation-steps)
10. [Testing & Validation](#testing--validation)

---

## Module Overview

The TEMS Tyre Management Module provides comprehensive tyre lifecycle tracking, predictive maintenance, and profitability analysis for commercial transport fleets.

### Key Features
- ✅ Full lifecycle tracking (purchase → installation → rotation → disposal)
- ✅ AI-powered health scoring (0-100 index)
- ✅ IoT sensor data ingestion (TPMS integration)
- ✅ Cost per kilometer analytics
- ✅ Predictive replacement scheduling
- ✅ Anomaly detection and alerts
- ✅ Brand/model performance comparison
- ✅ Vehicle-Asset integration

### Technology Stack
- **Framework**: Frappe v15+
- **ERP Integration**: ERPNext (Vehicle, Asset doctypes)
- **AI Module**: TEMS AI (for predictions)
- **Database**: MariaDB/MySQL
- **API**: REST with JWT authentication

---

## Architecture

### Integration Points

```
┌─────────────────────────────────────────────────────────┐
│                  TEMS Tyre Module                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Tyre       │  │ Installation │  │  Inspection  │  │
│  │   Master     │  │     Log      │  │     Log      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                  │           │
│         └─────────┬───────┴──────────────────┘           │
│                   │                                       │
└───────────────────┼───────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
    ┌───▼────┐            ┌─────▼──────┐
    │Vehicle │            │   Asset    │
    │(ERPNext)◄───────────┤  (ERPNext) │
    └───┬────┘            └─────┬──────┘
        │                       │
    ┌───▼────────────────┬──────▼──────────┐
    │ Operations         │ Finance         │
    │ (Journey Plan)     │ (Cost Ledger)   │
    └────────────────────┴─────────────────┘
```

### Data Flow

1. **Tyre Registration** → Creates Tyre record → Links to Asset (optional)
2. **Installation** → Links Tyre → Vehicle → Updates Vehicle tyre map
3. **Sensor Data** → IoT ingestion → Anomaly detection → Alerts
4. **Inspection** → Manual/AI → Health score → Predictive analytics
5. **Costs** → Rolls up to Vehicle → Finance profitability analysis

---

## DocType Specifications

### 1. Tyre (Master)

**Module**: TEMS Tyre  
**Naming**: `TYRE-{YYYY}-{#####}` (auto)  
**Is Submittable**: No  
**Track Changes**: Yes

#### Fields

| Field Name | Label | Type | Options | Required | In List | Description |
|------------|-------|------|---------|----------|---------|-------------|
| **Basic Information** |
| tyre_id | Tyre ID | Data | | No | Yes | Auto-generated |
| brand | Brand | Data | | Yes | Yes | Manufacturer (e.g., Michelin, Bridgestone) |
| model | Model | Data | | Yes | Yes | Tyre model number |
| size | Size | Data | | Yes | Yes | Size spec (e.g., 315/80R22.5) |
| tyre_type | Tyre Type | Select | Steer\nDrive\nTrailer\nSpare | Yes | Yes | Position type |
| serial_number | Serial Number | Data | | No | No | Manufacturer serial |
| **Financial** |
| cost | Purchase Cost | Currency | | Yes | No | Acquisition cost |
| purchase_date | Purchase Date | Date | | No | No | Date of purchase |
| supplier | Supplier | Link | Supplier | No | No | Vendor |
| warranty_months | Warranty (Months) | Int | | No | No | Warranty period |
| **Status & Location** |
| status | Status | Select | In Stock\nInstalled\nIn Repair\nRetread\nDisposed | Yes | Yes | Current status |
| vehicle | Vehicle | Link | Vehicle | No | Yes | Current vehicle (if installed) |
| asset_link | Asset Link | Link | Asset | No | No | ERPNext Asset reference |
| warehouse | Warehouse | Link | Warehouse | No | No | Storage location (if in stock) |
| **Technical Specifications** |
| load_index | Load Index | Int | | No | No | Load rating |
| speed_rating | Speed Rating | Data | | No | No | Speed code |
| tread_pattern | Tread Pattern | Select | Highway\nAll-Terrain\nMud\nWinter | No | No | Pattern type |
| ply_rating | Ply Rating | Data | | No | No | Strength rating |
| **Mileage & Usage** |
| initial_tread_depth | Initial Tread Depth (mm) | Float | | No | No | New tyre tread (default 16.0) |
| last_tread_depth_mm | Last Tread Depth (mm) | Float | | No | Yes | Most recent measurement |
| current_mileage | Current Mileage (km) | Float | | No | Yes | Total km traveled |
| estimated_remaining_life | Est. Remaining Life (km) | Float | | No | No | Predicted km remaining |
| **Maintenance & Inspection** |
| last_inspection_date | Last Inspection | Datetime | | No | No | Most recent check |
| last_pressure_psi | Last Pressure (PSI) | Float | | No | Yes | Most recent reading |
| last_rotation_date | Last Rotation | Date | | No | No | Last rotation event |
| next_rotation_due | Next Rotation Due | Date | | No | No | Scheduled rotation |
| **AI & Sensors** |
| pressure_sensor_id | Pressure Sensor ID | Data | | No | No | TPMS sensor identifier |
| ai_health_index | AI Health Index | Int | | No | Yes | 0-100 health score |
| ai_health_status | AI Health Status | Select | Good\nCaution\nReplace Soon\nReplace Immediately | No | Yes | AI classification |
| last_health_check | Last Health Check | Datetime | | No | No | Last AI calculation |
| **Lifecycle** |
| disposal_date | Disposal Date | Date | | No | No | End of life date |
| disposal_reason | Disposal Reason | Select | Worn Out\nDamaged\nDefect\nAge\nOther | No | No | Reason for disposal |
| scrap_value | Scrap Value | Currency | | No | No | Residual value |
| predicted_replacement_date | Predicted Replacement | Date | No | No | AI forecast |
| **Additional** |
| remarks | Remarks | Text Editor | | No | No | Notes |

#### Permissions
- Fleet Manager: All
- Fleet Officer: Read, Write, Create
- Operations Manager: Read
- Maintenance Tech: Read, Write
- Driver: Read (own vehicle only)

---

### 2. Tyre Installation Log

**Module**: TEMS Tyre  
**Naming**: `TINST-{YYYY}-{#####}` (auto)  
**Is Submittable**: No  
**Track Changes**: Yes

#### Fields

| Field Name | Label | Type | Options | Required | In List |
|------------|-------|------|---------|----------|---------|
| tyre | Tyre | Link | Tyre | Yes | Yes |
| vehicle | Vehicle | Link | Vehicle | Yes | Yes |
| position | Position | Select | Front Left\nFront Right\nRear Left 1\nRear Right 1\nRear Left 2\nRear Right 2\nSpare | Yes | Yes |
| installation_date | Installation Date | Datetime | | Yes | Yes |
| mileage_at_installation | Mileage at Installation | Float | | No | Yes |
| removed_date | Removed Date | Datetime | | No | Yes |
| mileage_at_removal | Mileage at Removal | Float | | No | No |
| technician | Technician | Link | Employee | No | No |
| installation_cost | Installation Cost | Currency | | No | No |
| remarks | Remarks | Small Text | | No | No |

#### Hooks
```python
doc_events = {
    "Tyre Installation Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_install",
        "on_update": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_removal"
    }
}
```

---

### 3. Tyre Rotation Log

**Module**: TEMS Tyre  
**Naming**: `TROT-{YYYY}-{#####}` (auto)

#### Fields

| Field Name | Label | Type | Options | Required | In List |
|------------|-------|------|---------|----------|---------|
| vehicle | Vehicle | Link | Vehicle | Yes | Yes |
| rotation_date | Rotation Date | Datetime | | Yes | Yes |
| mileage_at_rotation | Mileage | Float | | Yes | Yes |
| rotation_pattern | Rotation Pattern | Select | Front-to-Rear\nCross\nCustom | Yes | No |
| technician | Technician | Link | Employee | No | No |
| tyre_movements | Tyre Movements | Table | Tyre Rotation Item | Yes | No |
| cost | Cost | Currency | | No | No |
| remarks | Remarks | Text | | No | No |

#### Child Table: Tyre Rotation Item

| Field Name | Label | Type | Options |
|------------|-------|------|---------|
| tyre | Tyre | Link | Tyre |
| from_position | From Position | Data | |
| to_position | To Position | Data | |

---

### 4. Tyre Inspection Log

**Module**: TEMS Tyre  
**Naming**: `TINSP-{YYYY}-{#####}` (auto)

#### Fields

| Field Name | Label | Type | Options | Required | In List |
|------------|-------|------|---------|----------|---------|
| tyre | Tyre | Link | Tyre | Yes | Yes |
| inspection_date | Inspection Date | Datetime | | Yes | Yes |
| inspector | Inspector | Link | Employee | Yes | Yes |
| inspection_type | Type | Select | Routine\nPre-Trip\nPost-Trip\nIncident\nAI-Photo | Yes | Yes |
| **Measurements** |
| pressure_psi | Pressure (PSI) | Float | | No | Yes |
| tread_depth_mm | Tread Depth (mm) | Float | | No | Yes |
| temperature_c | Temperature (°C) | Float | | No | No |
| **Visual Inspection** |
| visual_condition | Visual Condition | Select | Good\nFair\nPoor | No | Yes |
| damage_detected | Damage Detected | Check | | No | Yes |
| damage_type | Damage Type | Select | Cut\nBulge\nCrack\nPuncture\nUneven Wear\nOther | No | No |
| damage_severity | Severity | Select | Minor\nModerate\nSevere | No | No |
| observations | Observations | Text | | No | No |
| **AI Analysis** |
| ai_condition_classification | AI Classification | Select | Good\nCaution\nReplace Soon\nReplace Immediately | No | Yes |
| ai_health_index | AI Health Index | Int | | No | Yes |
| ai_confidence_score | AI Confidence | Percent | | No | No |
| photo_attachment | Photo | Attach Image | | No | No |
| **Action Required** |
| action_required | Action Required | Check | | No | Yes |
| recommended_action | Recommended Action | Select | Monitor\nRotate\nRepair\nReplace\nImmediate Replacement | No | No |

#### Hooks
```python
doc_events = {
    "Tyre Inspection Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_inspection"
    }
}
```

---

### 5. Tyre Sensor Data

**Module**: TEMS Tyre  
**Naming**: Auto-increment  
**Purpose**: IoT sensor data storage

#### Fields

| Field Name | Label | Type | Options | Required | In List |
|------------|-------|------|---------|----------|---------|
| sensor_id | Sensor ID | Data | | Yes | Yes |
| tyre | Tyre | Link | Tyre | Yes | Yes |
| timestamp | Timestamp | Datetime | | Yes | Yes |
| pressure_psi | Pressure (PSI) | Float | | No | Yes |
| temperature_c | Temperature (°C) | Float | | No | Yes |
| battery_level | Battery Level (%) | Percent | | No | No |
| signal_strength | Signal Strength | Int | | No | No |
| speed_kmh | Speed (km/h) | Float | | No | No |
| alert_generated | Alert Generated | Check | | No | Yes |
| ai_status_flag | AI Status | Select | Normal\nWarning\nCritical | No | Yes |

#### Indexes
- `sensor_id, timestamp` (composite for time-series queries)
- `tyre, timestamp` (for tyre history)

#### Data Retention
- Keep last 90 days online
- Archive older data monthly

---

### 6. Tyre Disposal Log

**Module**: TEMS Tyre  
**Naming**: `TDISP-{YYYY}-{#####}` (auto)

#### Fields

| Field Name | Label | Type | Options | Required | In List |
|------------|-------|------|---------|----------|---------|
| tyre | Tyre | Link | Tyre | Yes | Yes |
| vehicle | Last Vehicle | Link | Vehicle | No | Yes |
| disposal_date | Disposal Date | Date | | Yes | Yes |
| reason | Reason | Select | Worn Out\nIrreparable Damage\nAge Limit\nDefect\nAccident\nOther | Yes | Yes |
| final_mileage | Final Mileage (km) | Float | | No | Yes |
| final_tread_depth | Final Tread Depth (mm) | Float | | No | No |
| disposal_method | Disposal Method | Select | Recycling\nRetread\nScrap\nResale | Yes | No |
| scrap_value | Scrap Value | Currency | | No | No |
| disposal_cost | Disposal Cost | Currency | | No | No |
| final_cost_impact | Final Cost Impact | Currency | | No | No |
| recycler | Recycler/Buyer | Link | Supplier | No | No |
| remarks | Remarks | Text | | No | No |

#### Hooks
```python
doc_events = {
    "Tyre Disposal Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_disposal"
    }
}
```

---

## Custom Fields

### ERPNext Vehicle (Extend, No Core Changes)

Add custom fields via `tems/tems_tyre/custom_fields/vehicle.json`:

```json
{
    "custom_fields": [
        {
            "dt": "Vehicle",
            "fieldname": "custom_tyre_section",
            "fieldtype": "Section Break",
            "label": "Tyre Management",
            "insert_after": "custom_tems_details"
        },
        {
            "dt": "Vehicle",
            "fieldname": "custom_tyre_map",
            "fieldtype": "JSON",
            "label": "Tyre Position Map",
            "insert_after": "custom_tyre_section",
            "read_only": 1,
            "description": "Auto-updated tyre position mapping"
        },
        {
            "dt": "Vehicle",
            "fieldname": "custom_total_tyre_positions",
            "fieldtype": "Int",
            "label": "Total Tyre Positions",
            "insert_after": "custom_tyre_map",
            "default": "6",
            "description": "Number of tyre positions (including spares)"
        },
        {
            "dt": "Vehicle",
            "fieldname": "custom_last_tyre_inspection",
            "fieldtype": "Date",
            "label": "Last Tyre Inspection",
            "insert_after": "custom_total_tyre_positions",
            "read_only": 1
        },
        {
            "dt": "Vehicle",
            "fieldname": "custom_next_tyre_rotation_due",
            "fieldtype": "Date",
            "label": "Next Rotation Due",
            "insert_after": "custom_last_tyre_inspection"
        },
        {
            "dt": "Vehicle",
            "fieldname": "custom_tyre_alert_count",
            "fieldtype": "Int",
            "label": "Active Tyre Alerts",
            "insert_after": "custom_next_tyre_rotation_due",
            "read_only": 1,
            "default": "0"
        }
    ],
    "doctype": "Vehicle",
    "sync_on_migrate": 1
}
```

### ERPNext Asset (Extend, No Core Changes)

Add custom fields via `tems/tems_tyre/custom_fields/asset.json`:

```json
{
    "custom_fields": [
        {
            "dt": "Asset",
            "fieldname": "custom_is_tyre",
            "fieldtype": "Check",
            "label": "Is Tyre",
            "insert_after": "asset_category",
            "default": "0"
        },
        {
            "dt": "Asset",
            "fieldname": "custom_tyre_link",
            "fieldtype": "Link",
            "label": "Tyre Record",
            "options": "Tyre",
            "insert_after": "custom_is_tyre",
            "depends_on": "eval:doc.custom_is_tyre==1"
        },
        {
            "dt": "Asset",
            "fieldname": "custom_tyre_size",
            "fieldtype": "Data",
            "label": "Tyre Size",
            "insert_after": "custom_tyre_link",
            "depends_on": "eval:doc.custom_is_tyre==1"
        },
        {
            "dt": "Asset",
            "fieldname": "custom_tyre_brand",
            "fieldtype": "Data",
            "label": "Tyre Brand",
            "insert_after": "custom_tyre_size",
            "depends_on": "eval:doc.custom_is_tyre==1"
        }
    ],
    "doctype": "Asset",
    "sync_on_migrate": 1
}
```

---

## Workspace Configuration

### Fleet Tyre Management Workspace

Create workspace via UI: **Desk → Workspaces → New Workspace**

**JSON Export** (`tems/tems_tyre/workspace/fleet_tyre_management.json`):

```json
{
    "name": "Fleet Tyre Management",
    "module": "TEMS Tyre",
    "public": 1,
    "title": "Fleet Tyre Management",
    "icon": "🛞",
    "extends_another_page": 0,
    "charts": [
        {
            "chart_name": "Tyre Health Distribution",
            "label": "Tyre Health Distribution"
        },
        {
            "chart_name": "Monthly Tyre Costs",
            "label": "Monthly Costs"
        }
    ],
    "shortcuts": [
        {
            "type": "DocType",
            "label": "Tyre",
            "link_to": "Tyre",
            "doc_view": "List",
            "color": "#FF5733"
        },
        {
            "type": "DocType",
            "label": "Tyre Installation Log",
            "link_to": "Tyre Installation Log",
            "doc_view": "List",
            "color": "#3498DB"
        },
        {
            "type": "DocType",
            "label": "Tyre Inspection Log",
            "link_to": "Tyre Inspection Log",
            "doc_view": "List",
            "color": "#F39C12"
        },
        {
            "type": "Report",
            "label": "Tyre Performance Analysis",
            "link_to": "Tyre Performance Analysis",
            "report_type": "Script Report",
            "color": "#9B59B6"
        },
        {
            "type": "Report",
            "label": "Tyre Cost Analysis",
            "link_to": "Tyre Cost Analysis",
            "report_type": "Script Report",
            "color": "#1ABC9C"
        },
        {
            "type": "Page",
            "label": "Tyre Dashboard",
            "link_to": "tyre-dashboard",
            "color": "#E74C3C"
        }
    ],
    "cards": [
        {
            "label": "Quick Actions",
            "items": [
                {
                    "type": "DocType",
                    "label": "Register New Tyre",
                    "link_to": "Tyre",
                    "description": "Add new tyre to inventory"
                },
                {
                    "type": "DocType",
                    "label": "Record Installation",
                    "link_to": "Tyre Installation Log",
                    "description": "Install tyre on vehicle"
                },
                {
                    "type": "DocType",
                    "label": "Conduct Inspection",
                    "link_to": "Tyre Inspection Log",
                    "description": "Perform tyre inspection"
                }
            ]
        },
        {
            "label": "Monitoring",
            "items": [
                {
                    "type": "report",
                    "label": "Active Alerts",
                    "link_to": "Tyre Alerts",
                    "description": "Tyres requiring attention"
                },
                {
                    "type": "report",
                    "label": "Replacement Schedule",
                    "link_to": "Tyre Replacement Schedule",
                    "description": "Predicted replacement dates"
                }
            ]
        },
        {
            "label": "Analytics",
            "items": [
                {
                    "type": "report",
                    "label": "Performance by Brand",
                    "link_to": "Tyre Brand Performance"
                },
                {
                    "type": "report",
                    "label": "Fleet Tyre Metrics",
                    "link_to": "Fleet Tyre Metrics"
                }
            ]
        }
    ]
}
```

---

## Reports & Dashboards

### Report 1: Tyre Performance Analysis

**Type**: Script Report  
**Module**: TEMS Tyre  
**File**: `tems/tems_tyre/report/tyre_performance_analysis/tyre_performance_analysis.py`

```python
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Tyre"), "fieldname": "tyre", "fieldtype": "Link", "options": "Tyre", "width": 120},
        {"label": _("Brand"), "fieldname": "brand", "fieldtype": "Data", "width": 100},
        {"label": _("Model"), "fieldname": "model", "fieldtype": "Data", "width": 100},
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": _("Health Index"), "fieldname": "health_index", "fieldtype": "Int", "width": 90},
        {"label": _("Condition"), "fieldname": "condition", "fieldtype": "Data", "width": 120},
        {"label": _("Mileage (km)"), "fieldname": "mileage", "fieldtype": "Float", "width": 100},
        {"label": _("Cost/km"), "fieldname": "cost_per_km", "fieldtype": "Currency", "width": 100},
        {"label": _("Tread (mm)"), "fieldname": "tread_depth", "fieldtype": "Float", "width": 90},
        {"label": _("Pressure (PSI)"), "fieldname": "pressure", "fieldtype": "Float", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_analyzer import batch_analyze_fleet_tyres
    
    vehicle = filters.get("vehicle") if filters else None
    insights = batch_analyze_fleet_tyres(vehicle)
    
    data = []
    for insight in insights:
        data.append({
            "tyre": insight.get("tyre"),
            "brand": insight.get("brand"),
            "model": insight.get("model"),
            "vehicle": insight.get("vehicle"),
            "health_index": insight.get("health_index"),
            "condition": insight.get("condition"),
            "mileage": insight.get("current_mileage"),
            "cost_per_km": insight.get("cost_per_km"),
            "tread_depth": 0,  # Get from tyre doc
            "pressure": 0,  # Get from tyre doc
            "status": insight.get("status")
        })
    
    return data
```

**Filters**:
- Vehicle (optional)
- Brand (optional)
- Status (optional)
- Date Range

---

### Report 2: Tyre Cost Analysis

**Type**: Script Report  
**Module**: TEMS Tyre

```python
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Tyre"), "fieldname": "tyre", "fieldtype": "Link", "options": "Tyre", "width": 120},
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": _("Purchase Cost"), "fieldname": "purchase_cost", "fieldtype": "Currency", "width": 120},
        {"label": _("Maintenance Cost"), "fieldname": "maintenance_cost", "fieldtype": "Currency", "width": 120},
        {"label": _("Total Cost"), "fieldname": "total_cost", "fieldtype": "Currency", "width": 120},
        {"label": _("Mileage"), "fieldname": "mileage", "fieldtype": "Float", "width": 100},
        {"label": _("Cost per km"), "fieldname": "cost_per_km", "fieldtype": "Currency", "width": 100},
        {"label": _("ROI Status"), "fieldname": "roi_status", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_calculator import calculate_tyre_roi
    
    conditions = []
    if filters.get("vehicle"):
        conditions.append(f"vehicle = '{filters.get('vehicle')}'")
    if filters.get("brand"):
        conditions.append(f"brand = '{filters.get('brand')}'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    tyres = frappe.db.sql(f"""
        SELECT name, vehicle, brand, cost, current_mileage
        FROM `tabTyre`
        WHERE {where_clause}
        AND status != 'Disposed'
    """, as_dict=True)
    
    data = []
    for tyre in tyres:
        roi = calculate_tyre_roi(tyre.name)
        
        data.append({
            "tyre": tyre.name,
            "vehicle": tyre.vehicle,
            "purchase_cost": tyre.cost,
            "maintenance_cost": roi["purchase_cost"] - flt(tyre.cost),
            "total_cost": roi["purchase_cost"],
            "mileage": tyre.current_mileage,
            "cost_per_km": roi["cost_per_km"],
            "roi_status": roi["status"]
        })
    
    return data

def get_chart_data(data):
    labels = [d["tyre"] for d in data[:10]]
    values = [d["cost_per_km"] for d in data[:10]]
    
    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}]
        },
        "type": "bar",
        "colors": ["#FF5733"]
    }
```

---

### Report 3: Tyre Replacement Schedule

**Type**: Script Report  
**Module**: TEMS Tyre

Shows predicted replacement dates for all active tyres.

```python
import frappe
from frappe import _
from frappe.utils import getdate, add_days

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Tyre"), "fieldname": "tyre", "fieldtype": "Link", "options": "Tyre", "width": 120},
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": _("Position"), "fieldname": "position", "fieldtype": "Data", "width": 100},
        {"label": _("Health Index"), "fieldname": "health_index", "fieldtype": "Int", "width": 90},
        {"label": _("Current Mileage"), "fieldname": "mileage", "fieldtype": "Float", "width": 100},
        {"label": _("Remaining km"), "fieldname": "remaining_km", "fieldtype": "Float", "width": 100},
        {"label": _("Days Until Replacement"), "fieldname": "days_until", "fieldtype": "Int", "width": 150},
        {"label": _("Predicted Date"), "fieldname": "predicted_date", "fieldtype": "Date", "width": 120},
        {"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_calculator import predict_replacement_date
    
    # Get installed tyres
    tyres = frappe.db.sql("""
        SELECT 
            t.name as tyre,
            t.vehicle,
            t.current_mileage,
            t.ai_health_index,
            til.position
        FROM `tabTyre` t
        LEFT JOIN `tabTyre Installation Log` til ON til.tyre = t.name
        WHERE t.status = 'Installed'
        AND til.removed_date IS NULL
        ORDER BY t.ai_health_index ASC
    """, as_dict=True)
    
    data = []
    for tyre_info in tyres:
        prediction = predict_replacement_date(tyre_info.tyre)
        
        if prediction:
            days = prediction.get("days_until_replacement", 999)
            
            if days < 7:
                priority = "Critical"
            elif days < 30:
                priority = "High"
            elif days < 90:
                priority = "Medium"
            else:
                priority = "Low"
            
            data.append({
                "tyre": tyre_info.tyre,
                "vehicle": tyre_info.vehicle,
                "position": tyre_info.position,
                "health_index": tyre_info.ai_health_index,
                "mileage": tyre_info.current_mileage,
                "remaining_km": prediction.get("remaining_km", 0),
                "days_until": days,
                "predicted_date": add_days(None, days),
                "priority": priority
            })
    
    return data
```

---

### Dashboard: Tyre Management Dashboard

**Number Cards**:

1. **Total Active Tyres**
```json
{
    "doctype": "Number Card",
    "name": "Total Active Tyres",
    "label": "Active Tyres",
    "function": "Count",
    "document_type": "Tyre",
    "filters_json": "{\"status\": [\"in\", [\"Installed\", \"In Stock\"]]}",
    "color": "#3498DB"
}
```

2. **Tyres Needing Attention**
```json
{
    "doctype": "Number Card",
    "name": "Tyres Needing Attention",
    "label": "Action Required",
    "function": "Count",
    "document_type": "Tyre",
    "filters_json": "{\"ai_health_status\": [\"in\", [\"Replace Soon\", \"Replace Immediately\"]]}",
    "color": "#E74C3C"
}
```

3. **Average Tyre Health**
```json
{
    "doctype": "Number Card",
    "name": "Average Tyre Health",
    "label": "Avg Health Index",
    "function": "Average",
    "aggregate_function_based_on": "ai_health_index",
    "document_type": "Tyre",
    "filters_json": "{\"status\": \"Installed\"}",
    "color": "#1ABC9C"
}
```

4. **Monthly Tyre Spend**
```json
{
    "doctype": "Number Card",
    "name": "Monthly Tyre Spend",
    "label": "This Month Spend",
    "function": "Sum",
    "aggregate_function_based_on": "amount",
    "document_type": "Cost And Revenue Ledger",
    "filters_json": "{\"category\": [\"like\", \"%Tyre%\"], \"date\": [\"timespan\", \"this month\"]}",
    "color": "#F39C12"
}
```

**Dashboard Charts**:

1. **Tyre Health Distribution** (Donut)
2. **Monthly Tyre Costs** (Line)
3. **Brand Performance Comparison** (Bar)
4. **Replacement Predictions** (Timeline)

---

## Scheduled Tasks

Add to `tems/hooks.py`:

```python
scheduler_events = {
    "hourly": [
        "tems.tems_tyre.tasks.monitor_tyre_sensors"
    ],
    "daily": [
        "tems.tems_tyre.tasks.update_tyre_health_scores",
        "tems.tems_tyre.tasks.predict_replacement_schedule",
        "tems.tems_tyre.tasks.sync_tyre_costs_to_finance"
    ],
    "weekly": [
        "tems.tems_tyre.tasks.analyze_fleet_tyre_performance"
    ],
    "monthly": [
        "tems.tems_tyre.tasks.cleanup_old_sensor_data"
    ]
}
```

---

## API Endpoints

All endpoints documented in `tems/tems_tyre/api/endpoints.py`

### Authentication
- **Method**: API Key or Session
- **Header**: `Authorization: token <api_key>:<api_secret>` OR `X-API-Key: <sensor_key>`

### Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/method/tems.tems_tyre.api.endpoints.register_tyre` | Register new tyre | Required |
| PUT | `/api/method/tems.tems_tyre.api.endpoints.update_tyre_status` | Update tyre status | Required |
| POST | `/api/method/tems.tems_tyre.api.endpoints.install_tyre` | Record installation | Required |
| PUT | `/api/method/tems.tems_tyre.api.endpoints.remove_tyre` | Record removal | Required |
| POST | `/api/method/tems.tems_tyre.api.endpoints.record_inspection` | Record inspection | Required |
| POST | `/api/method/tems.tems_tyre.api.endpoints.ingest_sensor_data` | IoT sensor data | API Key (Guest allowed) |
| GET | `/api/method/tems.tems_tyre.api.endpoints.get_tyre_health` | Get tyre health | Required |
| GET | `/api/method/tems.tems_tyre.api.endpoints.get_vehicle_tyre_status` | Get vehicle tyres | Required |

---

## Installation Steps

### Step 1: Create DocTypes

Use Frappe UI or bench command:

```bash
cd frappe-bench
bench --site your-site.local create-doctype "Tyre" --module "TEMS Tyre"
bench --site your-site.local create-doctype "Tyre Installation Log" --module "TEMS Tyre"
bench --site your-site.local create-doctype "Tyre Rotation Log" --module "TEMS Tyre"
bench --site your-site.local create-doctype "Tyre Inspection Log" --module "TEMS Tyre"
bench --site your-site.local create-doctype "Tyre Sensor Data" --module "TEMS Tyre"
bench --site your-site.local create-doctype "Tyre Disposal Log" --module "TEMS Tyre"
```

Then configure fields as per specifications above.

### Step 2: Apply Custom Fields

```bash
bench --site your-site.local migrate
```

This applies custom fields from JSON files.

### Step 3: Create Workspace

1. Navigate to **Desk → Workspaces**
2. Click **New Workspace**
3. Use JSON configuration above
4. Save and publish

### Step 4: Create Reports

For each report:
1. **Desk → Report Builder → New Report**
2. Set type: **Script Report**
3. Copy Python code
4. Save

### Step 5: Create Dashboard

1. **Desk → Dashboard → New Dashboard**
2. Name: "Tyre Management Dashboard"
3. Add number cards
4. Add charts
5. Save

### Step 6: Update hooks.py

Add to `tems/tems_tyre/hooks.py` (see [Scheduled Tasks](#scheduled-tasks) section).

### Step 7: Register Module

Update `tems/modules.txt`:
```
TEMS Tyre
```

### Step 8: Migrate

```bash
bench --site your-site.local migrate
bench --site your-site.local clear-cache
```

### Step 9: Set Permissions

```bash
bench --site your-site.local console
```

```python
from frappe.permissions import setup_custom_perms

# Tyre permissions
setup_custom_perms("Tyre")
# Configure via UI: Permissions Manager
```

### Step 10: Test APIs

```bash
# Test sensor ingestion
curl -X POST http://your-site.local/api/method/tems.tems_tyre.api.endpoints.ingest_sensor_data \
  -H "X-API-Key: your-sensor-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "TPMS-001",
    "tyre": "TYRE-2025-00001",
    "pressure_psi": 105.5,
    "temperature_c": 45.2
  }'
```

---

## Testing & Validation

### Unit Tests

Create tests in `tems/tems_tyre/tests/`:

```python
# test_tyre_calculator.py
import frappe
import unittest
from tems.tems_tyre.utils.tyre_calculator import calculate_cost_per_km

class TestTyreCalculator(unittest.TestCase):
    def test_cost_per_km(self):
        # Create test tyre
        tyre = frappe.get_doc({
            "doctype": "Tyre",
            "brand": "Test Brand",
            "model": "Test Model",
            "size": "315/80R22.5",
            "tyre_type": "Drive",
            "cost": 50000,
            "status": "In Stock",
            "current_mileage": 10000
        }).insert()
        
        cost = calculate_cost_per_km(tyre.name)
        self.assertEqual(cost, 5.0)  # 50000 / 10000
        
        tyre.delete()
```

Run tests:
```bash
bench --site your-site.local run-tests --app tems --module tems_tyre
```

### Integration Tests

1. **Tyre Lifecycle Test**: Register → Install → Inspect → Dispose
2. **Sensor Data Flow**: Ingest → Anomaly Detection → Alert
3. **Cost Rollup**: Tyre Cost → Vehicle → Finance Ledger
4. **Predictive Analytics**: Historical Data → Health Score → Replacement Prediction

### Performance Benchmarks

- Sensor data ingestion: < 100ms per record
- Health score calculation: < 500ms per tyre
- Fleet analytics: < 5s for 1000 tyres
- Report generation: < 10s for 12 months data

---

## Maintenance & Support

### Monitoring

- Check scheduler logs: `bench --site your-site.local doctor`
- Monitor sensor ingestion rates
- Review alert accuracy
- Track prediction precision

### Troubleshooting

**Issue**: Sensor data not ingesting
- Check API key validity
- Verify network connectivity
- Review error logs

**Issue**: Health scores not updating
- Run: `bench --site your-site.local execute tems.tems_tyre.tasks.update_tyre_health_scores`
- Check tyre has inspection data

**Issue**: Costs not rolling up to vehicle
- Verify Asset → Vehicle linkage
- Check Cost Ledger entries

---

## Appendix

### Tyre Position Standards

```
Heavy Commercial Vehicle (6-wheel):
- Front Left (FL)
- Front Right (FR)
- Rear Left 1 (RL1)
- Rear Right 1 (RR1)
- Rear Left 2 (RL2)
- Rear Right 2 (RR2)
- Spare

Tractor-Trailer (18-wheel):
[Configure based on axle configuration]
```

### API Response Codes

- `200`: Success
- `400`: Bad Request (validation error)
- `401`: Unauthorized (invalid API key)
- `404`: Resource not found
- `500`: Server error

### Glossary

- **TPMS**: Tyre Pressure Monitoring System
- **Health Index**: AI-calculated score (0-100) indicating tyre condition
- **Wear Rate**: Tread loss in mm per 1000 km
- **Cost per km**: Total tyre cost divided by mileage
- **ROI**: Return on Investment - performance vs expected lifespan

---

## 📞 Contact & Support

For implementation support:
- **Documentation**: `/workspace/development/frappe-bench/apps/tems/doc`
- **Source Code**: `/workspace/development/frappe-bench/apps/tems/tems/tems_tyre`
- **Issues**: Create GitHub issue or TEMS Support ticket

---

**End of Deployment Guide**

*Last Updated: October 16, 2025*
*Version: 1.0.0*
*Module: TEMS Tyre Management*
