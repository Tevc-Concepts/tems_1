---
mode: agent
---
PROJECT_CONTEXT:
- Frappe/ERPNext v15+ site.
- Main custom app: TEMS (already in codebase). All code, assets, overrides MUST live under apps/tems.
- Integrations: ERPNext modules (HRMS, Drive), and Frappe Insights. Keep custom doctypes, pages, workspaces inside TEMS.
- Target: modular features (Leadership, People, Fleet, Safety, Trade, Informal Economy, Climate + Finance/CRM/SCM).
- UI: Use Frappe UI components and Desk customization (Workspaces, Dashboards, Pages). Use TEMS theme CSS (no direct edits to frappe/erpnext core files).
- Deploy/testing: ensure bench migrate, bench build, bench clear-cache after changes. Verify cron/jobs on v15 (test scheduled jobs).
