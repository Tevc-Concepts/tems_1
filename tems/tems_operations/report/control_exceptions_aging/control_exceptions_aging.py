from __future__ import annotations

import frappe
from frappe.utils import now_datetime


def execute(filters=None):
    filters = filters or {}
    status = filters.get("status") or "Open"
    rows = frappe.get_all(
        "Control Exception",
        filters={"status": status},
        fields=["name", "vehicle", "occurred_at", "severity", "sla_minutes", "sla_breached"],
        order_by="occurred_at asc",
    )

    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Data", "width": 160},
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "Occurred At", "fieldname": "occurred_at", "fieldtype": "Datetime", "width": 160},
        {"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 100},
        {"label": "Age (min)", "fieldname": "age_minutes", "fieldtype": "Int", "width": 100},
        {"label": "SLA (min)", "fieldname": "sla_minutes", "fieldtype": "Int", "width": 100},
        {"label": "SLA Breached", "fieldname": "sla_breached", "fieldtype": "Check", "width": 100}
    ]

    data = []
    now_ts = now_datetime()
    for r in rows:
        occurred = r.get("occurred_at")
        age = 0
        if occurred:
            age = int((now_ts - occurred).total_seconds() // 60)
        data.append({
            "name": r["name"],
            "vehicle": r.get("vehicle"),
            "occurred_at": occurred,
            "severity": r.get("severity"),
            "age_minutes": age,
            "sla_minutes": r.get("sla_minutes"),
            "sla_breached": r.get("sla_breached"),
        })

    return columns, data
