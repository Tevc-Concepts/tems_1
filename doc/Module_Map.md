# TEMS Module Map

This map outlines dependencies and integration flows across TEMS modules on Frappe v15+. Each module should live under the `tems` app, extend ERPNext/HRMS where needed, and expose fixtures for roles/workspaces.

## Domains and Key Dependencies

- Governance
  - Depends on: Documents, Insights
  - Provides: Policy, Compliance Audit, SLA standards

- People (HRMS)
  - Depends on: HRMS Employee, Training
  - Provides: Driver Qualification, Training Records, Performance Reviews
  - Used by: Operations (assignment), Safety (eligibility), Finance (payroll links)

- Fleet
  - Depends on: ERPNext Asset/Vehicle, Maintenance
  - Provides: Vehicle master, Maintenance Work Orders, Emission Logs
  - Used by: Operations (allocation), Finance (asset costs), Climate (emissions)

- Safety
  - Depends on: People (driver fitness), Operations (journeys)
  - Provides: Journey Plan, Incident Report, Risk Assessment, Custom Checkpoints
  - Used by: Governance (policy adherence), Insights (risk KPIs)

- Trade
  - Depends on: Finance (FX), Documents (border docs)
  - Provides: Border Crossing, FX Transactions
  - Used by: Operations (cross-border journeys), Insights (trade flows)

- Informal Economy
  - Depends on: People (KYC), Finance (wallets/loans)
  - Provides: Trip Match, Savings Group, Micro-Loans
  - Used by: Operations (fill-rate), Insights (inclusion metrics)

- Climate
  - Depends on: Fleet (vehicle types), Operations (routes)
  - Provides: Climate Alerts, Renewable Assets, Emission Accounting
  - Used by: Governance (ESG), Insights (carbon KPIs)

- Finance
  - Depends on: ERPNext Accounting, FX feeds
  - Provides: Journey Costing, Cost/Revenue Ledger, TCO, FX Risk Log
  - Used by: Operations (profitability), Trade, Insights

- CRM
  - Depends on: ERPNext CRM
  - Provides: Customer, Orders, SLA Logs
  - Used by: Operations (fulfillment), Insights (service KPIs)

- Supply Chain
  - Depends on: ERPNext Stock/Buying
  - Provides: Suppliers, Procurement Orders, Inventory Items
  - Used by: Fleet (spares), Operations (consumption), Finance (costing)

- Documents
  - Depends on: Drive
  - Provides: Compliance Documents, Policy Documents, Attachments
  - Used by: Governance, Safety, Trade, Operations

- Insights
  - Depends on: All data-producing modules
  - Provides: KPI Config, Dashboards, Report Subscriptions
  - Used by: Executives and managers across roles

## Data Flow Highlights

- Journey Plan → Vehicle Trip → Cost/Revenue Ledger → Profitability KPIs
- Driver Qualification → Journey validation (block expired/invalid)
- Incident Reports → Risk Score adjustments → Governance alerts
- Maintenance Work Orders → Vehicle availability → Route Planning
- Border Crossing + FX → Trade Costs → Finance ledgers
- Emission Logs + Route → Climate Impact KPIs

## Implementation Pointers

- Use Link fields to ERPNext/HRMS doctypes (Employee, Asset/Vehicle, Item).
- Keep customizations inside `apps/tems`; use fixtures for Roles, Workspaces, Custom Fields.
- Register assets and hooks in `tems/hooks.py`.
- Add scheduler jobs for integrations: FX rates, Weather, Tariff databases.
