# FleetAgent.md

ROLE:
Build and maintain Fleet & Asset Management module inside TEMS app (Frappe v15+).

TASKS:
- Implement Asset inventory with offline photo uploads.
- Integrate GPS/Telematics with offline caching.
- Build Preventive & Predictive Maintenance workflows.
- Create Work Orders with mobile-first forms.
- Manage lifecycle (Acquisition → Utilization → Disposal → Replacement).

CONSTRAINTS:
- All code inside `apps/tems`.
- Extend ERPNext Asset/Vehicle via Custom Fields.
- New DocTypes: Maintenance Work Order, Asset Utilization Log.
- Fixtures: Role "Fleet Manager", Workspace "Fleet Manager".
- hooks.py: doc_events for Asset & Work Order.

INTER-RELATIONSHIPS:
- HRMS (Drivers, Technicians).
- Finance (Cost tracking, TCO).
- Safety (Journey Plans, Inspections).
- Supply Chain (Spares).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py 
- Workspace JSON fixtures.
- hooks.py entries.
- Unit tests (`tems/tests/test_fleet.py`).
