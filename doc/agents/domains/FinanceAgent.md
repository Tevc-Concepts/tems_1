# FinanceAgent.md

ROLE:
Build Finance & Accounting module extensions inside TEMS app.

TASKS:
- Enable Budgeting & Scenario Planning.
- Track Costs across Fleet, Safety, HR.
- Build Multi-Currency Billing & Invoicing.
- Generate Regulatory-Compliant Reports.

CONSTRAINTS:
- Extend ERPNext Finance DocTypes.
- New DocTypes: Journey Costing, FX Risk Log.
- Fixtures: Role "Finance Manager", Workspace "Finance".
- hooks.py: cron job for FX rate updates.

INTER-RELATIONSHIPS:
- Fleet (TCO, maintenance).
- HRMS (Payroll).
- Trade (FX, tariffs).
- Informal (loans, savings).

OUTPUTS:
- DocType JSONs, Workspace JSON.
- hooks.py jobs.
- Unit tests (`tems/tests/test_finance.py`).
