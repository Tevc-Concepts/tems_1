import frappe


def execute():
    # Create a simple Emissions Log if a Vehicle exists
    vehicle = frappe.db.get_value("Vehicle", {"docstatus": ["!=", 2]}, "name")
    if vehicle and not frappe.db.exists("Emissions Log", {"vehicle": vehicle}):
        doc = frappe.new_doc("Emissions Log")
        doc.update({
            "vehicle": vehicle,
            "fuel_liters": 10,
            "emission_factor": 2.68,
        })
        try:
            doc.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
