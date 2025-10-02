# TEMS Domains — TODO vs Implemented Status (Snapshot)

This status compares the checklist in `doc/agents/domains/TEMS-Domain-TODO.md` against features present under `apps/tems/tems/`.

Legend: Done ✅, Partial ◐, Pending ⏳

## Global Prerequisites
- Fixtures (Roles): ✅ role.json present; includes domain roles
- Hooks declarations: ✅ hooks.py defines app/web includes, fixtures, doc_events, scheduler_events
- Per-domain modules: ✅ `tems_{domain}` packages exist for all 13
- Module naming in DocTypes: ✅ modules.txt lists all "TEMS {Domain}"
- API placement: ✅ e.g., `tems.tems_governance.api.next_reviews`

## 1) Governance
- DocTypes: ✅ Governance Policy, Compliance Obligation, Approval Matrix, Governance Meeting
- Custom Fields: ◐ Employee/Department fields not verified in fixtures
- Role permissions: ✅ via DocType JSON/fixtures
- Client Scripts: ◐ validations not found for compliance evidence
- Server/API/Hooks: ✅ `next_reviews`, daily notify scheduled
- Workspace & Reports: ✅ workspace, reports present (Policy Review Schedule, Obligation Status Aging)
- Scheduled jobs: ✅ daily notifications
- Seed data: ✅ seed_governance.py
- Tests: ✅ tests/test_governance.py

## 2) Operations
- DocTypes: ✅ Dispatch Schedule, Shift Plan, Duty Assignment, Control Exception, Operations Event, SOS Event
- Custom Fields on Core: ◐ Journey Plan fields in Fleet; Employee/Asset fields presence TBD
- Role permissions: ✅ per DocType JSON
- Client Scripts: ✅ duty_assignment_validate_today client script exists
- Server/API/Hooks: ◐ placeholders (needs compute_otp, realtime publish)
- Workspace & Reports: ✅ workspace present; reports present
- Scheduled jobs: ✅ hourly escalation, daily/weekly/monthly tasks in hooks
- Seed data: ✅ seed_operations.py
- Tests: ⏳ compute_otp and SOS hook tests not present

## 3) People
- DocTypes: ✅ Driver Qualification, Training Record, Incident Involvement
- Custom Fields: ◐ employee phone/emergency not verified
- Client Scripts: ◐ expiry validation not found
- Server/API/Hooks: ◐ validate_driver_active referenced but not located
- Workspace/Reports: ✅ present
- Seed data: ✅ seed_people.py
- Tests: ⏳ validate_driver_active unit test missing

## 4) Fleet
- DocTypes: ✅ Journey Plan, Maintenance Work Order, Fuel Log, Route Planning
- Custom Fields: ✅ Vehicle custom fields fixture exists (assigned driver, GPS, etc.)
- Client Scripts: ◐ journey validate not enforced (placeholder in api/journey.py)
- Server/API/Hooks: ◐ validate_journey stub; daily compute metrics TBD
- Workspace/Reports: ✅ present
- Seed data: ✅ seed_fleet.py
- Tests: ⏳ fuel totals and journey validation tests not present

## 5) Safety
- DocTypes: ✅ Safety Incident, Spot Check, Incident Participant (+ Settings)
- Client Scripts: ✅ workflow/validation in place (workflow fixture present)
- Server/API/Hooks: ✅ overdue investigations tasks and hooks
- Reports/Workspace: ✅ present
- Seed data: ✅ seed_safety.py
- Tests: ⏳ incident close validation test not found

## 6) Trade
- DocTypes: ✅ Trade Lane (+ Border Post/Doc tables), Border Crossing, Customs Clearance
- Custom Fields: ◐ Delivery Note custom fields not verified
- Server/Hooks: ✅ crossing hook scaffolding
- Reports/Workspace: ✅ present
- Seed data: ✅ seed_trade.py
- Tests: ⏳ dwell time unit test missing

## 7) Informal Economy
- DocTypes: ✅ Informal Operator Profile, Market, Operator Route Association
- Custom Fields: ✅ Customer fields indicated; verify in fixtures
- Reports/Workspace: ✅ present
- Seed data: ✅ seed_informal.py
- Tests: ⏳ duplicate operator test missing

## 8) Climate
- DocTypes: ✅ Emissions Log
- Server/API/Hooks: ✅ daily/monthly aggregation stubs
- Custom Fields: ✅ Journey Plan JSON field present
- Workspace/Reports: ✅ present
- Seed data: ✅ seed_climate.py
- Tests: ✅ test_climate.py present

## 9) Finance
- DocTypes: ✅ Fleet Cost, Allocation Rule
- Server/API/Hooks: ✅ profitability roll-up hooks declared
- Reports/Workspace: ✅ present
- Seed data: ✅ seed_finance.py
- Tests: ⏳ allocation distribution unit test missing

## 10) CRM
- DocTypes: ✅ Field Service Request, Customer Feedback
- Server/API/Hooks: ◐ auto-assign by territory/route TBD
- Workspace/Reports: ✅ present
- Seed data: ✅ seed_crm.py
- Tests: ⏳ SLA breach test missing

## 11) Supply Chain
- DocTypes: ✅ Spare Part
- Server/API/Hooks: ✅ shortage handler linked to Work Order submit in hooks
- Workspace/Reports: ✅ present
- Seed data: ✅ seed_supply_chain.py
- Tests: ⏳ shortage triggers Spare Request test missing

## 12) Documents
- DocTypes: ✅ Document Checklist, Document Checklist Item (Verification Document TBD)
- Server/API/Hooks: ✅ expiry reminders scheduled (scaffolding)
- Workspace/Reports: ✅ present
- Seed data: ✅ seed_documents.py
- Tests: ✅ tests/test_documents.py present

## 13) Insights
- Assets & Fixtures: ✅ number cards/workspaces exist; dashboards fixtures included
- Reports: ✅ each domain has at least one report
- Server/API/Hooks: ✅ nightly refresh scaffolding
- Tests: ✅ smoke via workspace load implicit; explicit tests TBD

## Summary
Strong coverage across Governance, Fleet, Operations, Safety, Trade, Documents, Climate, Finance, CRM, Supply Chain, Informal, Insights. People and several unit-test items remain to be implemented. See domain TODOs for the missing validations and tests noted above.
