import frappe

def execute(filters=None):  # frappe standard signature
    data = frappe.db.sql(
        """
        SELECT severity, COUNT(*) as count
        FROM `tabSafety Incident`
        GROUP BY severity
        ORDER BY count DESC
        """,
        as_dict=True,
    )
    columns = [
        {"label": "Severity", "fieldname": "severity", "fieldtype": "Data", "width": 140},
        {"label": "Count", "fieldname": "count", "fieldtype": "Int", "width": 100},
    ]
    return columns, data