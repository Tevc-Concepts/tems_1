from __future__ import annotations

import frappe


def recalculate_vehicle_profitability(doc, method=None):
    """Rollup vehicle profitability from ledger entries. Placeholder implementation."""
    vehicle = getattr(doc, "vehicle", None)
    if not vehicle:
        return
    # Example: compute net = revenues - costs
    rows = frappe.get_all(
        "Cost & Revenue Ledger",
        filters={"vehicle": vehicle},
        fields=["type", "amount"],
    )
    net = 0
    for r in rows:
        if r["type"] == "Revenue":
            net += float(r.get("amount") or 0)
        else:
            net -= float(r.get("amount") or 0)
    # Store as a custom field on Vehicle if present
    try:
        frappe.db.set_value("Vehicle", vehicle, "custom_profitability", net)
    except Exception:
        pass
