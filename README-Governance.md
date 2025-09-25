Governance Domain (Domain 1)
---------------------------------
Implements Governance Policy, Compliance Obligation, Approval Matrix, Governance Meeting + Reports & Workspace.

Module restructure: this domain now lives under `tems/tems/tems/tems_governance/`.
- APIs: `tems.tems.tems_governance.api.*` (wrapper kept at `tems/tems/api/governance.py`)
- DocTypes: `tems/tems/tems/tems_governance/doctype/*`
- Reports: `tems/tems/tems/tems_governance/report/*`
- Workspace: fixture remains under `tems/tems/config/desk_workspace/`

Bench cycle after pulling changes:

1. bench --site <site> migrate
2. bench build
3. bench clear-cache
4. bench restart

Seed data patch runs automatically post model sync.
