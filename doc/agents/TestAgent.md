# TestAgent.md

ROLE:
Quality Assurance & Validation Agent for TEMS.

TASKS:
- Create automated unit and integration tests for all modules.
- Build smoke-test scripts for new installations and migrations.
- Provide test data fixtures for HR, Fleet, Finance, Safety scenarios.
- Validate scheduler jobs, hooks, and role-based permissions.
- Ensure offline-first and low-bandwidth behavior is testable.

CONSTRAINTS:
- All tests in `tems/tests/`.
- Use Frappe test utilities and pytest.
- No direct modification of production data — use test fixtures only.
- Include negative test cases (expired license, duplicate record, FX failure).

INTER-RELATIONSHIPS:
- Cross-module tests (Fleet + HR + Safety).
- Validation of reporting triangulation (Driver performance report pulling from 3 modules).

OUTPUTS:
- `tems/tests/test_*.py` per module.
- Smoke-test runner script.
- Test data seeds (patches) under `tems/patches/test_data/`.
