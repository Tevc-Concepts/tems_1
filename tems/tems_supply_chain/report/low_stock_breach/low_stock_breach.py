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
    # Determine spare part doctype name
    dt = "Spare Part" if frappe.db.table_exists("tabSpare Part") else ("Spare Part" if frappe.db.table_exists("tabSpare Part") else None)
    columns = [
        {"label": "Record", "fieldname": "name", "fieldtype": "Data", "width": 140},
        {"label": "Item", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 140},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 80},
        {"label": "Min Stock", "fieldname": "min_stock", "fieldtype": "Float", "width": 100},
        {"label": "Reorder Qty", "fieldname": "reorder_qty", "fieldtype": "Float", "width": 110},
    ]
    if not dt:
        return columns, []
    parts = frappe.get_all(dt, fields=["name", "min_stock", "reorder_qty", "items"], filters=[["min_stock", ">", 0]])
    data = []
    for p in parts:
        item_code = getattr(p, "items", None)
        qty_raw = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty") if item_code else 0
        qty = _safe_float(qty_raw)
        min_stock = _safe_float(p.min_stock)
        if qty < min_stock:
            data.append({
                "name": p.name,
                "item_code": item_code,
                "qty": qty,
                "min_stock": min_stock,
                "reorder_qty": p.reorder_qty,
            })
    return columns, data
