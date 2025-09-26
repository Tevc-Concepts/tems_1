import frappe


def execute():
    # Create a Document Checklist for Vehicle context with one sample item
    if not frappe.db.exists("Document Checklist", {"context": "Vehicle"}):
        checklist = frappe.new_doc("Document Checklist")
        checklist.update({"context": "Vehicle", "title": "Standard Compliance"})
        # child table may be empty; insert doc first, then append to avoid validation issues
        try:
            checklist.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
            return

        if not frappe.db.exists("DocType", "Document Checklist Item"):
            return

        try:
            checklist.append("items", {"doc_type": "Registration Certificate"})
            checklist.save(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
