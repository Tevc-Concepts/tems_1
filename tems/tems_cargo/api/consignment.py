import frappe
from frappe import _


@frappe.whitelist()
def create_consignment(customer: str, vehicle: str, operation_plan: str, origin: str, destination: str, cargo_weight: float = 0.0, cargo_value: float = 0.0):
    doc = frappe.get_doc({
        "doctype": "Cargo Consignment",
        "customer": customer,
        "vehicle": vehicle,
        "operation_plan": operation_plan,
        "origin": origin,
        "destination": destination,
        "cargo_weight": cargo_weight,
        "cargo_value": cargo_value,
    })
    doc.insert(ignore_permissions=True)
    return doc.name
