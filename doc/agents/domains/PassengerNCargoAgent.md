# 🚦 Prompt for Copilot — Safe Multimodal Expansion (Cargo + Passenger)

```markdown
# TASK CONTEXT
The project is an enterprise-grade Transport Management System built on Frappe/ERPNext v15+.
It already has the following domains: tems_operations, tems_fleet, tems_finance, tems_safety, tems_people, tems_documents, tems_crm, tems_supplychain, tems_trade, tems_informal, tems_climate, tems_governance, tems_insights.

You are now to **extend** the existing TEMS architecture (not rewrite) by adding support for **two new modules**:
1. tems_cargo (Cargo Management)
2. tems_passenger (Passenger Management)

This change must:
- Integrate cleanly into the existing TEMS/Frappe codebase.
- Reuse ERPNext doctypes (Vehicle, Asset, Employee, etc.) without replacing or renaming them.
- Follow Frappe modular structure and naming convention.
- Not modify core ERPNext doctypes directly — only extend through Custom Fields, Custom Scripts, and TEMS module logic.

---

# SPECIFIC OBJECTIVES

## 1. VEHICLE EXTENSION
- Add a custom field `vehicle_type` (Select: Cargo | Passenger) to the ERPNext `Vehicle` doctype via Frappe Custom Field API.
- Do **not** alter existing Vehicle fields or data.
- Location: `tems_fleet/custom_fields/vehicle_type.json`.
- Ensure this field is accessible in Fleet and Operations forms.

## 2. NEW MODULES
Create two new modules under TEMS app:
```

tems_cargo/
tems_passenger/

```
Each must include:
- `/doctype/` folder with core doctypes.
- `/handlers/` folder for doc event hooks.
- `/api/` folder for whitelisted methods.
- `/tasks.py` and `/utils/` for internal logic.

## 3. TEMS_CARGO DOCTYPES
- Cargo Consignment
- Cargo Manifest
- Cargo Waybill
- Cargo Delivery Log
- Cargo Rate Card

### Relationships:
- `Cargo Consignment` links to Customer, Vehicle, and Operation Plan.
- `Cargo Manifest` groups multiple consignments.
- `Cargo Waybill` documents delivery (links Manifest + Consignment).
- `Cargo Delivery Log` records delivery events.

Each must validate:
```

vehicle.vehicle_type == "Cargo"

```

## 4. TEMS_PASSENGER DOCTYPES
- Passenger Trip
- Passenger Booking
- Passenger Manifest
- Passenger Feedback
- Passenger Rate Card

### Relationships:
- `Passenger Trip` links to Vehicle, Operation Plan, and Route.
- `Passenger Booking` links to Trip and seat allocation.
- `Passenger Manifest` lists passengers for each trip.
- `Passenger Feedback` captures post-trip rating.

Each must validate:
```

vehicle.vehicle_type == "Passenger"

````

## 5. OPERATIONS INTEGRATION
Update `tems_operations`:
- Add field `operation_mode` (Select: Cargo | Passenger) in Operation Plan.
- Auto-sync with `vehicle.vehicle_type` when vehicle is selected.
- If `operation_mode == "Cargo"` → allow linking Cargo Consignments.
- If `operation_mode == "Passenger"` → allow linking Passenger Trips.
- Add validations and event handlers accordingly in:
  `tems_operations/handlers/operation_plan.py`

## 6. FINANCE & INSIGHTS INTEGRATION
- Ensure existing Cost/Revenue and Profitability rollups in `tems_finance` reference both cargo and passenger sources.
- Add a discriminator field `source_type` (Cargo or Passenger) in Cost & Revenue Ledger.
- Update Insights dashboards to group by `vehicle_type` and `source_type`.

## 7. SAFETY, HRMS, CRM ALIGNMENT
- No changes to existing logic required.
- Just ensure new Operation Plan entries are visible in dashboards and references.

## 8. HOOKS.PY
Register new module events without disturbing old ones:
```python
doc_events.update({
  "Cargo Consignment": {
    "validate": "tems_cargo.handlers.consignment.validate_vehicle_type"
  },
  "Passenger Trip": {
    "validate": "tems_passenger.handlers.trip.validate_vehicle_type"
  }
})
````

## 9. UI INTEGRATION

* In Desk, create two new Workspaces: **Cargo Management** and **Passenger Management**.
* Link their doctypes, reports, and dashboards.
* Apply Frappe UI theming consistent with existing TEMS workspaces.

## 10. TESTS

* Add basic integration tests for both modules in their respective `/tests/` folders.
* Validate that Operation Plans only accept vehicles of matching type.
* Ensure profitability reports correctly aggregate Cargo and Passenger records.

---

# CONSTRAINTS

* Preserve all existing doctypes, fixtures, and scripts.
* Do not refactor or rename previous module imports.
* New modules must integrate through hooks, not direct dependency injection.
* All `.py` files must remain under 300 lines.

---

# EXPECTED OUTPUTS

1. New folders: `tems_cargo/`, `tems_passenger/`.
2. Custom Field JSON for Vehicle (`vehicle_type`).
3. Updated `tems_operations` Operation Plan doctype and handlers.
4. Updated `tems_finance` Cost & Revenue Ledger.
5. Updated `hooks.py` (non-destructive merge).
6. New workspaces and icons in Desk.
7. Tests confirming safe integration and compatibility with current data.

---

# CODE STYLE & PATH RULES

* Handlers: `tems_{module}/handlers/{doctype_name}.py`
* APIs: `tems_{module}/api/{resource}.py`
* Tasks: `tems_{module}/tasks.py`
* Utils: `tems_{module}/utils/{helper}.py`
* Tests: `tems_{module}/tests/test_{doctype_name}.py`
* Custom Fields: `tems_fleet/custom_fields/*.json`
* hooks.py: must dynamically extend existing `doc_events` and `scheduler_events`, never replace them.

