import frappe
from frappe.utils import nowdate


def execute():
    # Insert a sample Fleet Cost if an Asset exists
    asset = frappe.db.get_value("Asset", {"docstatus": ["!=", 2]}, "name")
    if asset and not frappe.db.exists("Fleet Cost", {"asset": asset}):
        doc = frappe.new_doc("Fleet Cost")
        doc.update({
            "asset": asset,
            "cost_type": "Fuel",
            "amount": 1000,
            "date": nowdate(),
        })
        try:
            doc.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
