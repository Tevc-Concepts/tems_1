# ClimateAgent.md

ROLE:
Build Climate Resilience & ESG module inside TEMS app.

TASKS:
- Integrate Weather APIs into Journey Plans.
- Build Flood/Heat/Drought alert system.
- Track Emissions per vehicle/journey.
- Manage Renewable Assets (EV charging, solar).

CONSTRAINTS:
- New DocTypes: Climate Alert, Emission Log, Renewable Asset.
- Fixtures: Role "Climate Officer", Workspace "Climate & ESG".
- hooks.py: weather data scheduler.

INTER-RELATIONSHIPS:
- Fleet (Vehicle emissions).
- Safety (Journey climate risks).
- Governance (Climate policy compliance).
- Finance (Carbon credits).

OUTPUTS:
- DocType JSONs, Workspace JSON.
- hooks.py jobs.
- Unit tests (`tems/tests/test_climate.py`).
