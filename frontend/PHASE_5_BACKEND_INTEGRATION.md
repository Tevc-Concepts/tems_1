# Phase 5: Frappe Backend Integration - Implementation Guide

**Status:** Ready to Begin  
**Estimated Time:** 4-6 hours  
**Dependencies:** Phase 4 Complete ✅  
**Date:** October 14, 2025  

## Overview

Phase 5 focuses on integrating all 4 PWAs with the Frappe backend by creating API endpoints, web routes, and ensuring proper authentication and data flow between frontend and backend.

## Phase 5 Tasks (10 tasks)

### 1. Hooks Configuration (1 task)

#### Task 1.1: Update `tems/hooks.py` with PWA Routes
**File:** `/workspace/development/frappe-bench/apps/tems/tems/hooks.py`

**Required Changes:**
```python
# Add to website_route_rules
website_route_rules = [
    # Driver PWA
    {"from_route": "/driver/<path:app_path>", "to_route": "driver"},
    
    # Operations PWA
    {"from_route": "/operations/<path:app_path>", "to_route": "operations"},
    
    # Safety PWA
    {"from_route": "/safety/<path:app_path>", "to_route": "safety"},
    
    # Fleet PWA
    {"from_route": "/fleet/<path:app_path>", "to_route": "fleet"},
]

# Update app_include_js to include PWA scripts
app_include_js = [
    "/assets/tems/js/tems.min.js"
]

# Add PWA specific scheduled jobs if needed
scheduler_events = {
    "hourly": [
        "tems.tasks.sync_offline_data"
    ],
    "daily": [
        "tems.tasks.cleanup_old_logs"
    ]
}
```

**Verification:**
- [ ] Routes accessible via browser
- [ ] PWA loading correctly at each route
- [ ] No 404 errors for PWA assets

---

### 2. WWW Entry Points (4 tasks)

#### Task 2.1: Create Driver PWA Entry Point
**File:** `/workspace/development/frappe-bench/apps/tems/tems/www/driver/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#39ff14">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>TEMS Driver</title>
    <link rel="manifest" href="/assets/tems/frontend/driver-pwa/dist/manifest.webmanifest">
    <link rel="icon" type="image/svg+xml" href="/assets/tems/frontend/driver-pwa/dist/favicon.ico">
</head>
<body>
    <div id="app"></div>
    <script type="module" src="/assets/tems/frontend/driver-pwa/dist/index.js"></script>
</body>
</html>
```

**Path:** `tems/www/driver/`

---

#### Task 2.2: Create Operations PWA Entry Point
**File:** `/workspace/development/frappe-bench/apps/tems/tems/www/operations/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0284c7">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>TEMS Operations</title>
    <link rel="manifest" href="/assets/tems/frontend/operations-pwa/dist/manifest.webmanifest">
    <link rel="icon" type="image/svg+xml" href="/assets/tems/frontend/operations-pwa/dist/favicon.ico">
</head>
<body>
    <div id="app"></div>
    <script type="module" src="/assets/tems/frontend/operations-pwa/dist/index.js"></script>
</body>
</html>
```

**Path:** `tems/www/operations/`

---

#### Task 2.3: Create Safety PWA Entry Point
**File:** `/workspace/development/frappe-bench/apps/tems/tems/www/safety/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#ef4444">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>TEMS Safety</title>
    <link rel="manifest" href="/assets/tems/frontend/safety-pwa/dist/manifest.webmanifest">
    <link rel="icon" type="image/svg+xml" href="/assets/tems/frontend/safety-pwa/dist/favicon.ico">
</head>
<body>
    <div id="app"></div>
    <script type="module" src="/assets/tems/frontend/safety-pwa/dist/index.js"></script>
</body>
</html>
```

**Path:** `tems/www/safety/`

---

#### Task 2.4: Create Fleet PWA Entry Point
**File:** `/workspace/development/frappe-bench/apps/tems/tems/www/fleet/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#10b981">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>TEMS Fleet</title>
    <link rel="manifest" href="/assets/tems/frontend/fleet-pwa/dist/manifest.webmanifest">
    <link rel="icon" type="image/svg+xml" href="/assets/tems/frontend/fleet-pwa/dist/favicon.ico">
</head>
<body>
    <div id="app"></div>
    <script type="module" src="/assets/tems/frontend/fleet-pwa/dist/index.js"></script>
</body>
</html>
```

**Path:** `tems/www/fleet/`

---

### 3. API Endpoint Implementation (5 tasks)

#### Task 3.1: Create Operations API (`tems/api/pwa/operations.py`)

**Required Endpoints (13 endpoints):**

```python
import frappe
from frappe import _

@frappe.whitelist()
def get_vehicles(filters=None):
    """Get all vehicles with optional filters"""
    pass

@frappe.whitelist()
def get_vehicle_location(vehicle_id):
    """Get real-time vehicle location"""
    pass

@frappe.whitelist()
def update_vehicle_status(vehicle_id, status):
    """Update vehicle operational status"""
    pass

@frappe.whitelist()
def get_dispatches(filters=None):
    """Get dispatch assignments"""
    pass

@frappe.whitelist()
def create_dispatch(dispatch_data):
    """Create new dispatch assignment"""
    pass

@frappe.whitelist()
def assign_driver(dispatch_id, driver_id):
    """Assign driver to dispatch"""
    pass

@frappe.whitelist()
def update_dispatch_status(dispatch_id, status):
    """Update dispatch status"""
    pass

@frappe.whitelist()
def get_routes(filters=None):
    """Get route information"""
    pass

@frappe.whitelist()
def optimize_route(route_data):
    """Optimize route with multiple waypoints"""
    pass

@frappe.whitelist()
def get_fleet_statistics():
    """Get fleet statistics for dashboard"""
    pass

@frappe.whitelist()
def get_driver_availability():
    """Get available drivers"""
    pass

@frappe.whitelist()
def get_active_trips():
    """Get currently active trips"""
    pass

@frappe.whitelist()
def bulk_update_vehicles(vehicle_updates):
    """Bulk update vehicle information"""
    pass
```

---

#### Task 3.2: Create Safety API (`tems/api/pwa/safety.py`)

**Required Endpoints (17 endpoints):**

```python
import frappe
from frappe import _

@frappe.whitelist()
def get_incidents(filters=None):
    """Get safety incidents"""
    pass

@frappe.whitelist()
def report_incident(incident_data):
    """Report new safety incident"""
    pass

@frappe.whitelist()
def update_incident_status(incident_id, status):
    """Update incident status"""
    pass

@frappe.whitelist()
def assign_investigator(incident_id, investigator_id):
    """Assign investigator to incident"""
    pass

@frappe.whitelist()
def get_audits(filters=None):
    """Get safety audits"""
    pass

@frappe.whitelist()
def schedule_audit(audit_data):
    """Schedule new safety audit"""
    pass

@frappe.whitelist()
def submit_audit_findings(audit_id, findings):
    """Submit audit findings"""
    pass

@frappe.whitelist()
def get_compliance_items(filters=None):
    """Get compliance tracking items"""
    pass

@frappe.whitelist()
def update_compliance_status(compliance_id, status):
    """Update compliance item status"""
    pass

@frappe.whitelist()
def renew_compliance(compliance_id, renewal_data):
    """Renew compliance certification"""
    pass

@frappe.whitelist()
def get_risk_assessments(filters=None):
    """Get risk assessments"""
    pass

@frappe.whitelist()
def create_risk_assessment(assessment_data):
    """Create new risk assessment"""
    pass

@frappe.whitelist()
def update_mitigation_plan(assessment_id, plan_data):
    """Update risk mitigation plan"""
    pass

@frappe.whitelist()
def get_safety_statistics():
    """Get safety statistics for dashboard"""
    pass

@frappe.whitelist()
def get_expiring_compliance(days=30):
    """Get compliance items expiring soon"""
    pass

@frappe.whitelist()
def get_critical_incidents():
    """Get critical/high-severity incidents"""
    pass

@frappe.whitelist()
def calculate_compliance_rate():
    """Calculate overall compliance rate"""
    pass
```

---

#### Task 3.3: Create Fleet API (`tems/api/pwa/fleet.py`)

**Required Endpoints (16 endpoints):**

```python
import frappe
from frappe import _

@frappe.whitelist()
def get_assets(filters=None):
    """Get fleet assets"""
    pass

@frappe.whitelist()
def get_asset_details(asset_id):
    """Get detailed asset information"""
    pass

@frappe.whitelist()
def update_asset_status(asset_id, status, notes=''):
    """Update asset status"""
    pass

@frappe.whitelist()
def get_asset_categories():
    """Get asset categories"""
    pass

@frappe.whitelist()
def get_work_orders(filters=None):
    """Get maintenance work orders"""
    pass

@frappe.whitelist()
def get_upcoming_maintenance(days=30):
    """Get upcoming maintenance schedule"""
    pass

@frappe.whitelist()
def create_work_order(work_order_data):
    """Create new work order"""
    pass

@frappe.whitelist()
def update_work_order_status(work_order_id, status):
    """Update work order status"""
    pass

@frappe.whitelist()
def schedule_preventive_maintenance(asset_id, scheduled_date, maintenance_type):
    """Schedule preventive maintenance"""
    pass

@frappe.whitelist()
def get_fuel_logs(filters=None):
    """Get fuel consumption logs"""
    pass

@frappe.whitelist()
def get_fuel_stats(period='month'):
    """Get fuel statistics"""
    pass

@frappe.whitelist()
def log_fuel_entry(fuel_data):
    """Log fuel entry"""
    pass

@frappe.whitelist()
def get_fuel_trends(asset_id, period='month'):
    """Get fuel consumption trends"""
    pass

@frappe.whitelist()
def get_lifecycle_data(filters=None):
    """Get asset lifecycle data"""
    pass

@frappe.whitelist()
def get_asset_lifecycle(asset_id):
    """Get specific asset lifecycle"""
    pass

@frappe.whitelist()
def calculate_depreciation(asset_id):
    """Calculate asset depreciation"""
    pass

@frappe.whitelist()
def update_lifecycle_milestone(asset_id, milestone, status):
    """Update lifecycle milestone"""
    pass
```

---

#### Task 3.4: Enhance Driver API (`tems/api/pwa/driver.py`)

**Verify/Add Endpoints:**
- [ ] Authentication endpoints
- [ ] Trip management endpoints
- [ ] Document upload endpoints
- [ ] Geolocation tracking endpoints
- [ ] Offline sync endpoints

---

#### Task 3.5: Create API Index (`tems/api/pwa/__init__.py`)

```python
# Make API modules discoverable
from . import driver
from . import operations
from . import safety
from . import fleet

__all__ = ['driver', 'operations', 'safety', 'fleet']
```

---

## Implementation Checklist

### Pre-Implementation
- [x] Phase 4 complete (all PWAs built)
- [ ] Review existing Frappe DocTypes
- [ ] Identify required permissions
- [ ] Plan data migration if needed

### Implementation Order
1. [ ] Create www entry points (Tasks 2.1-2.4)
2. [ ] Update hooks.py (Task 1.1)
3. [ ] Create Operations API (Task 3.1)
4. [ ] Create Safety API (Task 3.2)
5. [ ] Create Fleet API (Task 3.3)
6. [ ] Enhance Driver API (Task 3.4)
7. [ ] Create API index (Task 3.5)

### Testing After Each API
- [ ] Test authentication flow
- [ ] Test CRUD operations
- [ ] Test error handling
- [ ] Test permissions
- [ ] Test with actual PWA

### Post-Implementation
- [ ] Build all PWAs: `npm run build:all`
- [ ] Restart Frappe: `bench restart`
- [ ] Test each PWA in browser
- [ ] Verify API responses
- [ ] Check browser console for errors
- [ ] Test offline functionality
- [ ] Document any issues

---

## Commands Reference

```bash
# Build all PWAs
cd /workspace/development/frappe-bench/apps/tems/frontend
npm run build:all

# Restart Frappe
cd /workspace/development/frappe-bench
bench restart

# Check Frappe logs
bench --site development.localhost console

# Test API endpoint
bench --site development.localhost console
>>> frappe.call('tems.api.pwa.operations.get_vehicles')

# Clear cache
bench --site development.localhost clear-cache
bench --site development.localhost clear-website-cache
```

---

## API Development Guidelines

### 1. Authentication
All API endpoints must use `@frappe.whitelist()` decorator and verify user permissions:

```python
@frappe.whitelist()
def get_data():
    if not frappe.has_permission("DocType Name", "read"):
        frappe.throw(_("Insufficient permissions"), frappe.PermissionError)
    # ... endpoint logic
```

### 2. Error Handling
Always include proper error handling:

```python
@frappe.whitelist()
def create_record(data):
    try:
        # Parse JSON if string
        if isinstance(data, str):
            data = frappe.parse_json(data)
        
        # Validate data
        if not data.get('required_field'):
            frappe.throw(_("Required field missing"))
        
        # Create record
        doc = frappe.get_doc(data)
        doc.insert()
        
        return doc.as_dict()
        
    except frappe.ValidationError as e:
        frappe.log_error(f"Validation error: {str(e)}")
        frappe.throw(_(str(e)))
    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}")
        frappe.throw(_("An error occurred"))
```

### 3. Data Validation
Validate all input data:

```python
def validate_dispatch_data(data):
    required_fields = ['vehicle_id', 'driver_id', 'destination']
    for field in required_fields:
        if not data.get(field):
            frappe.throw(_(f"{field} is required"))
    return True
```

### 4. Response Format
Return consistent response format:

```python
# Success
return {
    "success": True,
    "message": "Operation completed",
    "data": result
}

# Error (handled by frappe.throw)
frappe.throw({
    "success": False,
    "message": "Error message",
    "error": error_details
})
```

---

## Expected Outcomes

After Phase 5 completion:

1. **All PWAs Accessible via Browser**
   - http://localhost:8000/driver
   - http://localhost:8000/operations
   - http://localhost:8000/safety
   - http://localhost:8000/fleet

2. **API Endpoints Functional**
   - Operations: 13 endpoints working
   - Safety: 17 endpoints working
   - Fleet: 16 endpoints working
   - Driver: Enhanced with additional endpoints

3. **Authentication Working**
   - Users can login from each PWA
   - Session maintained across requests
   - Permissions enforced

4. **Data Flow Complete**
   - Frontend → API → DocType → Database
   - Real-time updates working
   - Offline sync functional

---

## Next Steps After Phase 5

Once Phase 5 is complete, proceed to:

**Phase 6: Testing & Deployment**
- Comprehensive E2E testing
- Mobile device testing
- Performance optimization
- Deployment documentation
- User training materials

---

**Ready to begin Phase 5? Let's start with creating the www entry points!** 🚀
