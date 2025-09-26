import frappe


def execute():
    item = frappe.db.get_value("Item", {"docstatus": ["!=", 2]}, "name")
    if item and not frappe.db.exists("Spare Part", {"item": item}):
        doc = frappe.new_doc("Spare Part")
        doc.update({
            "item": item,
            "min_stock": 5,
            "reorder_qty": 10,
        })
        try:
            doc.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
