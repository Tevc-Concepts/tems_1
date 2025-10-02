# DomainAgent.md

ROLE:
Domain Module Builder for TEMS app (Frappe v15+).

TASKS:
- For each domain (Governance, Operations,People, Fleet, Safety, Trade, Informal, Climate, Finance, CRM, Supply Chain, Documents, Insights) - domain specific prompt in /doc/agentic/domain/{domain}Agent.md:
  - Implement required DocTypes, fields, and relationships.
  - Extend ERPNext/HRMS core DocTypes with Custom Fields where appropriate.
  - Create server methods, Client Scripts, and API endpoints.
  - Add unit tests and sample data patches.
- Maintain modular boundaries between domains while allowing links for triangulation.

CONSTRAINTS:
- Place all code under `apps/tems` application folder.
- Fixtures must define Roles, Workspaces, Reports, and Custom Fields.
- hooks.py must register doc_events for each new DocType.
- No modifications to ERPNext/HRMS/DRIVE/FRAPPE core files.

INTER-RELATIONSHIPS:
- Always define Link fields to connect related domains (e.g., Journey Plan → Driver, Vehicle, Asset).
- Ensure consistent naming and reusable components across modules.

OUTPUTS:
- DocType JSON files under `tems_{domain}/doctype/*`. ( For all doctypes to be created ensure you generate the all 4 files types templates (.js, .json, .py (controller), .py(test) & __init__.py).)
- Workspace JSON fixtures under `tems_{domain}/workspace/*`.
- Unit test files under `tems/tests/test_<module>.py`.
- Example Client Scripts per module.

# DomainAgent.md — Adjustments for Vehicle–Asset Architecture

## 🚨 Core Architecture Rules
These rules apply to **all TEMS domains** to maintain correct system design:

1. **Vehicle as Core Entity**
   - A Vehicle is the **operational unit** across TEMS.
   - Vehicles are used in Operations, Finance, CRM, Safety, HRMS, Supply Chain, and Trade.
   - No other module should directly assign or operate on Assets without passing through Vehicle.

2. **Asset-to-Vehicle Relationship**
   - Assets (tractor, trailer, tires, equipment) always attach to a **Vehicle** (many Assets → one Vehicle).
   - Assets track lifecycle, maintenance, and utilization costs.
   - Assets never link directly to Orders, Operations, or Finance → only through their Vehicle.

3. **Profitability & Costing**
   - Profitability is calculated at **Vehicle level**.
   - Asset-level costs (fuel, tires, spares, etc.) roll up into Vehicle-level profitability.
   - Finance dashboards must provide drill-down: Vehicle → Asset → Transaction.

4. **Cross-Domain Integration**
   - **Fleet** manages Vehicles and their Assets.
   - **Operations** allocates Vehicles to Orders and logs movement.
   - **HRMS** assigns Drivers to Vehicles (not Assets).
   - **Safety** validates Driver + Vehicle competency and logs incidents per Vehicle.
   - **Supply Chain** procures parts that map to Assets → Vehicle.
   - **Trade** associates border crossings, tariffs, and FX costs with Vehicle.
   - **CRM** links Orders and SLAs to Vehicles fulfilling them.
   - **Climate** records emissions and renewable energy use at Vehicle level.
   - **Governance & Documents** link policies and compliance documents to Vehicles.
   - **Insights** aggregates KPIs at Vehicle level with drill-down to Assets.

5. **UI & Workspaces**
   - Workspaces for all roles must present **Vehicle-first views**:
     - Fleet Manager: Vehicle list + linked Assets.
     - Operations Manager: Active Vehicles + Trips.
     - Finance: Vehicle Profitability Dashboard.
     - Safety: Vehicle Risk & Incident Log.

6. **hooks.py Rules**
   - Vehicle status changes should cascade to Operations and Finance.
   - Asset changes update Vehicle lifecycle and cost calculations.
   - No hooks should allow Assets to bypass Vehicle in workflows.

---

## ✅ Application to Each Domain
When implementing a domain:
- Always ask: **“How does this relate to Vehicle?”**
- Ensure **DocTypes link back to Vehicle** either directly or through related logs.
- Ensure **reports roll up to Vehicle** and allow drill-down to Assets.
