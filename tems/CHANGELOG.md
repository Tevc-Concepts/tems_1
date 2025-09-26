# TEMS Change Log

This document tracks notable changes, fixes, and adjustments made during development and testing across domains.

## 2025-09-25

- Domain 4 (Fleet) introduced under `tems/tems/tems_fleet` with DocTypes: Journey Plan, Maintenance Work Order (+ Maintenance Part Item), Fuel Log, Route Planning. Added Fleet Manager workspace, KPI card (Open Work Orders), and reports (Open Work Orders, Fuel Efficiency by Vehicle). Seed patch added (`seed_fleet.py`) with idempotent creation.
- Vehicle-first alignment:
  - Fuel Log now links to Vehicle instead of Asset; Fuel Efficiency report updated to aggregate by Vehicle; Fleet workspace links updated to Vehicle.
  - Journey Plan retains Vehicle link (optional for seed resilience).
- Reuse existing Doctype:
  - Route Planning now uses existing `Way Points` child table under `tems/tems/tems/doctype/way_points` instead of a duplicate Fleet `Waypoint` child DocType.
- People domain enhancement: added Script Report “Training Compliance by Dept” and linked it in the People & Drivers workspace.

- Domain 5 (Safety) introduced under `tems/tems/tems_safety` with DocTypes: Safety Incident (vehicle-first with status/severity), Spot Check, Spot Check Photo (child). Added Safety Management workspace with shortcuts and KPI (Open Safety Incidents), plus query report “Safety Incidents by Severity”. Seed patch (`seed_safety.py`) creates demo records idempotently.

## 2025-09-24

- Domain 3 (People) implemented: Driver Qualification, Training Record, Incident Involvement; client script to prevent expired qualification save; report “Expiring Driver Qualifications”; number card; workspace; seed patch.

## 2025-09-23

- Domain 2 (Operations) implemented: Dispatch Schedule, Shift Plan, Duty Assignment, Control Exception, Operations Event, SOS Event; 2 query reports; client script; Vehicle refactor and DB indexes; workspace and seed.

## 2025-09-22

- Domain 1 (Governance) implemented with policies, obligations, approvals, meetings; API and daily scheduler; workspace, KPIs, and reports; seed patch. Routing and JSON fixes applied.

---

If you manually adjust fixtures or DocType fields, add a bullet here with the date and a short description so we keep an authoritative change history.
