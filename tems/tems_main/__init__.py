"""TEMS app package init.

Adds backward compatibility shims required for some dependant apps' test
utilities (e.g. HRMS) that still import IntegrationTestCase which was
removed / renamed in newer Frappe versions. We create a lightweight
alias to FrappeTestCase at import time so running isolated TEMS tests
doesn't fail before our own tests execute.
""" """

from __future__ import annotations

try:
	# Frappe v15+ provides FrappeTestCase in frappe.tests.utils
	from frappe.tests.utils import FrappeTestCase  # type: ignore
	import frappe.tests  # type: ignore

	if not hasattr(frappe.tests, "IntegrationTestCase"):
		class IntegrationTestCase(FrappeTestCase):  # pragma: no cover - simple alias
			pass

		frappe.tests.IntegrationTestCase = IntegrationTestCase  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - defensive; we don't want import errors to break app init
	# Silently ignore; test environment may differ, and absence is non-fatal for production use
	pass
 """
