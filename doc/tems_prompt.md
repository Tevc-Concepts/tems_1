# The 12 modules prompts --- 
## Task 1 - Leadership and Governance
TASK: Implement Leadership & Governance features in TEMS app (Frappe v15).

FEATURES:
- Vision & Mission CRUD (multi-language).
- Strategic Planning (goals, KPIs, dashboards).
- Policy & Standards management with compliance updates.
- Leadership meeting management (offline capable).
- Spot Checks (GPS + photo).
- Compliance audits with violation reporting.

CONSTRAINTS:
- All DocTypes and scripts under apps/tems.
- Create DocTypes: Strategic Goal, Leadership Meeting, Spot Check.
- Extend ERPNext Goal/Project modules where possible.
- Fixtures: Role "Executive", Workspace "Executive Dashboard".
- hooks.py to register doc_events for Spot Check and Policy.

INTER-RELATIONSHIPS:
- Links to HRMS (competency/training records).
- Links to Safety (incident oversight).
- Links to Finance (budget compliance).

EXPECTED OUTPUT:
- DocType JSONs, Workspace JSON fixture.
- hooks.py entries, Client Script for KPI reminder.
- Unit tests in tems/tests/test_governance.py.

## Task 2 - People & Competency (HRMS)
TASK: Implement People & Competency features in TEMS app (Frappe v15, with HRMS).

FEATURES:
- Recruitment & driver qualification tracking.
- Training programs with offline access.
- Competency matrix with gap analysis.
- Performance reviews & KPI assignment.
- Succession planning with high-potential tracking.

CONSTRAINTS:
- Extend HRMS Employee DocType with TEMS fields (license, medical).
- New DocTypes: Training Record, Competency Matrix, Succession Plan.
- Fixtures: Role "HR Manager", Workspace "People & Competency".
- hooks.py: reminders for expiring licenses/certifications.

INTER-RELATIONSHIPS:
- Links to Fleet (assign drivers to vehicles).
- Links to Safety (driver competence validation).
- Links to Finance (payroll & incentive payouts).

EXPECTED OUTPUT:
- DocType JSONs, fixtures, hooks.py events.
- Workspace JSON.
- Unit tests in tems/tests/test_people.py.

## Task 3 - Fleet & Asset Management
TASK: Implement Fleet & Asset Management features in TEMS app.

FEATURES:
- Asset inventory with photos & offline access.
- GPS/telematics integration with offline cache.
- Maintenance scheduling & predictive maintenance.
- Work Orders with mobile interface.
- Asset lifecycle (Acquisition → Utilization → Disposal).

CONSTRAINTS:
- Extend ERPNext Asset/Vehicle where possible.
- New DocTypes: Maintenance Work Order, Asset Utilization Log.
- Fixtures: Role "Fleet Manager", Workspace "Fleet Manager".
- hooks.py: after_insert for Asset, on_submit for Work Orders.

INTER-RELATIONSHIPS:
- Link Fleet assets to Drivers (HRMS).
- Link to Finance (TCO, costs).
- Link to Safety (Journey Plans, inspections).

EXPECTED OUTPUT:
- DocType JSONs, fixtures.
- Sample Client Script for pre-trip inspection validation.
- Unit tests in tems/tests/test_fleet.py.

## Task 4 - Safety & Risk Management
TASK: Implement Safety & Risk Management features in TEMS app.

FEATURES:
- Journey Planning with route optimization.
- SOS alerts & real-time monitoring.
- Incident reporting with offline sync.
- Defensive driving assessment & training records.
- Risk assessment & mitigation workflows.

CONSTRAINTS:
- New DocTypes: Journey Plan, Incident Report, Risk Assessment.
- Fixtures: Role "Safety Officer", Workspace "Safety & Risk".
- hooks.py: validate Journey Plan with driver certification.

INTER-RELATIONSHIPS:
- Link to HRMS (driver competence).
- Link to Fleet (vehicle assigned).
- Link to Climate (weather data for route risks).
- Link to Governance (policy compliance).

EXPECTED OUTPUT:
- DocType JSONs, Workspace JSON, fixtures.
- hooks.py entries, server method for risk scoring.
- Unit tests in tems/tests/test_safety.py.

## Task 5 - Cross-Border Trade Management
TASK: Implement Cross-Border Trade features in TEMS app.

FEATURES:
- Customs document preparation.
- Border queue monitoring & fee calculation.
- Multi-currency accounting for trade.
- Regional trade agreement compliance (AfCFTA, ECOWAS).

CONSTRAINTS:
- Extend ERPNext Sales Invoice/Customs DocTypes where possible.
- New DocTypes: Border Crossing, Trade Agreement Compliance.
- Fixtures: Role "Border Agent", Workspace "Cross-Border Trade".
- hooks.py: cron to update tariff database.

INTER-RELATIONSHIPS:
- Link to Fleet (journey & vehicles crossing).
- Link to Finance (FX, duties).
- Link to Governance (compliance audits).

EXPECTED OUTPUT:
- DocType JSONs, fixtures.
- hooks.py scheduled task for tariff sync.
- Unit tests in tems/tests/test_trade.py.

## Task 6 - Informal Economy Integration
TASK: Implement Informal Economy Integration features.

FEATURES:
- Onboard informal operators via USSD/mobile KYC.
- Trip/cargo matching engine with dynamic pricing.
- Community logistics management (micro-hubs).
- Informal finance integration (ROSCA, microloans).

CONSTRAINTS:
- New DocTypes: Informal Operator, Trip Match, Savings Group.
- USSD integration for onboarding flows.
- Fixtures: Role "Informal Operator", Workspace "Community Logistics".
- hooks.py: tasks for ROSCA rotations.

INTER-RELATIONSHIPS:
- Link to Finance (loan, savings transactions).
- Link to HRMS (basic KYC).
- Link to Safety (operator compliance).

EXPECTED OUTPUT:
- DocType JSONs, USSD API endpoint, fixtures.
- Unit tests in tems/tests/test_informal.py.

## Task 7 - Climate Resilience & ESG
TASK: Implement Climate Resilience & ESG features.

FEATURES:
- Weather integration into journey planning.
- Flood/heat/drought alerts.
- Carbon footprint tracking & reporting.
- Renewable energy (EV charging, solar) management.

CONSTRAINTS:
- New DocTypes: Climate Alert, Emission Log, Renewable Asset.
- Fixtures: Role "Climate Officer", Workspace "Climate & ESG".
- hooks.py: scheduler for weather API pulls.

INTER-RELATIONSHIPS:
- Link to Fleet (vehicle emissions).
- Link to Safety (climate risks on journeys).
- Link to Governance (climate policy compliance).
- Link to Finance (carbon credits).

EXPECTED OUTPUT:
- DocType JSONs, fixtures, hooks.py events.
- Unit tests in tems/tests/test_climate.py.

## Task 8 - Finance & Accounting
TASK: Implement Finance & Accounting extensions.

FEATURES:
- Budgeting & scenario planning.
- Cost tracking for maintenance, journeys, payroll.
- Multi-currency billing & invoicing.
- Financial reporting (local + international standards).

CONSTRAINTS:
- Extend ERPNext Accounts DocTypes.
- New DocTypes: Journey Costing, FX Risk Log.
- Fixtures: Role "Finance Manager", Workspace "Finance".
- hooks.py: cron to fetch FX rates.

INTER-RELATIONSHIPS:
- Link to Fleet (TCO, maintenance costs).
- Link to HRMS (payroll).
- Link to Cross-Border (FX, tariffs).
- Link to Informal (loans, savings).

EXPECTED OUTPUT:
- DocType JSONs, fixtures.
- hooks.py scheduled job for FX updates.
- Unit tests in tems/tests/test_finance.py.

## Task 9 - CRM & Customer Operations
TASK: Implement CRM & Customer features.

FEATURES:
- Customer database with segmentation.
- Order & SLA tracking.
- Feedback & complaint resolution.
- Sentiment analysis of surveys.

CONSTRAINTS:
- Extend ERPNext Customer, Sales Order.
- New DocTypes: SLA Log, Feedback Ticket.
- Fixtures: Role "Customer Manager", Workspace "CRM".
- hooks.py: auto-escalate overdue SLAs.

INTER-RELATIONSHIPS:
- Link to Fleet (journeys fulfilling orders).
- Link to Finance (billing).
- Link to Governance (service quality reporting).

EXPECTED OUTPUT:
- DocType JSONs, fixtures.
- hooks.py entries.
- Unit tests in tems/tests/test_crm.py.

## Task 10 - Supply Chain & Procurement
TASK: Implement Supply Chain & Procurement features.

FEATURES:
- Supplier management with performance metrics.
- Procurement & approval workflows.
- Inventory with low-stock alerts.
- Logistics coordination (real-time tracking).

CONSTRAINTS:
- Extend ERPNext Supplier, Purchase Order, Item.
- New DocTypes: Supplier Rating, Logistics Task.
- Fixtures: Role "Procurement Officer", Workspace "Supply Chain".
- hooks.py: task for stock alerts.

INTER-RELATIONSHIPS:
- Link to Fleet (spare parts).
- Link to Finance (purchase orders).
- Link to Governance (supplier compliance).

EXPECTED OUTPUT:
- DocType JSONs, fixtures.
- Unit tests in tems/tests/test_supplychain.py.

## Task 11 - Document & Drive
TASK: Extend Document Management with Drive integration.

FEATURES:
- Centralized repository with offline access.
- Blockchain-backed audit trail.
- Compliance document retention.
- E-signature integration.

CONSTRAINTS:
- Extend ERPNext File/Document DocTypes.
- New DocTypes: Compliance Document, Signature Log.
- Fixtures: Role "Document Controller", Workspace "Drive".
- hooks.py: file validation events.

INTER-RELATIONSHIPS:
- Link to HRMS (licenses).
- Link to Safety (incident docs).
- Link to Finance (invoices).
- Link to Governance (policy docs).

EXPECTED OUTPUT:
- DocType JSONs, fixtures.
- hooks.py file hooks.
- Unit tests in tems/tests/test_docs.py.

## Task 12 - Analytics & Insights
TASK: Implement Analytics & Insights for TEMS.

FEATURES:
- KPI dashboards for all roles.
- Predictive analytics (maintenance, demand).
- Anomaly detection across finance & safety.
- Natural language report generation.

CONSTRAINTS:
- Use Frappe Insights dashboards.
- Export dashboards as fixtures in TEMS.
- New DocTypes: KPI Config, Report Subscription.
- Fixtures: Role "Analyst", Workspace "Insights".
- hooks.py: scheduler for auto-report delivery.

INTER-RELATIONSHIPS:
- Pull data from HRMS, Fleet, Safety, Finance.
- Governance (KPI reporting).
- CRM (customer feedback trends).

EXPECTED OUTPUT:
- Insights dashboards exported as JSON.
- DocType JSONs, fixtures.
- hooks.py jobs for auto-reports.
- Unit tests in tems/tests/test_insights.py.
