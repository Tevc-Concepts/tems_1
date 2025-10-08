"""TEMS Demo Data seeding package.

Split domain seeding logic into focused modules so each domain can be
individually invoked (useful for iterative development) while a single
`run_all()` orchestrates full business flow required by DemoDataAgent.

Each domain seeder exposes a `seed(context)` function that receives a
mutable dict collecting created record name lists for cross-linking.
"""

from .orchestrator import run_all, run_minimal

__all__ = ["run_all", "run_minimal"]
"""TEMS Demo Data Package

Provides utilities to seed rich, inter‑linked demo data for Transport
Excellence Management System.

Entry point for bench execute:

    bench --site tems.local execute tems.tems_demo.seed_demo_data.run

"""

__all__: list[str] = []
# Package for TEMS demo data generation
