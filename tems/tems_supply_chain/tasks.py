"""Scheduled tasks for TEMS Supply Chain domain."""
from __future__ import annotations

import frappe
from frappe.utils import nowdate


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][SupplyChain] {msg}")


def low_stock_alert() -> None:
    """Identify Spare Parts below min stock and raise a Notification Communication.
    This is a lightweight placeholder; real implementation could create Material Requests.
    """
    # Expect DocType name maybe 'Spare Parts'; keep dynamic fallback.
    doctype_candidates = ["Spare Part", "Spare Part"]
    target_doctype = None
    for dt in doctype_candidates:
        if frappe.db.table_exists(f"tab{dt}"):
            target_doctype = dt
            break
    if not target_doctype:
        _log("No Spare Part(s) DocType found; skipping low_stock_alert")
        return
    rows = frappe.get_all(target_doctype, fields=["name", "min_stock", "reorder_qty"], filters=[["min_stock", ">", 0]])
    if not rows:
        _log("No spare part definitions with min_stock set")
        return
    breaches = []
    for r in rows:
        # Attempt to find current bin qty via Item table link (assuming field 'items')
        item_code = frappe.db.get_value(target_doctype, r.name, "items")
        if not item_code:
            continue
        qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty") or 0
        if r.min_stock and qty < r.min_stock:
            breaches.append((r.name, item_code, qty, r.min_stock))
    if not breaches:
        _log("No low stock breaches")
        return
    for name, item_code, qty, min_stock in breaches:
        key = f"LOW-STOCK-{item_code}-{nowdate()}"
        exists = frappe.db.exists("Communication", {"subject": key})
        if exists:
            continue
        try:
            frappe.get_doc(
                {
                    "doctype": "Communication",
                    "communication_type": "Notification",
                    "subject": key,
                    "content": f"Item {item_code} stock {qty} below minimum {min_stock} (Record: {name})",
                }
            ).insert(ignore_permissions=True)
        except Exception:
            _log(f"Failed to create low stock notification for {item_code}")
    _log(f"Low stock alerts processed: {len(breaches)} breaches")
