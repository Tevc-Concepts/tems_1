# TEMS User Guide

Version: Draft 0.1 (Generated 2025-10-08)

This guide explains how different user roles operate the Transport Excellence Management System (TEMS) across core domains: Fleet, Operations, Safety, Trade, Governance, People, Finance, Climate, Supply Chain, CRM, Informal Economy, Insights, and Documents.

> NOTE: This draft is based on current DocTypes present in the repository (code inspection) and the Product Requirements & ERD. Fields / flows marked (Planned) are specified in PRD but not yet implemented in code.

---
## 1. Core Concepts
- **Workspace / Module**: Functional grouping (e.g., TEMS Fleet, TEMS Operations) exposing DocTypes, reports, dashboards.
- **DocType**: A business object (e.g., Journey Plan, Maintenance Work Order, Border Crossing) with forms, list views, and workflows.
- **Event Hooks**: Automated logic triggered on validate / insert / submit (see `hooks.py`).
- **Scheduled Tasks**: Background jobs computing rollups, reminders, predictive maintenance stubs, compliance notifications.

### 1.1 Lifecycle Status Terms
- *Draft*: Record editable, not yet actioned.
- *Submitted*: Locked for most edits; represents approved / executed state (where submit applies).
- *Cancelled*: Reversal of a submitted record (where supported).

### 1.2 Role Overview (From fixtures)
| Role | Primary Use Cases |
|------|------------------|
| TEMS Executive | Strategic goals, high-level KPIs (Planned) |
| Operations Manager / Officer | Journey and shift planning, trip allocation, operational events, SOS response |
| Fleet Manager / Officer | Vehicle, maintenance work orders, fuel logs, route planning, asset cost rollups |
| Safety Officer / Manager | Journey validation, incidents, risk assessments, spot checks |
| Driver | Execute assigned journeys, provide feedback, pre/post trip inputs (UI/ Mobile – Partial) |
| Maintenance Tech / Maintenance Technician | Execute maintenance work orders, log parts used |
| Finance Manager / Officer | Cost & revenue ledger, FX rates, fleet cost profitability (Partial) |
| Analyst | Dashboards & insights (Planned) |
| HR | Driver qualification, training records, competency matrix |
| Informal Operator | Basic registration & route association (Planned) |
| Border Agent | Border crossing execution & customs clearance data |
| Community Leader | Local data inputs (Planned) |
| Read-Only Auditor | Compliance / audit trail review |
| Business Transformation Officer | Change initiatives & adoption monitoring (Planned) |

---
## 2. Module Guides

### 2.1 Fleet Management
Key DocTypes: Vehicle (ERPNext core), Journey Plan, Maintenance Work Order, Maintenance Part Item, Fuel Log, Route Planning, Asset Utilization Log.

#### 2.1.1 Journey Plan
Purpose: Defines an upcoming or in-progress journey linking Route, Driver, Vehicle, schedule, and risk metadata.
Fields (current): Route (reqd), Driver (reqd), Vehicle (optional), Start Time, End Time, Risk Score (float), Weather Snapshot (JSON raw capture), SOS Contact (Data).
Hooks: `validate` via Safety module (driver competence), `after_insert` for potential enrichment.
Typical Flow:
1. Fleet/Operations user creates Journey Plan selecting an existing Route Planning entry and a Driver.
2. (Optional) Assign Vehicle if allocation already known.
3. System validation checks driver active status (Client Script + server validation stub).
4. Save as Draft; on further process (planned future) may be submitted / linked to Trip Allocation.
Edge Cases: Missing vehicle (allowed), expired driver qualification (should block once logic implemented), overlapping schedules (Planned), route risk score calculation (Planned AI enrichment).

#### 2.1.2 Maintenance Work Order
Purpose: Track maintenance tasks against a Vehicle / Asset with parts consumed.
Hooks: After insert / on update recalc costs and predictive maintenance signals.
Flow:
1. Create Work Order referencing Vehicle.
2. Add child Maintenance Part Items (spare parts) referencing Spare Part or Asset.
3. Submit when completed; cost rolls up to vehicle profitability.

#### 2.1.3 Fuel Log
Purpose: Capture fueling events for Vehicle (quantity, cost) – contributes to efficiency reporting (Planned reports).

#### 2.1.4 Route Planning
Purpose: Define named routes with distance, risk, checkpoints (Planned additional fields). Used by Journey Plan.

#### 2.1.5 Asset Utilization Log (Planned Usage)
Purpose: Capture runtime hours, distance; feed into availability and reliability analytics.

KPIs (Planned): Open Work Orders, Fuel Efficiency by Vehicle, Predictive Maintenance Alerts.

### 2.2 Operations
DocTypes: Operation Plan, Trip Allocation, Movement Log, Operations Event, Control Exception (Planned), SOS Event, Dispatch Schedule (Planned), Shift Plan, Shift Team Member, Planned Departure (Planned), Duty Assignment (present but not inspected), Trip Allocation.

Example Flow (Daily Operations):
1. Operation Plan created for a set date/shift assigning target vehicles & drivers (before_submit ensures vehicle available).
2. Trip Allocation entries created referencing Journey Plans ensuring driver/vehicle validity.
3. Movement Logs update vehicle status (on_update handler). Could feed into availability checks.
4. Operations Events log notable occurrences (breakdowns, delays) publishing real-time notifications.
5. SOS Event triggers urgent alert; handler publishes to realtime channel for response.
6. End-of-day scheduled task generates operations report (`generate_daily_operations_report`).

Edge Cases: Vehicle double booking, driver fatigue rules (Planned), missed departures, SOS escalation chain (Planned workflow).

### 2.3 Safety & Risk
DocTypes: Journey Plan (validation), Incident Report, Incident Participant, Risk Assessment, Safety Incident (alias / variant), Spot Check, Spot Check Photo.

Incident Handling Flow:
1. User logs Incident Report (draft) with context (driver, vehicle, journey plan if available).
2. Submit triggers logging against vehicle and potential analytics rollup.
3. Risk Assessment records hazards and mitigation; `before_submit` validates vehicle risk thresholds.
4. Spot Checks (Leadership / Safety) create on-site observation records; handlers unify update/submit.
5. Scheduled emissions aggregation tasks (daily/monthly) compute sustainability metrics (aligned with Climate module).

### 2.4 Governance
DocTypes: Governance Policy, Compliance Obligation, Governance Meeting, Leadership Meeting, Meeting Action Item, Strategic Goal, Compliance Audit, Approval Matrix / Role.
Flows:
- Policy Lifecycle: Draft → Review (Planned Workflow) → Published; `apply_policy_to_vehicle` hook for propagation (stub reference).
- Compliance Audit: Create schedule, record findings & evidences (child table). On submit triggers handler for status summarization.
- Strategic Goal: Define KPIs and target; future linkage to Dashboard (Planned).
- Spot Checks (See Safety overlap) produce governance oversight evidence.

### 2.5 People & Competency
DocTypes: Driver Qualification, Training Record, Competency Matrix, Succession Plan, Succession Candidate, Incident Involvement.
Key Flow: Driver Qualification expiry triggers reminders (`remind_expiring_driver_docs` daily) and should block Journey Plan validation (planned logic extension in `validate_driver_competence`).
Training Records feed Competency Matrix; Succession Plan identifies critical roles and candidates.

### 2.6 Trade (Cross-Border)
DocTypes: Trade Lane, Trade Lane Border Post, Border Crossing, Customs Clearance, Trade Lane Document.
Flow:
1. Define Trade Lane (route including border posts, docs required).
2. Journey Plan associated with Border Crossing when traversing an international segment.
3. Border Crossing submission logs vehicle crossing (`log_vehicle_crossing`).
4. Customs Clearance handles tariff, HS codes (Planned fields), compliance statuses.

### 2.7 Supply Chain
DocTypes: Procurement Order (hook on_submit), Spare Part (in Fleet domain), link to Maintenance Work Order consumption.
Flow: Procurement Order submission triggers handler to link parts to assets (ensuring traceability of part usage vs. vehicle lifecycle).

### 2.8 Finance
DocTypes: Cost And Revenue Ledger (profitability updates), Fleet Cost (Planned), Allocation Rule (Planned), FX Rates (daily update task), Emission Log cost externality (Planned integration).
Flow: Ledger updates recalc vehicle profitability; scheduled tasks update FX & interest; results inform replacement planning.

### 2.9 Climate & ESG
DocTypes: Climate Risk Journey, Climate Risk Events, Emissions Log.
Hooks: Emission Log updates roll up emissions to vehicles; daily/monthly aggregation tasks compute emissions KPIs.
Future: Carbon offset suggestions, adaptation strategies (Planned).

### 2.10 Informal Economy
DocTypes Present: (Informal Operator Profile, Operator Route Association) – Not inspected in code listing (assumed under `tems_informal`).
Flows: Registration → Route Association → Trip Matching (Planned) → Feedback & Microfinance integration.

### 2.11 CRM
DocTypes: Field Service Request (Planned), Customer Feedback, Order (hook on_submit linking to vehicle).
Flows: Order processed; vehicle utilization and customer satisfaction feed analytics.

### 2.12 Insights & Dashboards
DocTypes: KPI Config, Dashboard, Report Subscription (some planned, some core Frappe). Number Cards fixture (temporarily trimmed) will expose metrics like open work orders, active incidents, risk scores.

### 2.13 Documents & Compliance
DocTypes: Document Checklist, Compliance Document, Verification Document (planned naming), with hook validating vehicle document currency.

---
## 3. Cross-Cutting Automation
| Area | Mechanism | Current Implementation |
|------|-----------|------------------------|
| Driver Active Validation | Client Script + server validate hook | Stub; extend `validate_driver_competence` for full rules |
| Predictive Maintenance | Daily scheduled task | Stub to compute maintenance signals |
| Emissions Aggregation | Daily & Monthly tasks | Implemented task names (logic TBD) |
| FX Rate Update | Daily scheduled task | `update_fx_rates` stub |
| Compliance Notifications | Daily tasks | Governance handlers & tasks stubs |
| Operations Reports | Daily/hourly/weekly/monthly tasks | Multi-frequency sync checkpoints |

---
## 4. Typical User Journeys
### 4.1 Plan & Execute a Journey
1. Create/confirm Route Planning.
2. Create Journey Plan (assign Driver, Start Time, optional Vehicle).
3. Validate driver status (system). Fix issues if blocked.
4. Create Trip Allocation linking Journey Plan once vehicle confirmed.
5. During execution log Operations Events or SOS.
6. Post journey close Movement Log or set End Time; update risk/incident records if needed.
7. Review analytics dashboard (risk score trends – Planned).

### 4.2 Record Maintenance
1. Create Maintenance Work Order; specify vehicle.
2. Add Maintenance Part Items (pull from Spare Parts inventory).
3. Submit when done; verify cost rolled into vehicle profitability dashboard.

### 4.3 Handle Incident
1. Open Incident Report referencing Journey Plan & Vehicle.
2. Add Participants (Incident Participant child - link employees/drivers).
3. Submit → triggers safety & governance hooks.
4. Create Risk Assessment if systemic risk uncovered.
5. Track corrective actions (Planned linkage to tasks/workflow).

### 4.4 Governance Audit
1. Create Compliance Audit with scope & schedule.
2. Add Evidence records (child table) referencing documents & policies.
3. Submit audit → handler processes status (e.g., pass rate).
4. Use Spot Checks for follow-up observations.

### 4.5 Driver Qualification Renewal
1. HR monitors daily reminder list for upcoming expiries.
2. Update Driver Qualification DocType with new validity dates.
3. Journey Plan creation again passes validation.

---
## 5. Data Quality & Validation Rules (Current vs Planned)
| Rule | Current State | Planned Enhancement |
|------|---------------|---------------------|
| Driver must be active | Client script call to people API | Enforce in server validate + status badge |
| Driver qualification not expired | Placeholder | Fetch latest qualification expiry & block |
| Vehicle availability (no overlapping assignment) | Handler on Operation Plan submit | Pre-check on Journey Plan & Trip Allocation |
| Route required for Journey Plan | Enforced (reqd=1) | Pre-populate weather & risk metrics |
| Maintenance cost rollup | On update handler | Add TCO & predictive signals |
| Emissions aggregation | Task names only | Actual calc from Emission Log fields |

---
## 6. Security & Permissions
- Journey Plan accessible to System Manager, Fleet Manager/Officer per DocType permissions.
- Additional roles (Safety Officer, Driver) will need tailored read/create rights (extension recommended).
- Compliance / Audit records restricted to Governance roles (configure granular permissions as implemented).
- Sensitive cost and profitability only for Finance roles.

Recommendation: Add Role Permissions Manager matrix documentation once stabilized.

---
## 7. Reporting & Analytics (Early Stage)
Available / Planned Reports (based on code & PRD):
- Open Maintenance Work Orders
- Fuel Efficiency by Vehicle (Planned)
- Border Dwelling (existing report referencing Journey Plan)
- Emissions Summary (Planned scheduled aggregation output)
- Driver Qualification Expiry (daily reminder output)

---
## 8. Administration & Setup
1. Install app and ensure fixtures load (Roles).
2. Configure core master data: Employees, Vehicles, Spare Parts, Routes.
3. Set up scheduled jobs (bench scheduler enabled) to activate reminders and rollups.
4. Deploy client scripts (fixtures) for validation prompts.
5. Assign roles to users per responsibilities table.

Environment Health Checklist:
- Scheduler running (check `bench doctor` / logs).
- No failed jobs in background worker logs (`worker.log`, `scheduler.log`).
- Hooks not erroring (inspect `frappe.log`).

---
## 9. Glossary
- Journey Plan: Planned movement record linking driver/route/vehicle.
- Trip Allocation: Specific resource assignment tying Journey Plan to operations schedule.
- Operations Event: Real-time operational notable event.
- SOS Event: High severity alert requiring immediate response.
- Risk Assessment: Structured hazard evaluation with mitigation.
- Compliance Audit: Formal audit capturing findings & evidences.
- Driver Qualification: Record of driver’s license, medical, certification validity.

---
## 10. Future Enhancements Indicators
Labels “(Planned)” denote PRD-backed but not yet implemented features. Track them in backlog to avoid test false negatives.

---
## 11. Change Log Reference
See `CHANGELOG.md` for domain introduction milestones (e.g., Fleet domain introducing Journey Plan, Maintenance Work Order, Fuel Log).

---
## 12. Feedback
Submit issues via repository issue tracker with category tags: [BUG] [ENHANCEMENT] [DOC] [TEST].

---
End of User Guide.
