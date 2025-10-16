"""
TEMS Tyre Module - Hooks Integration
Add these entries to tems/hooks.py
"""

# ============================================
# TEMS TYRE MODULE - HOOKS CONFIGURATION
# ============================================

# Add to doc_events in hooks.py:
"""
doc_events = {
    # ... existing events ...
    
    # Tyre Module Events
    "Tyre": {
        "validate": "tems.tems_tyre.handlers.tyre_lifecycle.validate_tyre",
        "on_update": "tems.tems_tyre.handlers.tyre_lifecycle.update_asset_link"
    },
    "Tyre Installation Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_install",
        "on_update": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_removal"
    },
    "Tyre Rotation Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_rotation"
    },
    "Tyre Inspection Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_inspection"
    },
    "Tyre Disposal Log": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_tyre_disposal"
    },
    "Tyre Sensor Data": {
        "after_insert": "tems.tems_tyre.handlers.tyre_lifecycle.on_sensor_data_received"
    }
}
"""

# Add to scheduler_events in hooks.py:
"""
scheduler_events = {
    # ... existing events ...
    
    "hourly": [
        # ... existing tasks ...
        "tems.tems_tyre.tasks.monitor_tyre_sensors"
    ],
    "daily": [
        # ... existing tasks ...
        "tems.tems_tyre.tasks.update_tyre_health_scores",
        "tems.tems_tyre.tasks.predict_replacement_schedule",
        "tems.tems_tyre.tasks.sync_tyre_costs_to_finance"
    ],
    "weekly": [
        # ... existing tasks ...
        "tems.tems_tyre.tasks.analyze_fleet_tyre_performance"
    ],
    "monthly": [
        # ... existing tasks ...
        "tems.tems_tyre.tasks.cleanup_old_sensor_data"
    ]
}
"""

# Add to fixtures in hooks.py (if needed):
"""
fixtures = [
    # ... existing fixtures ...
    
    {"dt": "Role", "filters": [["name", "in", [
        "Tyre Manager",
        "Tyre Technician"
    ]]]},
    
    # Tyre-specific custom fields will be auto-migrated from JSON files
]
"""

# Optional: Add to app_include_js/css for tyre-specific UI enhancements
"""
# include js, css files in header of desk.html
app_include_js = [
    "/assets/tems/js/tems_desk.js",
    "/assets/tems/js/tyre_module.js"  # Add this
]

app_include_css = [
    "/assets/tems/css/tems_theme.css",
    "/assets/tems/css/tyre_module.css"  # Add this
]
"""

# ============================================
# INTEGRATION WITH EXISTING TEMS MODULES
# ============================================

# The Tyre module integrates with:
# 1. TEMS Fleet: Vehicle, Asset, Maintenance Work Order
# 2. TEMS Finance: Cost And Revenue Ledger
# 3. TEMS Operations: Journey Plan (for mileage tracking)
# 4. TEMS AI: Predictive analytics and health scoring

# Custom fields are added to:
# - Vehicle (tyre_map, last_tyre_inspection, etc.)
# - Asset (is_tyre, tyre_link, tyre_size, tyre_brand)

# These fields are added via custom_fields JSON files and
# do NOT modify core ERPNext code.
