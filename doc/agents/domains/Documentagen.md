# DocumentAgent.md

ROLE:
Build Document Management module integrated with Frappe Drive.

TASKS:
- Centralize Document Repository.
- Implement Blockchain-backed Audit Trail.
- Automate Retention for Compliance Documents.
- Support Legal E-signature flows.

CONSTRAINTS:
- Extend ERPNext File & Document.
- New DocTypes: Compliance Document, Signature Log.
- Fixtures: Role "Document Controller", Workspace "Drive".
- hooks.py: file validation & retention rules.

INTER-RELATIONSHIPS:
- HRMS (Licenses).
- Safety (Incident docs).
- Finance (Invoices).
- Governance (Policies).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py 
- hooks.py file handlers.
- Unit tests (`tems_{domain}/tests/test_documents.py`).
