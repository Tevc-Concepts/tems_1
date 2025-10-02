from __future__ import annotations

import frappe


def execute(filters=None):
    filters = filters or {}
    for_date = filters.get("for_date")
    if not for_date:
        return [], []

    # Aggregate Duty Assignment by status for the date (using date portion of schedule_slot)
    rows = frappe.db.sql(
        """
        select date(schedule_slot) as day, status, count(*) as cnt
        from `tabDuty Assignment`
        where date(schedule_slot) = %(d)s
        group by day, status
        order by status
        """,
        {"d": for_date},
        as_dict=True,
    )

    columns = [
        {"label": "Day", "fieldname": "day", "fieldtype": "Date", "width": 140},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 140},
        {"label": "Count", "fieldname": "cnt", "fieldtype": "Int", "width": 100}
    ]
    return columns, rows
