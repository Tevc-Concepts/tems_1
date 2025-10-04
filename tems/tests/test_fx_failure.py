from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFXFailure(FrappeTestCase):
    def test_fx_rate_update_failure_logging(self):
        # Monkeypatch frappe.get_doc to raise for FX insertion and ensure function swallows/continues logging
        from tems.tems_finance import tasks as finance_tasks

        original_get_doc = frappe.get_doc
        calls = {"attempted": 0}

        def failing_get_doc(*args, **kwargs):  # noqa: D401
            if isinstance(args[0], dict) and args[0].get("doctype") == "FX Risk Log":
                calls["attempted"] += 1
                raise Exception("Simulated FX insert failure")
            return original_get_doc(*args, **kwargs)

        frappe.get_doc = failing_get_doc  # type: ignore
        try:
            finance_tasks.update_fx_rates()  # Should not raise after patch resilience
        finally:
            frappe.get_doc = original_get_doc  # type: ignore
        self.assertGreaterEqual(calls["attempted"], 1)
