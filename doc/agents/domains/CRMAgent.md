# CRMAgent.md

ROLE:
Build CRM & Customer Operations module inside TEMS app.

TASKS:
- Manage Customer Database with segmentation.
- Process Orders & SLA tracking.
- Collect Feedback & Complaints.
- Analyze Customer Sentiment.

CONSTRAINTS:
- Extend ERPNext Customer & Sales Order.
- New DocTypes: SLA Log, Feedback Ticket.
- Fixtures: Role "Customer Manager", Workspace "CRM".
- hooks.py: auto-escalation for overdue SLAs.

INTER-RELATIONSHIPS:
- Fleet (Order fulfillment journeys).
- Finance (Billing).
- Governance (Service quality reporting).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py 
- hooks.py entries.
- Unit tests (`tems_{domain}/tests/test_crm.py`).
