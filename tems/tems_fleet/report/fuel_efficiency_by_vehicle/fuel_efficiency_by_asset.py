import frappe
from frappe import _
from typing import Any


def execute(filters: dict[str, Any] | None = None):
    filters = filters or {}

    columns = [
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 200},
        {"label": _("Records"), "fieldname": "records", "fieldtype": "Int", "width": 90},
        {"label": _("Distance (km)"), "fieldname": "distance_km", "fieldtype": "Float", "width": 130},
        {"label": _("Fuel (L)"), "fieldname": "liters", "fieldtype": "Float", "width": 100},
        {"label": _("L/100km"), "fieldname": "l_per_100km", "fieldtype": "Float", "width": 110},
    ]

    date_conditions = []
    params: dict[str, Any] = {}
    if filters.get("from_date"):
        date_conditions.append("fl.date >= %(from_date)s")
        params["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        date_conditions.append("fl.date <= %(to_date)s")
        params["to_date"] = filters["to_date"]
    date_clause = (" AND " + " AND ".join(date_conditions)) if date_conditions else ""

    rows: list[dict[str, Any]] = frappe.db.sql(
        f'''
        SELECT
            fl.vehicle,
            COUNT(*) as records,
            SUM(fl.liters) as liters,
            MIN(fl.odometer) as min_odo,
            MAX(fl.odometer) as max_odo
        FROM `tabFuel Log` fl
        WHERE 1=1 {date_clause}
        GROUP BY fl.vehicle
        ORDER BY fl.vehicle
        ''',
        params,
        as_dict=True,
    )

    for r in rows:
        dist = ((r.get("max_odo") or 0) - (r.get("min_odo") or 0))
        liters = r.get("liters") or 0
        r["distance_km"] = dist
        r["l_per_100km"] = (liters / dist * 100.0) if dist else None

    return columns, rows
