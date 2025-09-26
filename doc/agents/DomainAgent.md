# DomainAgent.md

ROLE:
Domain Module Builder for TEMS app (Frappe v15+).

TASKS:
- For each domain (Governance, Operations,People, Fleet, Safety, Trade, Informal, Climate, Finance, CRM, Supply Chain, Documents, Insights) - domain specific prompt in /doc/agentic/domain/{domain}Agent.md:
  - Implement required DocTypes, fields, and relationships.
  - Extend ERPNext/HRMS core DocTypes with Custom Fields where appropriate.
  - Create server methods, Client Scripts, and API endpoints.
  - Add unit tests and sample data patches.
- Maintain modular boundaries between domains while allowing links for triangulation.

CONSTRAINTS:
- Place all code under `apps/tems` application folder.
- Fixtures must define Roles, Workspaces, Reports, and Custom Fields.
- hooks.py must register doc_events for each new DocType.
- No modifications to ERPNext/HRMS/DRIVE/FRAPPE core files.

INTER-RELATIONSHIPS:
- Always define Link fields to connect related domains (e.g., Journey Plan → Driver, Vehicle, Asset).
- Ensure consistent naming and reusable components across modules.

OUTPUTS:
- DocType JSON files under `tems_{domain}/doctype/*`. ( For all doctypes to be created ensure you generate the all 4 files types templates (.js, .json, .py (controller), .py(test) & __init__.py).)
- Workspace JSON fixtures under `tems_{domain}/workspace/*`.
- Unit test files under `tems/tests/test_<module>.py`.
- Example Client Scripts per module.
