# TEMS Domains — Master TODO & Data Plan (13 domains)

Assumptions
- We will cover these 13 domains: Governance, Operations, People, Fleet, Safety, Trade, Informal Economy, Climate, Finance, CRM, Supply Chain, Documents, Insights.
- Operations and Governance are treated as distinct domains. If you prefer to merge or rename, we can consolidate later.
- All work lives under `apps/tems` and follows the instructions in `.github/instructions/tems project.instructions.md` and `doc/agents/DomainAgent.md`.

Global Prerequisites (once per repo)
- [ ] Fixtures: Base Roles fixture (TEMS Administrator, TEMS Executive, Operations Manager, Operations Officer, Fleet Officer, Fleet Manager, Safety Officer, Safety Manager, Business Transformation Officer, Driver, Maintenance Technician, Informal Operator, Border Agent, Community Leader, Read-Only Auditor)
- [ ] Hooks: Ensure `app_include_css/js`, `web_include_css/js`, `fixtures`, `doc_events`, and `scheduler_events` are declared in `apps/tems/tems/hooks.py`
- [ ] Per-domain modules: each domain lives under its own package `tems_{domain}` inside `apps/tems/tems/`. Example: `tems_governance`.
- [ ] Module naming: set DocType JSON `module` to human label "TEMS {Domain}" (e.g., "TEMS Governance"). Add the module label to `apps/tems/tems/modules.txt`.
 [ ] API placement: domain server methods live under `apps/tems/tems/tems_{domain}/api/` and hooks refer to `tems.tems_{domain}.api.*`.
 Server method: `tems.tems_governance.api.next_reviews()` to list policies due for review
Execution Order (recommended)
1) Governance → 2) Operations → 3) People → 4) Fleet → 5) Safety → 6) Trade → 7) Informal Economy → 8) Climate → 9) Finance → 10) CRM → 11) Supply Chain → 12) Documents → 13) Insights

Definition of Done (applies to each domain)
- [ ] DocTypes implemented with fields and links to core ERPNext/HRMS doctypes
- [ ] Custom Fields (fixtures) for extending core doctypes where needed
- [ ] Role-based permissions set in DocType JSON and/or fixtures
- [ ] Client Scripts for essential UI validations/UX
- [ ] Server methods (API) and hooks registered in `hooks.py` if needed
- [ ] Workspace JSON fixture for the domain’s role(s)
- [ ] At least 1 Report (Query/Script) and 1 Insight chart/dashboard link
- [ ] Scheduled job(s) if relevant (idempotent!)
- [ ] Seed data patch with valid, relational sample dataset
- [ ] Unit tests for 1–2 critical server methods and a small smoke test
- [ ] Bench cycle verified locally: migrate, build, clear-cache, restart

---

## 1) Governance
Goal: Capture organizational policies, obligations, approvals, meetings and compliance.

Primary DocTypes (new)
- Governance Policy: code, title, category, owner (Employee), effective_from, review_cycle, status, attached_files (Table), acknowledgement_required (Check)
- Compliance Obligation: code, title, regulator, due_frequency, next_due_date, evidence_required, status
- Approval Matrix: process_name, min_amount, max_amount, approver_role(s), escalation_role, sla_hours
- Governance Meeting: meeting_date, participants (Table Link Employee), agenda, decisions (Long Text), action_items (Table)

Links to Core
- Link to Company, Department, Employee (HRMS)
- Optional: Project link when policy relates to initiatives

Custom Fields on Core
- Employee: governance_role (Select)
- Department: compliance_owner (Link Employee)

Workspace & Reports
- Workspace: “Governance” (shortcuts to Policies, Obligations, Meetings; link to Drive folder; link to Insights dashboard)
- Reports: “Policy Review Schedule” (Query), “Obligation Status Aging” (Script)

Server/API & Hooks
- Server method: `tems.tems_governance.api.next_reviews()` to list policies due for review
- Hook: daily scheduler to notify owners of upcoming reviews and obligations

Client Scripts
- Validate that next_due_date respects frequency
- Prevent submit if evidence_required and no evidence attached

Seed Data (fixtures/patch)
- Policies: 5
- Obligations: 10 (varied regulators and due dates)
- Approval Matrix entries: 3 (low/medium/high bands)
- Meetings: 4 with 2–5 participants each

Tests
- Unit: ensure `next_reviews()` returns only items due within N days
- Unit: obligation cannot be set to “Compliant” without evidence

---

## 2) Operations
Goal: Control room operations — dispatch, shift/roster, duty assignment, on-time performance, exceptions and SOS handling.

Primary DocTypes (new)
- Dispatch Schedule: date, route (Link Route Planning), shift (Select), dispatcher (Link Employee), planned_departures (Table: time, asset optional), notes
- Shift Plan: date, shift_type (Link Shift Type), supervisor (Link Employee), team (Table Link Employee)
- Duty Assignment: journey_plan (Link Journey Plan), driver (Link Employee), assistant (Link Employee), schedule_slot (Datetime), status (Planned/Assigned/In Progress/Completed/Cancelled)
- Control Exception: type (delay, breakdown, no_show, overload), severity, occurred_at, asset (Link Asset), journey_plan (Link Journey Plan), description, resolution, status, sla_minutes
- Operations Event: journey_plan, event_time, location (lat, lng, geohash), event_type (depart, arrive, checkpoint, delay_reason), variance_minutes
- SOS Event: created_at, reporter (Link Employee or Data phone), location (lat, lng, geohash), asset (Link Asset), journey_plan (optional), status (Open/Acknowledged/Resolved), resolved_at, notes

Links to Core
- Journey Plan (Fleet), Employee (HRMS), Asset/Vehicle (ERPNext), Route Planning (Fleet), Shift Type (HRMS)

Custom Fields on Core
- Journey Plan: dispatch_status (Select), delay_reason (Small Text), otp_variance_min (Float)
- Asset: radio_id (Data)
- Employee: control_room_role (Select)

Workspace & Reports
- Workspace: “Operations Control” (shortcuts: Dispatch Schedule, Duty Assignment, Control Exception, SOS Event; link to fleet-dashboard page and Drive folder)
- Reports: “On-time Performance (OTP) by Route/Shift”, “Exceptions Aging”, “Shift Coverage”

Server/API & Hooks
- Server: `tems.api.operations.compute_otp(from_date, to_date, route?)`
- Realtime: publish `operations_event` and `sos_event` to Socket.IO namespace (site) on create/update
- Scheduler: hourly job to escalate overdue Control Exceptions; immediate notify Safety on SOS Event creation

Client Scripts
- Duty Assignment: prevent submit if driver invalid (uses People API)
- Control Exception: require resolution prior to Close; compute SLA breach flag

Seed Data
- Shift Plans: 14 (two weeks × 1/day)
- Dispatch Schedules: 14 with 3–8 planned_departures each
- Duty Assignments: 50
- Operations Events: 200 (depart/arrive/checkpoints with variance)
- Control Exceptions: 20 (mix of types and severities)
- SOS Events: 3

Tests
- Unit: `compute_otp` calculates OTP% correctly with early/late thresholds
- Unit: creating SOS Event triggers Safety notification hook

---

## 3) People
Goal: Extend HRMS for driver qualifications, training, competency and incident participation.

Primary DocTypes (new)
- Driver Qualification: employee (Link Employee), license_no, license_class, medical_clearance (Date), expiry_date, verified_by, verification_date, status
- Training Record: employee, training_type, provider, start_date, end_date, certificate_id, status
- Incident Involvement: incident (Link Safety Incident), employee, role (driver/assistant), notes

Links to Core
- HRMS Employee, Attendance, Shift Type

Custom Fields on Core
- Employee: driver_badge_id, emergency_contact_phone

Workspace & Reports
- Workspace: “People & Drivers”
- Reports: “Expiring Driver Qualifications” (Query), “Training Compliance by Dept” (Script)

Server/API & Hooks
- Server method: `tems.api.people.validate_driver_active(employee)` used by Journey Plan
- Hook: on Employee validate, sync driver fields from HRMS where relevant

Client Scripts
- Prevent save if qualification expiry_date < today

Seed Data
- Employees: 20 (ensure role distribution)
- Driver Qualification: 15 (2 expired for negative test)
- Training Records: 30

Tests
- Unit: `validate_driver_active` returns False for expired qualifications

---

## 4) Fleet
Goal: Trips, assets, maintenance and route planning.

Primary DocTypes (new)
- Journey Plan: route, driver (Link Employee), vehicle (Link Asset), start_time, end_time, risk_score, weather_snapshot (JSON), sos_contact
- Maintenance Work Order: asset (Link Asset), vendor (Link Supplier), status, parts_used (Table Item), planned_date, completion_date, cost
- Fuel Log: asset, odometer, liters, price_per_liter, total_cost, station, geohash
- Route Planning: name, waypoints (Table), distance_km, duration_estimate
- Waypoint: name, lat, lng, geohash, sequence, checkpoint_type

Links to Core
- ERPNext Asset/Vehicle, Item, Supplier, Stock Entry (for parts usage)

Custom Fields on Core
- Asset: vehicle_type (Select), availability_status (Select)

Workspace & Reports
- Workspace: “Fleet Manager” (shortcuts to Asset, Journey Plan, Work Orders)
- Reports: “Open Work Orders”, “Fuel Efficiency by Asset”, “Journey On-time Performance”

Server/API & Hooks
- `tems.api.journey.validate_journey` and `on_submit`
- Daily compute: asset availability, utilization metrics

Client Scripts
- Journey Plan: prevent submit if driver invalid (uses People API)

Seed Data
- Assets/Vehicles: 20
- Journey Plans: 40
- Fuel Logs: 200
- Work Orders: 25 (various statuses)
- Routes/Waypoints: 10 routes; 6–20 waypoints/route

Tests
- Unit: `validate_journey` rejects expired drivers
- Unit: fuel cost totals computed correctly

---

## 5) Safety
Goal: Field inspections, spot checks, safety incidents and risk assessments.

Primary DocTypes (new)
- Spot Check: inspector (Employee), photos (File Table), gps (lat,lng, geohash), notes, findings (Table)
- Safety Inspection: asset, checklist_template, result, defects (Table), attachments
- Safety Incident: date_time, location, severity, people_involved (Table Link Employee), vehicle, cause, corrective_action, status
- Risk Assessment: activity, hazards (Table), risk_score, mitigations (Table), review_date
- Checklist Template: name, items (Table: item, criticality)

Links to Core
- Employee, Asset, File (Drive)

Custom Fields on Core
- Asset: last_inspection_date, risk_category

Workspace & Reports
- Workspace: “Safety”
- Reports: “Incidents by Severity/Month”, “Inspection Failures by Asset”

Server/API & Hooks
- File uploads linked to Drive folders
- Hook: notify Safety Officer on high-severity incidents

Client Scripts
- Prevent close if corrective_action missing for non-trivial severity

Seed Data
- Spot Checks: 30 (with sample photo refs)
- Inspections: 40
- Incidents: 12 (2 high severity)
- Templates: 5

Tests
- Unit: cannot close incident without corrective_action when severity >= Medium

---

## 6) Trade
Goal: Cross-border trade operations, crossings, and clearances linking to ERPNext sales/stock.

Primary DocTypes (new)
- Trade Lane: origin_country, destination_country, border_posts (Table), documents_required (Table)
- Border Crossing: journey_plan, border_post, arrival_time, departure_time, wait_duration, officer (Link Employee)
- Customs Clearance: shipment_ref (Link Delivery Note/Sales Invoice), broker, fee, status, documents (Files)

Links to Core
- Sales Order, Delivery Note, Sales Invoice, Item, Customer

Custom Fields on Core
- Delivery Note: trade_lane (Link), export_ref

Workspace & Reports
- Workspace: “Trade & Borders”
- Reports: “Border Dwell Time”, “Clearance Fees by Broker”

Server/API & Hooks
- Server: compute dwell_time, associate to Journey Plan
- Hook: notify when clearance status = Released

Client Scripts
- Validate border_post belongs to trade lane

Seed Data
- Trade Lanes: 6
- Border Crossings: 25
- Clearances: 15

Tests
- Unit: border dwell time computed correctly

---

## 7) Informal Economy
Goal: Capture informal operators, markets, and lightweight KYC.

Primary DocTypes (new)
- Informal Operator Profile: name, phone, ussd_id, id_type, id_number, photo, markets (Table)
- Market: name, location (lat,lng, geohash), operating_days, fees
- Operator Route Association: operator (Link), route (Link Route Planning), start_date, status

Links to Core
- Customer (optional), Contact

Custom Fields on Core
- Customer: informal_operator (Check), ussd_id

Workspace & Reports
- Workspace: “Informal Economy”
- Reports: “Active Informal Operators”, “Market Participation”

Server/API & Hooks
- Lightweight KYC validation

Client Scripts
- Phone format validation, duplicate phone guard

Seed Data
- Operators: 30
- Markets: 10
- Associations: 40

Tests
- Unit: cannot create duplicate operator by phone + id_type/id_number

---

## 8) Climate
Goal: Emissions, weather impacts, and climate risk events.

Primary DocTypes (new)
- Emissions Log: asset, journey_plan, fuel_liters, emission_factor, co2e_kg
- Climate Risk Event: date, type (flood, heat, storm), severity, location, impact, related_journeys (Table)
- Weather Snapshot: journey_plan, source, json_payload, captured_at

Links to Core
- Asset, Journey Plan, Company

Custom Fields on Core
- Journey Plan: weather_snapshot (JSON), co2e_kg (Float)

Workspace & Reports
- Workspace: “Climate”
- Reports: “Emissions by Asset/Month”, “Risk Events Map”

Server/API & Hooks
- Server: compute emissions from fuel logs
- Hook: nightly aggregation of emissions

Client Scripts
- N/A (minimal)

Seed Data
- Emissions Logs: 120
- Risk Events: 8
- Weather Snapshots: 40

Tests
- Unit: emissions = liters × factor

---

## 9) Finance
Goal: Fleet cost control, leasing/loans, and allocation to cost centers.

Primary DocTypes (new)
- Fleet Cost: asset, cost_type (fuel, maintenance, toll, fine), amount, date, reference_doctype/name
- Lease/Loan: asset, financier, start_date, end_date, principal, rate, schedule (Table)
- Allocation Rule: cost_type, allocation_basis (km, hours, trips), cost_center, percentage

Links to Core
- GL Entry, Purchase Invoice, Payment Entry, Cost Center

Custom Fields on Core
- Asset: cost_center (Link)

Workspace & Reports
- Workspace: “Finance (TEMS)”
- Reports: “Total Cost of Ownership”, “Allocated Costs by Cost Center”

Server/API & Hooks
- Server: post Fleet Cost from Work Orders/Fuel Logs
- Hook: daily interest accrual for loans

Client Scripts
- Validate allocation percentages sum to 100%

Seed Data
- Fleet Costs: 200
- Loans/Leases: 5
- Allocation Rules: 6

Tests
- Unit: allocation distributes amounts correctly by basis

---

## 10) CRM
Goal: Field service, customer feedback, and route-based engagements.

Primary DocTypes (new)
- Field Service Request: customer, address, request_type, description, priority, status, assigned_to (Employee)
- Customer Feedback: customer, journey_plan (optional), rating, comments
- Visit Plan: customer, proposed_date, route (optional), status

Links to Core
- Customer, Contact, Sales Order (optional)

Custom Fields on Core
- Customer: service_sla_hours (Int)

Workspace & Reports
- Workspace: “CRM (TEMS)”
- Reports: “FSR Aging”, “Customer Ratings Trend”

Server/API & Hooks
- Hook: auto-assign requests by territory/route

Client Scripts
- Prevent close if rating < 3 without corrective notes

Seed Data
- FSR: 25
- Feedback: 40
- Visit Plans: 20

Tests
- Unit: SLA breach detector for FSR

---

## 11) Supply Chain
Goal: Spares, vendors, maintenance BOMs and procurement flow.

Primary DocTypes (new)
- Spare Part: item (Link Item), asset_compatibility (Table), min_stock, reorder_qty
- Spare Request: asset, requested_by, parts (Table Link Item + qty), priority, status
- Vendor Performance: supplier, on_time_score, quality_score, notes, period

Links to Core
- Item, Supplier, Purchase Order/Receipt, Stock Entry

Custom Fields on Core
- Item: is_spare_part (Check), asset_model

Workspace & Reports
- Workspace: “Supply Chain (TEMS)”
- Reports: “Spare Consumption by Vehicle”, “Vendor Performance Trend”

Server/API & Hooks
- Hook: on Work Order submit → create Spare Request for shortages

Client Scripts
- Warn when requested parts below min_stock

Seed Data
- Spare Parts: 60 (map to Items)
- Spare Requests: 25
- Vendor Performance: 12 months for 3 suppliers

Tests
- Unit: shortage detection triggers Spare Request

---

## 12) Documents
Goal: Operational document management with Drive integration.

Primary DocTypes (new)
- Verification Document: owner_doctype/owner_name, document_type, issue_date, expiry_date, file (Link File), status
- Document Checklist: context (vehicle/driver/trip), items (Table: doc_type, required)
- Document Review: doc (Link Verification Document), reviewer (Employee), outcome, notes

Links to Core
- File (Drive), Employee, Vehicle, Journey Plan

Custom Fields on Core
- Vehicle: registration_doc (Link Verification Document)
- Employee: license_doc (Link Verification Document)

Workspace & Reports
- Workspace: “Documents”
- Reports: “Expiring Documents (30/60/90)”, “Checklist Compliance”

Server/API & Hooks
- Hook: nightly reminder for upcoming expiries

Client Scripts
- Prevent submit if required checklist items missing

Seed Data
- Verification Docs: 40 (mix of assets/employees)
- Checklists: 6
- Reviews: 20

Tests
- Unit: expiry reminders select correct windows

---

## 13) Insights
Goal: Dashboards and analytics across domains via Frappe Insights.

Assets & Fixtures
- Create Insights dashboards (JSON fixtures) for: Fleet Manager, Safety, Finance, CRM, Supply Chain; link from role workspaces
- At least 2 KPI cards per domain where meaningful (availability %, open WOs, incident rate, etc.)

Reports
- Ensure each domain has at least one Query or Script Report backing the insights

Server/API & Hooks
- Nightly refresh of materialized tables (if any created) or precomputed metrics

Seed Data
- N/A (uses domain datasets)

Tests
- Smoke: dashboards load and widgets resolve without errors

---

## Cross-Domain Link Map (high level)
- People ↔ Fleet: Driver Qualification → Journey Plan validation
- Safety ↔ Fleet: Inspections/Incidents reference Asset/Journey
- Documents ↔ People/Fleet/Safety: Verification Docs & Checklists
- Trade ↔ Fleet/CRM: Shipments and crossings link to Journey/Customer
- Finance ↔ Fleet/Supply Chain: Costs flow from Fuel/WO/Spare usage
- Insights ↔ All: Dashboards consume Reports from each domain

---

## Delivery Rhythm per Domain (repeatable)
1) Model DocTypes and links via Desk; ensure indices on frequently queried fields (status, dates, geohash, route_id)
2) Add client scripts (validations) and server methods (API)
3) Export fixtures (roles, workspaces, custom fields, reports)
4) Write unit tests for core server logic + a smoke test
5) Create seed patch under `apps/tems/tems/patches/v15/` and register if needed
6) Verify with: bench migrate, build, clear-cache, restart; open forms, run report

Notes
- Use Drive for uploads (Photos/Docs). Link File records instead of raw binary fields when possible.
- Keep server jobs idempotent; expect retries.
- Keep payloads for realtime events small and fetch details via REST when needed.
