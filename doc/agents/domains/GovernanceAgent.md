# GovernanceAgent.md

ROLE:
Build Leadership & Governance module inside TEMS app.

TASKS:
- Manage Vision, Mission, and Strategy (multi-language).
- Track KPIs with dashboards.
- Manage Policies & Standards.
- Build Leadership Meeting & Spot Check workflows.
- Support Compliance Audits & Violation Reporting.

CONSTRAINTS:
- DocTypes: Strategic Goal, Leadership Meeting, Spot Check, Policy.
- Fixtures: Role "Executive", Workspace "Executive Dashboard".
- hooks.py: event logs for Spot Checks and Compliance Audits.

INTER-RELATIONSHIPS:
- HRMS (Competency, Training).
- Safety (Incident oversight).
- Finance (Budget compliance).

OUTPUTS:
- DocType JSONs, Workspace JSON.
- hooks.py entries.
- Unit tests (`tems/tests/test_governance.py`).
