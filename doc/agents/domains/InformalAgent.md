# InformalAgent.md

ROLE:
Build Informal Economy Integration module inside TEMS app.

TASKS:
- Register Informal Operators via USSD/Mobile onboarding.
- Implement Trip Matching with dynamic pricing.
- Build Community Logistics & Micro-hub management.
- Integrate Informal Finance (ROSCA, Microloans, Savings Groups).

CONSTRAINTS:
- New DocTypes: Informal Operator, Trip Match, Savings Group, Loan.
- Fixtures: Role "Informal Operator", Workspace "Community Logistics".
- USSD APIs for onboarding.
- hooks.py: ROSCA rotation scheduler.

INTER-RELATIONSHIPS:
- Finance (Savings/Loans).
- HRMS (KYC).
- Safety (Operator compliance).

OUTPUTS:
- DocType JSONs, Workspace JSON, .Js (template), .py (template) and it __init__.py  USSD API scripts.
- hooks.py scheduled jobs.
- Unit tests (`tems/tests/test_informal.py`).
