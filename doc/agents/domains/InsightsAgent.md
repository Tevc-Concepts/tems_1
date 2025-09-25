# InsightsAgent.md

ROLE:
Build Analytics & Insights module inside TEMS app.

TASKS:
- Create KPI Dashboards for all roles.
- Add Predictive Analytics (maintenance, demand).
- Build Anomaly Detection workflows.
- Auto-generate Reports with summaries.

CONSTRAINTS:
- Use Frappe Insights dashboards (export as fixtures).
- New DocTypes: KPI Config, Report Subscription.
- Fixtures: Role "Analyst", Workspace "Insights".
- hooks.py: scheduled auto-report delivery.

INTER-RELATIONSHIPS:
- Pulls from HRMS, Fleet, Finance, Safety, CRM.
- Governance (KPI Reporting).
- Trade (Compliance trends).

OUTPUTS:
- Insights dashboards JSON fixtures.
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py 
- hooks.py jobs.
- Unit tests (`tems/tests/test_insights.py`).
