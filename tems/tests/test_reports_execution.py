import importlib
import frappe
from frappe.tests.utils import FrappeTestCase


CURATED_REPORTS = [
    "Vehicle Profitability Summary",
    "Asset Lifecycle Cost Breakdown",
    "Expiring Driver Qualifications",
    "Low Stock Breach",
]


def _script_module_path(report_name: str, module_hint: str | None):
    base_mod = (module_hint or "tems").lower().replace(" ", "_")
    return f"{base_mod}.report.{frappe.scrub(report_name)}.{frappe.scrub(report_name)}"


def _execute_report(name: str):
    rpt_doc = frappe.get_doc("Report", name)
    report_type = getattr(rpt_doc, "report_type", "")
    module_hint = getattr(rpt_doc, "module", None)
    if report_type == "Script Report":
        mod_path = _script_module_path(name, module_hint)
        try:
            mod = importlib.import_module(mod_path)
        except ModuleNotFoundError:
            for prefix in [
                "tems.tems_finance.report",
                "tems.tems_people.report",
                "tems.tems_supply_chain.report",
                "tems.tems_fleet.report",
            ]:
                alt = f"{prefix}.{frappe.scrub(name)}.{frappe.scrub(name)}"
                try:
                    mod = importlib.import_module(alt)
                    break
                except ModuleNotFoundError:  # noqa: PERF203
                    continue
            else:
                raise AssertionError(f"Could not import execute() for report {name}")
        execute_fn = getattr(mod, "execute", None)
        assert callable(execute_fn), f"execute() missing for report {name}"
        columns, data = execute_fn()  # type: ignore[misc]
        assert isinstance(columns, (list, tuple)), f"Columns not list/tuple for {name}"
        assert isinstance(data, (list, tuple)), f"Data not list/tuple for {name}"
    else:
        result = frappe.get_all("Report", filters={"name": name})
        assert result, f"Report {name} not found"


class TestCuratedReports(FrappeTestCase):
    def test_curated_reports_execute(self):
        for r in CURATED_REPORTS:
            try:
                _execute_report(r)
            except Exception as e:  # noqa: BLE001
                frappe.log_error(title=f"Report Execution Failure: {r}", message=frappe.get_traceback())
                raise AssertionError(f"Report {r} failed to execute: {e}") from e
