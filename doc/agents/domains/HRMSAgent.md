# HRMSAgent.md

ROLE:
Build People & Competency module integrated with HRMS.

TASKS:
- Track Recruitment of staff & Driver with their Qualifications.
- Build Training Management with offline content.
- Maintain Competency Matrix with gap analysis.
- Enable Performance Reviews & KPI Assignment.
- Implement Succession Planning & Talent Development.

CONSTRAINTS:
- Extend HRMS Employee via Custom Fields.
- New DocTypes: Driver Qualification, Training Record, Competency Matrix, Succession Plan.
- Fixtures: Role "HR Manager", Workspace "People & Competency".
- hooks.py: reminders for license/medical renewals.
- Drivers are assigned to Vehicles, not Assets.
- Training/Competency logs tie to Driver–Vehicle combinations.
- Example: “Driver X certified to operate Vehicle Y type.”

INTER-RELATIONSHIPS:
- Fleet (Assign drivers to Vehicle).
- Safety (Competency validation).
- Finance (Payroll, incentives).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py 
- hooks.py reminders.
- Unit tests (`tems/tests/test_hrms.py`).
