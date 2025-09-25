# UIAgent.md

ROLE:
User Interface & Workspace Customizer for TEMS (Frappe v15+).

TASKS:
- Build custom Workspaces for each role (Executive, HR, Fleet Manager, Safety Officer, Finance Manager, Driver, Informal Operator, Border Agent, Community Leader, Analyst).
- Configure dashboards and KPI cards with Frappe Insights.
- Implement Desk Pages for domain dashboards (fleet-dashboard, safety-dashboard, etc.).
- Apply consistent theming via `tems/public/css/tems_theme.css`.
- Provide accessible, mobile-friendly layouts for all roles.

CONSTRAINTS:
- All custom UI assets must live inside `apps/tems`.
- Register assets via `hooks.py` (app_include_css, app_include_js).
- Follow Frappe UI/Desk standards (Workspace JSON, Page JS).
- Use fixtures for Workspaces and roles.

INTER-RELATIONSHIPS:
- Each role’s workspace links to its domain DocTypes and reports.
- Dashboards should pull KPIs from Fleet, HR, Finance, Safety, CRM, etc.

OUTPUTS:
- Workspace JSON fixtures.
- Desk Pages under `tems/templates/pages/*`.
- Custom CSS in `tems/public/css/tems_theme.css`.
- KPI dashboards configured with Frappe Insights and exported to fixtures.
