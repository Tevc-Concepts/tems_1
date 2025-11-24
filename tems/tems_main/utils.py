import frappe
import importlib


@frappe.whitelist()
def doc_exists(doctype: str, name: str | None = None, filters: dict | None = None):
    if name:
        return bool(frappe.db.exists(doctype, name))
    return bool(frappe.db.exists(doctype, filters or {}))


@frappe.whitelist()
def smoke_check_reports():
    """
    Import and call execute() for all Script Reports we scaffolded across domains.
    Returns a dict with counts and failures for quick smoke validation.
    """
    report_modules = [
        # Trade
        "tems.tems_trade.report.border_dwell_time.border_dwell_time",
        # Informal
        "tems.tems_informal.report.active_informal_operators.active_informal_operators",
        # Climate
        "tems.tems_climate.report.emissions_by_asset_month.emissions_by_asset_month",
        # Finance
        "tems.tems_finance.report.total_cost_by_type.total_cost_by_type",
        # CRM
        "tems.tems_crm.report.fsr_open_by_priority.fsr_open_by_priority",
        # Supply Chain
        "tems.tems_supply_chain.report.spare_parts_min_stock_breach.spare_parts_min_stock_breach",
        # Documents
        "tems.tems_documents.report.checklist_count_by_context.checklist_count_by_context",
        # Governance
        "tems.tems_governance.report.obligation_status_aging.obligation_status_aging",
        # People
        "tems.tems_people.report.training_compliance_by_dept.training_compliance_by_dept",
        # Fleet
        "tems.tems_fleet.report.fuel_efficiency_by_vehicle.fuel_efficiency_by_asset",
    ]

    successes = []
    failures = []

    for mod in report_modules:
        try:
            m = importlib.import_module(mod)
            execute = getattr(m, "execute")
            # run with empty filters to surface basic import/runtime errors
            cols, data = execute({}) if execute.__code__.co_argcount else execute()
            # store a tiny summary to avoid dumping heavy rows
            successes.append({
                "module": mod,
                "columns": len(cols) if isinstance(cols, (list, tuple)) else 0,
                "rows": len(data) if isinstance(data, (list, tuple)) else 0,
            })
        except Exception as exc:
            failures.append({"module": mod, "error": repr(exc)})

    return {
        "ok": len(failures) == 0,
        "successes": successes,
        "failures": failures,
        "counts": {"success": len(successes), "failure": len(failures)},
    }
