# TEMS Demo Data Seeding

Modular demo dataset generator following `doc/agents/DemoDataAgent.md`.

## Entry Points

Minimal (fast, CI smoke):
```
bench --site tems.local execute "tems.tems.tems_demo.orchestrator.run_minimal"
```

Full rich dataset (20+ per domain):
```
bench --site tems.local execute "tems.tems.tems_demo.orchestrator.run_all"
```

Generates `demo_data_summary.md` under the site directory with record counts.

## Structure

Each `seed_*.py` provides a `seed_<domain>` function accepting a shared `context` dict for cross-linking (vehicles, assets, employees ...).

Functions are defensive: they check if a DocType exists and required columns exist before inserting, allowing partial installs without failures.

## Idempotency Notes

Scripts avoid duplicate creation by checking key names (e.g., Item, Customer) before insert. Re-running may append additional transactional logs (movement, ledgers) but will not duplicate master data heavily.

## Post-run

After full run you may rebuild dashboards / number cards as needed or export fixtures:
```
bench --site tems.local export-fixtures
```

## Troubleshooting

1. Missing Warehouses: If Stock Entry creation fails (no warehouse), create a Warehouse named `Stores - DML` or adjust code.
2. Permissions: Commands run as Administrator context via bench execute; if restricted, temporarily elevate user.
3. Rollbacks: Any exception inside loops performs a rollback for that doc then continues to avoid aborting the whole run.
