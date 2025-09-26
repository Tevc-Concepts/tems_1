import frappe


def execute():
    # Seed a couple of Informal Operators
    operators = [
        {"phone": "+234800000001"},
        {"phone": "+234800000002"},
    ]
    for op in operators:
        if not frappe.db.exists("Informal Operator Profile", {"phone": op["phone"]}):
            doc = frappe.new_doc("Informal Operator Profile")
            doc.update(op)
            try:
                doc.insert(ignore_permissions=True)
            except Exception:
                frappe.db.rollback()
