__version__ = "0.0.1"

# Backward compatibility shim for legacy tests in dependent apps that still
# import IntegrationTestCase from frappe.tests. Some versions of HRMS (and
# possibly other apps) reference frappe.tests.IntegrationTestCase which was
# removed in newer Frappe. Provide an alias to FrappeTestCase early so test
# discovery (bench run-tests) succeeds.
try:  # pragma: no cover - defensive import handling
	import frappe.tests  # type: ignore
	from frappe.tests.utils import FrappeTestCase, change_settings  # type: ignore
	# Provide ERPNextTestSuite & HRMSTestSuite backward compat if missing
	import erpnext.tests.utils as erpnext_tests_utils  # type: ignore

	if not hasattr(frappe.tests, "IntegrationTestCase"):
		class IntegrationTestCase(FrappeTestCase):  # type: ignore
			pass

		frappe.tests.IntegrationTestCase = IntegrationTestCase  # type: ignore[attr-defined]
	if not hasattr(frappe.tests, "change_settings"):
		frappe.tests.change_settings = change_settings  # type: ignore[attr-defined]
	# Some downstream tests import ERPNextTestSuite from erpnext.tests.utils; if it's absent,
	# create a harmless alias to FrappeTestCase so imports succeed.
	if not hasattr(erpnext_tests_utils, "ERPNextTestSuite"):
		class ERPNextTestSuite(FrappeTestCase):  # type: ignore
			pass
		erpnext_tests_utils.ERPNextTestSuite = ERPNextTestSuite  # type: ignore[attr-defined]
except Exception:  # pragma: no cover
	# Non-fatal if this fails; only impacts test harness expecting old class.
	pass

# Re-export demo seeding utilities for simplified bench execute import path
try:  # pragma: no cover
	from .tems_demo.orchestrator import run_all as demo_run_all, run_minimal as demo_run_minimal  # noqa: F401
except Exception:
	# ignore if not yet generated
	pass

