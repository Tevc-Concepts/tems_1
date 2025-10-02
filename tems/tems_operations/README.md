TEMS Operations Module (Execution Core)

- DocTypes: Dispatch Schedule, Shift Plan, Duty Assignment, Control Exception, Operations Event, SOS Event, Operation Plan, Movement Log, Trip Allocation
- Handlers: hooks in `handlers.py` to validate vehicle availability, driver-vehicle validation, movement state rollup, realtime events
- API: `api.compute_otp(from_date, to_date, route?)`
- Workspace: `workspace/operations_control/operations_control.json`
- Dashboard: `dashboard/operations_dashboard.json`

Vehicle-first Principles
- All planning, allocations, movement logs, and cost/revenue rollups key off Vehicle.
- Assets contribute costs to Vehicle via Finance ledger.
