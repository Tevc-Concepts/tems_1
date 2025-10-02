# Hooks Scaffolding — Cross-Domain Events and Schedules

This reference mirrors `tems/hooks.py` and shows the expected structure and import paths per domain. Keep scheduled jobs idempotent.

## Doc Events (examples)

```python
# tems/hooks.py (excerpt)
doc_events = {
    "Vehicle": {
        "on_update": "tems.tems_fleet.handlers.update_vehicle_profitability",
        "on_submit": "tems.tems_fleet.handlers.validate_vehicle_assets",
    },
    "Asset": {
        "on_update": "tems.tems_fleet.handlers.rollup_asset_cost_to_vehicle",
        "on_trash": "tems.tems_fleet.handlers.prevent_asset_without_vehicle",
    },
    "Journey Plan": {
        "before_insert": "tems.tems_fleet.handlers.validate_journey",
        "on_submit": "tems.tems_operations.handlers.log_journey_start",
    },
    "Duty Assignment": {
        "before_insert": "tems.tems_operations.handlers.ensure_driver_vehicle_valid",
    },
    "Safety Incident": {
        "on_submit": "tems.tems_safety.handlers.log_incident_against_vehicle",
    },
    "Border Crossing": {
        "on_submit": "tems.tems_trade.handlers.log_vehicle_crossing",
    },
    "Compliance Obligation": {
        "on_update": "tems.tems_governance.handlers.on_obligation_update",
    },
}
```

## Scheduler Events (examples)

```python
scheduler_events = {
    "daily": [
        "tems.tems_governance.api.notify_upcoming_reviews_and_obligations",
        "tems.tems_operations.tasks.generate_daily_operations_report",
        "tems.tems_finance.tasks.daily_interest_compute",
    ],
    "hourly": [
        "tems.tems_operations.tasks.check_vehicle_availability",
    ],
    "monthly": [
        "tems.tems_safety.tasks.aggregate_emissions_monthly",
    ],
}
```

Notes
- Import path schema is `tems.tems_{domain}.{api|handlers|tasks}.*`.
- Prefer per-domain handlers over a monolith; keep functions small and idempotent.
- Register fixture types in `fixtures` list (roles, custom fields, workspaces, reports, dashboards, client scripts, workflows, etc.).
