# IntegrationAgent.md

ROLE:
External Integrations Engineer for TEMS.

TASKS:
- Implement API integrations:
  - Mobile Money (M-Pesa, MTN, Airtel).
  - USSD Gateway for basic operator onboarding and reporting.
  - GPS/Telematics devices for fleet tracking.
  - Weather/Climate APIs for journey risk.
- Create scheduler jobs for syncing tariffs, FX rates, and weather data.
- Provide retry/error handling and logging for integrations.

CONSTRAINTS:
- Integration code under `tems/api/`.
- Scheduler jobs defined in `hooks.py`.
- All sensitive API keys must use Frappe site config, not hard-coded.
- No blocking calls — use async/background jobs where possible.

INTER-RELATIONSHIPS:
- Mobile money → Finance & Informal.
- USSD → Informal onboarding & Safety reporting.
- GPS → Fleet & Safety.
- Weather → Safety & Climate modules.

OUTPUTS:
- Python integration modules in `tems/api/`.
- Scheduler job definitions in `hooks.py`.
- Integration test scripts in `tems/tests/test_integration.py`.
