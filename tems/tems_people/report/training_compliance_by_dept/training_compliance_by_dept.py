import frappe
from frappe import _
from typing import Any


def execute(filters: dict[str, Any] | None = None) -> tuple[list[dict], list[dict]]:
    filters = filters or {}

    columns: list[dict] = [
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 200},
        {"label": _("Employees"), "fieldname": "employees", "fieldtype": "Int", "width": 100},
        {"label": _("Completed"), "fieldname": "completed", "fieldtype": "Int", "width": 100},
        {"label": _("In Progress"), "fieldname": "in_progress", "fieldtype": "Int", "width": 110},
        {"label": _("Planned"), "fieldname": "planned", "fieldtype": "Int", "width": 100},
        {"label": _("Completion %"), "fieldname": "completion_pct", "fieldtype": "Percent", "width": 120},
    ]

    date_conditions = []
    params = {}
    if filters.get("from_date"):
        date_conditions.append("tr.start_date >= %(from_date)s")
        params["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        date_conditions.append("tr.end_date <= %(to_date)s")
        params["to_date"] = filters["to_date"]
    date_clause = (" AND " + " AND ".join(date_conditions)) if date_conditions else ""

    # Aggregate training status per department
    data: list[dict] = frappe.db.sql(
        f'''
        SELECT
            e.department as department,
            COUNT(DISTINCT e.name) as employees,
            SUM(CASE WHEN tr.status = 'Completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN tr.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN tr.status = 'Planned' THEN 1 ELSE 0 END) as planned
        FROM `tabEmployee` e
        LEFT JOIN `tabTraining Record` tr ON tr.employee = e.name{date_clause}
        WHERE e.status = 'Active'
        GROUP BY e.department
        ORDER BY e.department
        ''',
        params,
        as_dict=True,
    )

    # Compute completion percentage per department
    for row in data:
        total = (row.get("completed") or 0) + (row.get("in_progress") or 0) + (row.get("planned") or 0)
        row["completion_pct"] = (row["completed"] / total * 100.0) if total else 0

    return columns, data
