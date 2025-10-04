from __future__ import annotations
import frappe


def _safe_float(val):
    try:
        if val in (None, "", []):
            return 0.0
        return float(val)  # type: ignore[arg-type]
    except Exception:
        return 0.0


def execute(filters=None):
    columns = [
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 140},
        {"label": "Revenues", "fieldname": "revenues", "fieldtype": "Currency", "width": 120},
        {"label": "Costs", "fieldname": "costs", "fieldtype": "Currency", "width": 120},
        {"label": "Net Profit", "fieldname": "net", "fieldtype": "Currency", "width": 120},
    ]
    vehicles = frappe.get_all("Vehicle", pluck="name")
    data = []
    for v in vehicles:
        rev_raw = frappe.db.get_value("Cost And Revenue Ledger", {"vehicle": v, "type": "Revenue"}, "sum(amount)") or 0
        cost_raw = frappe.db.get_value("Cost And Revenue Ledger", {"vehicle": v, "type": "Cost"}, "sum(amount)") or 0
        rev = _safe_float(rev_raw)
        cost = _safe_float(cost_raw)
        if frappe.db.table_exists("tabFleet Costs"):
            fc_raw = frappe.db.get_value("Fleet Costs", {"vehicle": v}, "sum(amount)") or 0
            cost += _safe_float(fc_raw)
        data.append({"vehicle": v, "revenues": rev, "costs": cost, "net": (rev - cost)})
    return columns, data
