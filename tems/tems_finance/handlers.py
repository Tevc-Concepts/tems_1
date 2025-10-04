from __future__ import annotations

import frappe
from typing import Any, Union


def _safe_float(val: Any) -> float:
    try:
        if val in (None, "", []):
            return 0.0
        return float(val)  # type: ignore[arg-type]
    except Exception:
        return 0.0


def recalculate_vehicle_profitability(doc, method=None):
    """Rollup vehicle profitability from ledger + fleet costs + allocations.
    Stores value in Vehicle.custom_profitability (ensure Custom Field exists in fixtures).
    """
    vehicle = getattr(doc, "vehicle", None)
    if not vehicle:
        return
    # Ledger rows (Cost And Revenue Ledger)
    ledger_rows = frappe.get_all(
        "Cost And Revenue Ledger",
        filters={"vehicle": vehicle},
        fields=["type", "amount"],
    )
    revenues = sum(_safe_float(r.get("amount")) for r in ledger_rows if r.get("type") == "Revenue")
    direct_costs = sum(_safe_float(r.get("amount")) for r in ledger_rows if r.get("type") == "Cost")
    # Fleet Costs DocType (may be named 'Fleet Costs')
    if frappe.db.table_exists("tabFleet Costs"):
        fleet_cost_total = frappe.db.get_value(
            "Fleet Costs",
            filters={"vehicle": vehicle},
            fieldname="sum(amount)",
        ) or 0
        direct_costs += _safe_float(fleet_cost_total)
    # Allocation Rules influence distribution; lightweight implementation if Allocation Rule doctype exists.
    if frappe.db.table_exists("Allocation Rule"):
        try:
            rules = frappe.get_all(
                "Allocation Rule",
                filters={"allocation_basis": "Vehicle", "disabled": 0},
                fields=["name", "percentage"],
            )
            for r in rules:
                pct = _safe_float(r.get("percentage"))
                if pct > 0:
                    # treat allocation percentage as overhead applied to direct_costs
                    direct_costs += direct_costs * pct / 100.0
        except Exception:
            pass
    net = revenues - direct_costs
    try:
        frappe.db.set_value("Vehicle", vehicle, "custom_profitability", net)
    except Exception:
        pass


def compute_profitability_for_all():
    """Utility for scheduled job to recompute profitability across all vehicles."""
    vehicles = frappe.get_all("Vehicle", pluck="name")
    for v in vehicles:
        dummy = frappe._dict(vehicle=v)
        recalculate_vehicle_profitability(dummy)

