from __future__ import annotations

import frappe


def execute(filters=None):
    filters = filters or {}
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    if not from_date or not to_date:
        return [], []

    # Using Operations Event: assume journey_reference encodes route; Shift can be derived from Dispatch Schedule if joined later.
    events = frappe.get_all(
        "Operations Event",
        filters={"event_type": "Arrive", "event_time": ["between", [from_date, to_date]]},
        fields=["journey_reference", "variance_minutes"],
    )

    rows_map = {}
    for e in events:
        route = (e.get("journey_reference") or "").split("|")[0] or "Unknown Route"
        shift = "Unknown"  # Placeholder until deeper linkage is added
        key = (route, shift)
        if key not in rows_map:
            rows_map[key] = {"total": 0, "on_time": 0}
        rows_map[key]["total"] += 1
        if (e.get("variance_minutes") or 0) <= 5:
            rows_map[key]["on_time"] += 1

    columns = [
        {"label": "Route", "fieldname": "route", "fieldtype": "Data", "width": 200},
        {"label": "Shift", "fieldname": "shift", "fieldtype": "Data", "width": 120},
        {"label": "Total", "fieldname": "total", "fieldtype": "Int", "width": 100},
        {"label": "On-Time", "fieldname": "on_time", "fieldtype": "Int", "width": 100},
        {"label": "OTP %", "fieldname": "otp", "fieldtype": "Percent", "width": 100},
    ]

    data = []
    for (route, shift), v in rows_map.items():
        otp = round((v["on_time"] * 100.0 / v["total"]) if v["total"] else 0, 2)
        data.append({"route": route, "shift": shift, "total": v["total"], "on_time": v["on_time"], "otp": otp})

    return columns, data
