# TEMS Tyre Module - Quick Reference Card

## 🎯 Quick Start

### Installation Checklist
- [ ] Create 6 DocTypes (see deployment guide)
- [ ] Run `bench migrate` to apply custom fields
- [ ] Add hooks to `tems/hooks.py`
- [ ] Create workspace and reports
- [ ] Configure permissions
- [ ] Test API endpoints

### Essential Commands
```bash
# Migrate
bench --site site.local migrate

# Clear cache
bench --site site.local clear-cache

# Run tests
bench --site site.local run-tests --app tems --module tems_tyre

# Manual task execution
bench --site site.local console
>>> from tems.tems_tyre.tasks import update_tyre_health_scores
>>> update_tyre_health_scores()
```

---

## 📋 DocTypes to Create

1. **Tyre** (Master) - 30+ fields
2. **Tyre Installation Log** - 10 fields
3. **Tyre Rotation Log** - 8 fields + child table
4. **Tyre Inspection Log** - 15 fields
5. **Tyre Sensor Data** - 10 fields
6. **Tyre Disposal Log** - 12 fields

*See deployment guide for complete field specifications*

---

## 🔌 API Quick Reference

### Register Tyre
```bash
POST /api/method/tems.tems_tyre.api.endpoints.register_tyre
{
  "brand": "Michelin",
  "model": "XZA2",
  "size": "315/80R22.5",
  "tyre_type": "Drive",
  "cost": 45000
}
```

### Sensor Data (IoT)
```bash
POST /api/method/tems.tems_tyre.api.endpoints.ingest_sensor_data
X-API-Key: <sensor_key>
{
  "sensor_id": "TPMS-001",
  "pressure_psi": 105.5,
  "temperature_c": 45.2
}
```

### Get Health
```bash
GET /api/method/tems.tems_tyre.api.endpoints.get_tyre_health?tyre=TYRE-2025-00001
```

---

## 📊 Key Metrics

### Health Index Formula
```
Health = (Tread × 0.40) + (Pressure × 0.25) + (Usage × 0.20) + (Incidents × 0.15)
```

### Classification
- 85-100: Good
- 70-84: Caution
- 50-69: Replace Soon
- 0-49: Replace Immediately

### Cost per KM
```
Cost/KM = (Purchase Cost + Maintenance Costs) / Current Mileage
```

---

## 🗂️ File Locations

### Core Files
- Handlers: `tems/tems_tyre/handlers/tyre_lifecycle.py`
- Calculator: `tems/tems_tyre/utils/tyre_calculator.py`
- Analyzer: `tems/tems_tyre/utils/tyre_analyzer.py`
- API: `tems/tems_tyre/api/endpoints.py`
- Tasks: `tems/tems_tyre/tasks.py`

### Config Files
- Vehicle Fields: `tems/tems_tyre/custom_fields/vehicle.json`
- Asset Fields: `tems/tems_tyre/custom_fields/asset.json`
- Hooks Guide: `tems/tems_tyre/HOOKS_INTEGRATION.py`

### Documentation
- Main README: `tems/tems_tyre/README.md`
- Deployment: `doc/agents/domains/TyreModule_Deployment_Guide.md`
- Summary: `doc/agents/domains/TyreModule_Implementation_Summary.md`

---

## 🔧 Custom Fields

### Vehicle Extensions
- `custom_tyre_map` (JSON) - Position mapping
- `custom_total_tyre_positions` (Int) - Number of positions
- `custom_last_tyre_inspection` (Date) - Last inspection
- `custom_next_tyre_rotation_due` (Date) - Next rotation
- `custom_tyre_alert_count` (Int) - Active alerts
- `custom_avg_tyre_health` (Float) - Average health

### Asset Extensions
- `custom_is_tyre` (Check) - Flag as tyre
- `custom_tyre_link` (Link) - Link to Tyre doctype
- `custom_tyre_brand` (Data) - Brand
- `custom_tyre_model` (Data) - Model
- `custom_tyre_size` (Data) - Size specification

---

## ⏰ Scheduled Tasks

### Hourly
- `monitor_tyre_sensors()` - Detect stale sensors

### Daily (2 AM)
- `update_tyre_health_scores()` - Recalculate health

### Daily (3 AM)
- `predict_replacement_schedule()` - Forecast needs

### Daily (6 AM)
- `sync_tyre_costs_to_finance()` - Cost rollup

### Weekly (Monday 1 AM)
- `analyze_fleet_tyre_performance()` - Generate report

### Monthly (1st, 4 AM)
- `cleanup_old_sensor_data()` - Archive data

---

## 🎨 Workspace Shortcuts

### Quick Actions
- Register New Tyre
- Record Installation
- Conduct Inspection
- View Alerts

### Reports
- Tyre Performance Analysis
- Cost Analysis
- Replacement Schedule
- Brand Comparison

### Monitoring
- Active Alerts
- Health Distribution
- Monthly Costs

---

## 🚨 Common Tasks

### Register and Install Tyre
```python
# 1. Register
tyre = frappe.get_doc({
    "doctype": "Tyre",
    "brand": "Michelin",
    "model": "XZA2",
    "size": "315/80R22.5",
    "tyre_type": "Drive",
    "cost": 45000,
    "status": "In Stock"
}).insert()

# 2. Install
install = frappe.get_doc({
    "doctype": "Tyre Installation Log",
    "tyre": tyre.name,
    "vehicle": "VEH-001",
    "position": "Rear Right 1",
    "installation_date": frappe.utils.now()
}).insert()
```

### Record Inspection
```python
inspection = frappe.get_doc({
    "doctype": "Tyre Inspection Log",
    "tyre": "TYRE-2025-00001",
    "inspector": "EMP-001",
    "pressure_psi": 105.5,
    "tread_depth_mm": 12.5,
    "inspection_type": "Routine"
}).insert()
```

### Get Tyre Analytics
```python
from tems.tems_tyre.utils.tyre_analyzer import generate_tyre_insights

insights = generate_tyre_insights("TYRE-2025-00001")
print(f"Health: {insights['health_index']}")
print(f"Condition: {insights['condition']}")
print(f"Cost/km: {insights['cost_per_km']}")
```

---

## 🐛 Troubleshooting

### Health Scores Not Updating
```python
# Run manually
from tems.tems_tyre.tasks import update_tyre_health_scores
update_tyre_health_scores()
```

### Check Sensor Status
```sql
SELECT sensor_id, tyre, MAX(timestamp) as last_reading
FROM `tabTyre Sensor Data`
GROUP BY sensor_id
HAVING last_reading < DATE_SUB(NOW(), INTERVAL 2 HOUR);
```

### Verify Cost Rollup
```sql
SELECT t.name, t.vehicle, SUM(c.amount) as total_cost
FROM `tabTyre` t
LEFT JOIN `tabCost And Revenue Ledger` c ON c.vehicle = t.vehicle
WHERE t.vehicle IS NOT NULL
GROUP BY t.name;
```

---

## 📞 Support

- **Documentation**: See `TyreModule_Deployment_Guide.md`
- **Issues**: Check error logs in `frappe-bench/logs/`
- **Forum**: Frappe Discuss
- **GitHub**: github.com/Gabcelltd/tems

---

## 📚 Key Functions

### Calculator Utils
```python
from tems.tems_tyre.utils.tyre_calculator import (
    calculate_cost_per_km,
    calculate_wear_rate,
    predict_replacement_date,
    calculate_tyre_roi,
    calculate_fleet_tyre_metrics
)
```

### Analyzer Utils
```python
from tems.tems_tyre.utils.tyre_analyzer import (
    calculate_health_index,
    classify_tyre_condition,
    detect_pressure_anomaly,
    analyze_wear_pattern,
    generate_tyre_insights,
    batch_analyze_fleet_tyres
)
```

### Lifecycle Handlers
```python
from tems.tems_tyre.handlers.tyre_lifecycle import (
    on_tyre_install,
    on_tyre_removal,
    on_tyre_rotation,
    on_tyre_inspection,
    on_tyre_disposal,
    update_vehicle_tyre_map,
    create_tyre_cost_entry
)
```

---

## 🎯 Integration Points

1. **Vehicle** ← Many Tyres
2. **Asset** ← Tyre (optional)
3. **Cost & Revenue Ledger** ← Tyre Costs
4. **Journey Plan** → Mileage Tracking
5. **Maintenance Work Order** ← Scheduled Replacements
6. **TEMS AI** → Predictive Analytics

---

## ✅ Pre-Deployment Checklist

- [ ] All 6 DocTypes created with correct fields
- [ ] Custom fields migrated (Vehicle, Asset)
- [ ] Hooks added to `tems/hooks.py`
- [ ] Workspace created with shortcuts
- [ ] 4+ reports configured
- [ ] Dashboard with number cards
- [ ] Permissions assigned to roles
- [ ] API endpoints tested
- [ ] Scheduled tasks registered
- [ ] Sample data created for testing

---

## 📊 Success Metrics

### After 30 Days
- [ ] 100% tyre inventory registered
- [ ] All vehicles have tyre maps
- [ ] Daily health scores updating
- [ ] Sensor data flowing (if IoT)
- [ ] At least 10 inspections logged
- [ ] Cost tracking operational
- [ ] First predictive alert generated

### After 90 Days
- [ ] ROI analysis complete
- [ ] Brand performance trends visible
- [ ] Replacement predictions accurate
- [ ] Cost savings identified
- [ ] Maintenance optimization active

---

*Quick Reference v1.0 | Last Updated: Oct 16, 2025*
