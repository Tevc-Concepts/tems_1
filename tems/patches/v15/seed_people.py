import frappe
from frappe.utils import add_days, nowdate


def execute():
    # minimal seed: create a few Driver Qualifications with one expired
    employees = frappe.get_all("Employee", fields=["name"], limit=5)
    if not employees:
        return
    for i, emp in enumerate(employees[:3]):
        expiry = add_days(nowdate(), -10) if i == 0 else add_days(nowdate(), 20)
        doc = frappe.get_doc({
            "doctype": "Driver Qualification",
            "employee": emp.name,
            "license_no": f"LIC-{emp.name}",
            "license_class": "B",
            "medical_clearance": nowdate(),
            "expiry_date": expiry,
            "status": "Active" if i != 0 else "Expired",
        })
        doc.insert(ignore_if_duplicate=True)
