# OperationsAgent.md

ROLE:
Build Operations Management module for TEMS (the execution engine of transportation).

TASKS:
- Plan transport operations integrating Fleet, HR, CRM, Finance, and Safety.
- Vehicle Availability: check status from Fleet (maintenance, allocation).
- Trip Planning: allocate vehicle + driver to customer order.
- Movement Tracking:
  - Check-In (at depot/warehouse).
  - Check-Out (departure).
  - In Transit (normal).
  - Diversion (reroute).
  - Out Transit (cross-border).
  - Delivery Confirmation.
- Cost & Revenue Tracking:
  - Capture costs from fuel, maintenance, tolls, fees.
  - Capture revenues from customer orders.
  - Calculate margins per trip.
- Operational Dashboards:
  - Active journeys.
  - Vehicle availability.
  - Cost vs revenue metrics.

CONSTRAINTS:
- New DocTypes: Operation Plan, Movement Log, Trip Allocation, Cost & Revenue Ledger.
- Extend Fleet, HRMS, and CRM DocTypes via Link fields.
- Fixtures: Role "Operations Manager", Workspace "Operations".
- hooks.py: trigger state changes on Movement Log (Check-In → In Transit → Delivered).
- Must be offline-first with mobile forms for drivers.

INTER-RELATIONSHIPS:
- Fleet: vehicles, maintenance availability.
- HRMS: drivers, certifications.
- CRM: orders & SLA.
- Finance: trip cost, billing, revenue.
- Safety: risk scores for journeys.
- Trade: border crossing status.
- Supply Chain: spare parts affecting availability.

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py (Operation Plan, Movement Log, Trip Allocation, Cost & Revenue Ledger).
- Workspace JSON fixture for Operations role.
- hooks.py event handlers for movement states.
- Unit tests (`tems/tests/test_operations.py`).
- Example dashboard (Operations Dashboard with KPIs).
