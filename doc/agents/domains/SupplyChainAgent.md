# SupplyChainAgent.md

ROLE:
Build Supply Chain & Procurement module inside TEMS app.

TASKS:
- Manage Suppliers & Performance.
- Automate Procurement & Approvals.
- Track Inventory & Stock Alerts.
- Coordinate Logistics across sites.
- Procurement of parts (tires, spare engines, etc.) → linked to Assets → then roll up to Vehicle.
- Supplier performance impacts Vehicle availability.
- Supplier performance on parts

CONSTRAINTS:
- Extend ERPNext Supplier, PO, Item.
- New DocTypes: Supplier Rating, Logistics Task.
- Fixtures: Role "Procurement Officer", Workspace "Supply Chain".
- hooks.py: low-stock alert task.


INTER-RELATIONSHIPS:
- Fleet (Spare parts usage).
- Finance (Procurement costs).
- Governance (Supplier compliance).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py 
- hooks.py jobs.
- Unit tests (`tems/tests/test_supplychain.py`).
