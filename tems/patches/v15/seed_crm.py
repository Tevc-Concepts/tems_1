import frappe


def execute():
    customer = frappe.db.get_value("Customer", {"docstatus": ["!=", 2]}, "name")
    if customer and not frappe.db.exists("Field Service Request", {"customer": customer}):
        doc = frappe.new_doc("Field Service Request")
        doc.update({
            "customer": customer,
            "request_type": "Inspection",
            "priority": "Low",
        })
        try:
            doc.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
