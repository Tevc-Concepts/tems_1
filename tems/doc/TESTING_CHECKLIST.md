# TEMS End-to-End Testing Checklist
Version: Draft 0.1 (2025-10-08)
Scope: Covers current implemented DocTypes & hooks plus PRD-aligned near-term behaviors. Mark Planned items separately so failures do not block current release unless explicitly in scope.

Legend:
[ ] Not Run   [✔] Pass   [✖] Fail / Defect ID   [~] Partial (explain)   (P) Planned / Not Implemented

## 1. Environment & Pre-Flight
- [ ] Install TEMS app & dependencies
- [ ] All fixtures (Roles) present (`Role` list matches expected)
- [ ] Scheduler enabled & running
- [ ] No tracebacks in `frappe.log` after restart
- [ ] Workers processing jobs (check `worker.log`)
- [ ] Timezone & currency configured correctly

## 2. Master Data Setup
- [ ] Create sample Employees (Driver, Maintenance Tech, Safety Officer)
- [ ] Create Vehicles (min 2), ensure status fields available
- [ ] Create Spare Parts & initial stock
- [ ] Define Route Planning entries (at least 2 distinct routes)
- [ ] Define Trade Lane & Border Posts (for cross-border test)
- [ ] Create Governance Policy & Compliance Obligation
- [ ] Create Strategic Goal (Planned metrics) (P)

## 3. Fleet Module Tests
### 3.1 Journey Plan Creation
- [ ] Create Journey Plan with required Route & Driver
- [ ] Omit Vehicle (allowed) – system accepts
- [ ] Add Vehicle – system saves
- [ ] Start Time required validation triggers on blank
- [ ] Risk Score editable & persists
- [ ] Weather Snapshot accepts JSON (paste sample) and persists
- [ ] Client Script: Inactive / invalid driver blocks validate (P – logic stub)
- [ ] Server Validation: Expired Driver Qualification blocks save (P)

### 3.2 Journey Plan Integration
- [ ] Link Journey Plan in Trip Allocation
- [ ] Attempt linking Journey Plan with missing Vehicle if Trip Allocation requires Vehicle (expected: validation path) (P)
- [ ] Border Crossing referencing Journey Plan allowed
- [ ] Climate Risk Journey referencing Journey Plan allowed

### 3.3 Maintenance Work Order
- [ ] Create Maintenance Work Order with Vehicle
- [ ] Add Maintenance Part Item referencing Spare Part
- [ ] Submit Work Order – cost rollup hook executes (check logs / profitability field if present)
- [ ] Delete part line, verify recalculation (P)
- [ ] Predictive maintenance daily task generates placeholder output (P – inspect logs after scheduler run)

### 3.4 Fuel Log
- [ ] Create Fuel Log with Vehicle, quantity & cost
- [ ] Report (Fuel Efficiency) available / calculates (P)

## 4. Operations Module Tests
### 4.1 Operation Plan
- [ ] Create Operation Plan referencing Vehicle – before_submit ensures availability (simulate conflict) (P if logic incomplete)
- [ ] Submit Operation Plan – movement start logged (check Movement Log / logs)

### 4.2 Trip Allocation
- [ ] Create Trip Allocation linking Journey Plan & Vehicle & Driver – validation passes
- [ ] Attempt with mismatched Driver vs Journey Plan Driver (should block) (P)

### 4.3 Movement Log
- [ ] Update Movement Log – vehicle status updated (verify in Vehicle form)

### 4.4 Operations Event & SOS Event
- [ ] Create Operations Event – realtime publish (check logs/websocket) (P if socket infra not active)
- [ ] Update Operations Event – republish occurs
- [ ] Create SOS Event – publish & escalation path (P for escalation)

### 4.5 Scheduled Reports
- [ ] Daily operations report task runs (inspect scheduler log) (P content validation)

## 5. Safety & Risk Module Tests
### 5.1 Incident Report
- [ ] Create Incident Report referencing Journey Plan & Vehicle
- [ ] Add Incident Participant (Employee)
- [ ] Submit – handler logs against vehicle (inspect vehicle timeline / logs)

### 5.2 Risk Assessment
- [ ] Create Risk Assessment referencing Vehicle / Journey Plan
- [ ] Submit – `validate_vehicle_risk` executes (confirm no exception)
- [ ] Enter high-risk scenario & expect mitigation requirement (P if logic not built)

### 5.3 Spot Check
- [ ] Create Spot Check – on_update handler executes (log)
- [ ] Submit Spot Check – on_submit handler executes
- [ ] Attach Spot Check Photo – visible in child table

### 5.4 Journey Plan Validation
- [ ] Create Journey Plan with driver lacking qualification (P – once enforcement code added)

## 6. Governance Module Tests
### 6.1 Governance Policy
- [ ] Create & update Governance Policy – `apply_policy_to_vehicle` hook fires (log) (P logic)

### 6.2 Compliance Audit
- [ ] Create Compliance Audit, add Evidence child rows
- [ ] Submit – handler processes (no errors) & summarization fields update (P if summarization pending)

### 6.3 Leadership / Governance Meetings
- [ ] Create Governance Meeting & add participants (P validation of quorum)
- [ ] Add Meeting Action Items & verify linkage

## 7. People & Competency Tests
### 7.1 Driver Qualification
- [ ] Create Driver Qualification for Driver with future expiry
- [ ] Daily reminder task identifies near-expiry (simulate by setting date near threshold) (P until cron observed)
- [ ] Expire qualification & attempt Journey Plan – blocked (P)

### 7.2 Training Record & Competency Matrix
- [ ] Create Training Record linked to Employee
- [ ] Competency Matrix reflects updated training (P auto-rollup)

### 7.3 Succession Planning
- [ ] Create Succession Plan & Candidate links (basic persistence)

## 8. Trade Module Tests
### 8.1 Trade Lane
- [ ] Create Trade Lane with Border Posts
- [ ] Attach required documents (Trade Lane Document) (P file validation)

### 8.2 Border Crossing
- [ ] Create Border Crossing referencing Journey Plan & Vehicle
- [ ] Submit – `log_vehicle_crossing` hook fires (log)

### 8.3 Customs Clearance
- [ ] Create Customs Clearance – HS code assistance (P AI): ensure mandatory docs enforced (P)

## 9. Supply Chain Tests
### 9.1 Procurement Order
- [ ] Submit Procurement Order with Spare Parts – handler links parts to asset (verify relation) (P if linking stub)

### 9.2 Spare Part Usage Traceability
- [ ] Verify Maintenance Part Item referencing Spare Part shows correct stock deduction (P inventory integration)

## 10. Finance Module Tests
### 10.1 Cost & Revenue Ledger
- [ ] Update ledger entry referencing Vehicle – profitability recalculated (verify field/log)

### 10.2 FX Rates Task
- [ ] After scheduler run, FX rates updated (P actual calculation) – inspect task log

### 10.3 Emission Externality Cost (Future)
- (P) Emission cost factoring into TCO

## 11. Climate & ESG Module Tests
### 11.1 Emissions Log
- [ ] Create Emissions Log referencing Vehicle – rollup handler invoked (log)

### 11.2 Aggregation Tasks
- [ ] Daily emissions aggregation run (check scheduler log)
- [ ] Monthly emissions aggregation run (simulate via manual trigger) (P)

### 11.3 Climate Risk Journey
- [ ] Create Climate Risk Journey referencing Journey Plan (persistence)

## 12. Informal Economy Module Tests
- [ ] Create Informal Operator Profile (basic save)
- [ ] Create Operator Route Association linking profile & route
- [ ] Trip Matching simulation (P future algorithm)

## 13. CRM Module Tests
### 13.1 Order
- [ ] Submit Order referencing Vehicle – `link_order_to_vehicle` executes (log)

### 13.2 Customer Feedback
- [ ] Create Customer Feedback referencing Journey Plan / Order (P cross-link enforcement)

## 14. Documents & Compliance Module
### 14.1 Compliance Document
- [ ] Create / update – `validate_vehicle_document` invoked (log) (P enforcement rules)

### 14.2 Document Checklist
- [ ] Create Checklist with required docs & verify status rollup (P)

## 15. Insights & Dashboards
- [ ] Number Cards (Open Work Orders) appear (when fixture restored)
- [ ] Dashboard loads without errors
- [ ] Report Subscription (P scheduling behavior)

## 16. Security & Permissions
- [ ] Journey Plan only editable by Fleet roles (verify with non-privileged user)
- [ ] Safety Officer can read Journey Plan (if required) (adjust matrix if blocked)
- [ ] Read-Only Auditor has read but no write on sensitive docs
- [ ] Finance docs not accessible to Driver
- [ ] Governance Policy restricted to Governance roles

## 17. Negative & Edge Cases
- [ ] Journey Plan with Start Time after End Time – validation (P)
- [ ] Overlapping Journey Plans for same Driver – blocked (P)
- [ ] Maintenance Work Order with no parts – allowed (document decision) or blocked (P)
- [ ] Incident Report without Vehicle – allowed? (Decide & test)
- [ ] Border Crossing without Journey Plan – allowed (should it?) (Clarify policy)
- [ ] Emissions Log with negative values – blocked (P validation)

## 18. Performance & Resilience (Basic)
- [ ] Create 100 Journey Plans via script – no degradation / errors
- [ ] Scheduler handles burst of 50 Operations Events (P load test)
- [ ] Large Weather Snapshot JSON accepted (size threshold test) (P define limit)

## 19. Logs & Observability
- [ ] Key hooks produce structured log entries
- [ ] No unexpected stack traces during end-to-end run
- [ ] SOS Event logs contain correlation identifiers (P enhancement)

## 20. Reporting Validation
- [ ] Border Dwelling report filters by Journey Plan successfully
- [ ] Export of report to XLS works

## 21. Cleanup
- [ ] Cancellation paths (where supported) reverse effects cleanly (P details)
- [ ] Archival / soft delete policies documented (P)

## 22. Sign-off
Record summary:
- Total Tests: ____
- Passed: ____  Failed: ____  Planned (excluded): ____  Deferred Defects: ____

Sign-offs:
- QA Lead: ____________ Date: _______
- Product Owner: ______ Date: _______

---
Notes:
1. (P) indicates feature not yet implemented – track in backlog and exclude from current release pass criteria unless explicitly in sprint scope.
2. Attach evidence (screenshots / log excerpts) to test management system referencing checklist item number.
3. Keep this file versioned; update when new DocTypes or hooks are added.
