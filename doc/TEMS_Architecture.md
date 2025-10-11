# TEMS Architecture — Layered Overview

Audience: Stakeholders, architects, and senior developers.

## Layers
- Core Platform: Frappe/ERPNext/HRMS v15+ (Users, Roles, Permissions, Employee, Asset, Vehicle, GL, Stock, File/Drive)
- TEMS Domains (apps/tems/tems):
  - Governance, Operations, People, Fleet, Safety, Trade, Informal, Climate, Finance, CRM, Supply Chain, Documents, Insights
- API Layer: `tems.tems_{domain}.api` for whitelisted methods; `handlers.py` for DocEvents; `tasks.py` for schedules
- UI Layer: Workspaces, Client Scripts, Number Cards, Reports/Pages
- Data/Fixtures: Roles, Custom Fields, Workspaces, Reports, Dashboards, Workflows

## Vehicle-Centric Model
- Vehicle is the operational nucleus. Assets (tires, equipment) link to Vehicle; Operations (Journeys, Duty Assignments) always reference Vehicle.
- Costs roll up: Asset → Vehicle → Operations → Finance. Profitability is reported per Vehicle with drill-down.
- Safety risk, Trade crossings, CRM engagements, Documents, and Insights all tie back to Vehicle.

## Cross-Domain Contracts
- People → Fleet: `Driver Qualification` validates `Journey Plan` submission.
- Operations → Safety: `SOS Event` triggers Safety notification; `Control Exception` escalates hourly.
- Trade → Operations: `Border Crossing` associates to `Journey Plan`.
- Documents → People/Fleet: `Document Checklist` and `Verification Document` for employee/vehicle compliance.
- Finance → Fleet/Operations: `Fleet Cost` posts from Work Orders/Fuel Logs; `Allocation Rule` distributes.

## Scheduling & Idempotency
- Use daily/hourly/monthly jobs for reminders, aggregations, and validations. Jobs must be idempotent and safe to re-run.

## Security & Roles
- Fleet Manager: Vehicles, Assets, Maintenance, Fuel
- Operations Manager/Officer: Dispatch, Duty Assignment, Exceptions, SOS
- Safety Officer/Manager: Incidents, Spot Checks
- Finance Manager/Officer: Fleet Costs, Allocation, Profitability
- TEMS Executive/Analyst: Dashboards & Insights

## Packaging
- All code and fixtures live in `apps/tems` only. No core overrides; extend via Links, Fixtures, and Hooks.

## Quality
- Unit tests per domain for critical logic. Smoke test to load workspaces and dashboards.

TASK:
Design and integrate **Cargo** and **Passenger** management features into TEMS.

CONSTRAINTS:
- `Vehicle` (ERPNext) must have a field `vehicle_type` = Cargo | Passenger.
- Cargo operations → handled in `tems_cargo`.
- Passenger operations → handled in `tems_passenger`.
- All operations must link through `tems_operations.Operation Plan` and `Vehicle`.
- Finance and Insights modules must aggregate both types for profitability.
- Ensure all hooks and validations enforce type consistency.

OUTPUTS:
- Updated ERD (VehicleType relationships).
- Folder structure for `tems_cargo` and `tems_passenger`.
- hooks.py updates.
- DocType definitions and fixtures for Cargo and Passenger doctypes.
- Example Operation Plan JSON with linked Cargo or Passenger records.
