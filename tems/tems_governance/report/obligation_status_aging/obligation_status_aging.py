import frappe
from frappe.utils import nowdate, date_diff, getdate


def execute(filters=None):
    data = []
    columns = [
        {"label": "Obligation", "fieldname": "name", "fieldtype": "Link", "options": "Compliance Obligation"},
        {"label": "Title", "fieldname": "title", "fieldtype": "Data"},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data"},
        {"label": "Next Due Date", "fieldname": "next_due_date", "fieldtype": "Date"},
        {"label": "Days To Due", "fieldname": "days_to_due", "fieldtype": "Int"},
    ]
    rows = frappe.get_all("Compliance Obligation", fields=["name", "title", "status", "next_due_date"], order_by="next_due_date asc")
    for r in rows:
        due = getdate(r.get("next_due_date")) if r.get("next_due_date") else getdate(nowdate())
        days_to_due = date_diff(str(due), nowdate())
        data.append({
            "name": r.get("name"),
            "title": r.get("title"),
            "status": r.get("status"),
            "next_due_date": r.get("next_due_date"),
            "days_to_due": days_to_due,
        })
    return columns, data
