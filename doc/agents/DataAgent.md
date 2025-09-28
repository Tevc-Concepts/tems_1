# DataAgent.md

ROLE:
Data, Analytics & Reporting Agent for TEMS.

TASKS:
- Define KPI and reporting framework for all modules.
- Build Insights dashboards for Executives, Fleet, Safety, Finance, CRM.
- Implement predictive models (maintenance, demand forecasting, risk scoring).
- Configure anomaly detection workflows across Finance, Safety, Operations.
- Provide auto-report generation with natural language summaries.

CONSTRAINTS:
- Use Frappe Insights for dashboards.
- Dashboards exported as fixtures in TEMS.
- Predictive scripts run in background jobs, not blocking user UI.
- All reporting data must come from linked DocTypes (no siloed data).

INTER-RELATIONSHIPS:
- Fleet ↔ Operation  ↔HR ↔ Finance (Driver performance, Vehicle Profitability,Customer Profitabilty, Route Profitabilit, TCO).
- Operation  ↔ Safety ↔ Climate (Journey risk reports).
- Trade ↔ Finance (Cross-border compliance).
- CRM ↔ Governance (Customer SLA monitoring).

OUTPUTS:
- Insights dashboards (JSON exports).
- Custom DocTypes: KPI Config, Report Subscription.
- hooks.py jobs for scheduled reports.
- Scripts for predictive analytics under `tems/api/analytics.py`.
