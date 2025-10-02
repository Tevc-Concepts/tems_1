from __future__ import annotations

import frappe


def execute(filters=None):
    f = filters or {}
    conditions = {}
    if f.get("vehicle"):
        conditions["vehicle"] = f.get("vehicle")
    if f.get("from_date") and f.get("to_date"):
        conditions["date"] = ["between", [f.get("from_date"), f.get("to_date")]]

    rows = frappe.get_all(
        "Cost And Revenue Ledger",
        filters=conditions,
        fields=["date", "vehicle", "asset", "type", "amount", "currency", "reference_doctype", "reference_name"],
        order_by="date asc",
    )

    columns = [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 110},
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 140},
        {"label": "Asset", "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 140},
        {"label": "Type", "fieldname": "type", "fieldtype": "Data", "width": 90},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 110},
        {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 90},
        {"label": "Reference", "fieldname": "reference", "fieldtype": "Data", "width": 220}
    ]

    data = []
    for r in rows:
        ref = f"{r.get('reference_doctype') or ''} {r.get('reference_name') or ''}".strip()
        data.append({
            "date": r.get("date"),
            "vehicle": r.get("vehicle"),
            "asset": r.get("asset"),
            "type": r.get("type"),
            "amount": r.get("amount"),
            "currency": r.get("currency"),
            "reference": ref,
        })
    return columns, data
