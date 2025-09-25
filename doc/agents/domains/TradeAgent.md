# TradeAgent.md

ROLE:
Build Cross-Border Trade Management module inside TEMS app.

TASKS:
- Automate Customs document preparation.
- Track Border Queues & Fees.
- Handle Multi-Currency Accounting.
- Ensure Regional Trade Agreement compliance.

CONSTRAINTS:
- Extend ERPNext Invoices/Customs DocTypes where possible.
- New DocTypes: Border Crossing, Trade Compliance Log, FX Transaction.
- Fixtures: Role "Border Agent", Workspace "Cross-Border Trade".
- hooks.py: cron jobs for tariff updates.

INTER-RELATIONSHIPS:
- Fleet (Cross-border journeys).
- Finance (FX, Duties).
- Governance (Regulatory compliance).

OUTPUTS:
- DocType JSONs, Workspace JSON.
- hooks.py scheduled jobs.
- Unit tests (`tems/tests/test_trade.py`).
