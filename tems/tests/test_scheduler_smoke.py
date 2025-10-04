from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase


class TestSchedulerSmoke(FrappeTestCase):
    def test_finance_profitability_task_runs(self):
        from tems.tems_finance.tasks import update_vehicle_profitability
        update_vehicle_profitability()  # Should not raise

    def test_people_reminder_task_runs(self):
        from tems.tems_people.tasks import remind_expiring_driver_docs
        remind_expiring_driver_docs(0)  # edge case: cutoff=today; should not raise

    def test_fx_rates_task_runs(self):
        from tems.tems_finance.tasks import update_fx_rates
        update_fx_rates()  # Should create placeholder FX Risk Log (idempotent)
