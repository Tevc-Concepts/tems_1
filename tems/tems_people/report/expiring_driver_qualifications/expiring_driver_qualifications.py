from __future__ import annotations
import frappe
from frappe.utils import add_days, getdate, nowdate


def execute(filters=None):
    days = (filters or {}).get("days") or 30
    cutoff = add_days(getdate(), int(days))
    quals = frappe.get_all(
        "Driver Qualification",
        filters={"expiry_date": ["between", [nowdate(), cutoff]]},
        fields=["name", "employee", "expiry_date", "status"],
    )
    columns = [
        {"label": "Qualification", "fieldname": "name", "fieldtype": "Link", "options": "Driver Qualification", "width": 140},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 140},
        {"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "width": 110},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]
    return columns, quals
