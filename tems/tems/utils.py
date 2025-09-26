import frappe

@frappe.whitelist()
def doc_exists(doctype: str, name: str | None = None, filters: dict | None = None):
    if name:
        return bool(frappe.db.exists(doctype, name))
    return bool(frappe.db.exists(doctype, filters or {}))
