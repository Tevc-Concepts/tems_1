import frappe
from frappe.utils import now_datetime, nowdate

def execute():
    # Idempotent seed for Safety domain
    # Ensure at least one Safety Incident and a Spot Check exist for demo/testing
    if not frappe.db.exists("Safety Incident", {"title": ("like", "Demo%")}):
        incident = frappe.get_doc({
            "doctype": "Safety Incident",
            "title": "Demo Incident - Near Miss",
            "incident_date": now_datetime(),
            "severity": "near miss",
            "status": "Open",
            "description": "Demo seeded near miss incident during testing."
        })
        incident.insert(ignore_permissions=True)

    if not frappe.db.exists("Spot Check", {"notes": ("like", "Demo%") }):
        # Try to link to any vehicle/employee if available
        vehicle = frappe.db.get_value("Vehicle", {}, "name")
        employee = frappe.db.get_value("Employee", {"status": "Active"}, "name") or frappe.db.get_value("Employee", {}, "name")
        if vehicle:
            sc = frappe.get_doc({
                "doctype": "Spot Check",
                "date": nowdate(),
                "vehicle": vehicle,
                "driver": employee,
                "notes": "Demo seeded spot check"
            })
            sc.insert(ignore_permissions=True)
