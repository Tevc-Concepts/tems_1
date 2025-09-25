# SafetyAgent.md

ROLE:
Build Safety & Risk Management module inside TEMS app.

TASKS:
- Implement Journey Planning with route optimization.
- Enable SOS alerts & real-time journey monitoring.
- Create Incident Reporting with offline sync.
- Add Defensive Driving assessments & coaching logs.
- Build Risk Assessment & Mitigation workflows.

CONSTRAINTS:
- New DocTypes: Journey Plan, Incident Report, Risk Assessment.
- Fixtures: Role "Safety Officer", Workspace "Safety & Risk".
- hooks.py: validate driver competence before Journey approval.

INTER-RELATIONSHIPS:
- Fleet (Vehicles assigned).
- HRMS (Driver certifications).
- Climate (Weather alerts).
- Governance (Policy compliance).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py , fixtures.
- hooks.py events.
- Unit tests (`tems/tests/test_safety.py`).
