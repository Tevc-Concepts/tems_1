import frappe
from frappe.utils import now_datetime


def execute():
    # Trade Lane seed
    lanes = [
        ("GH-NG", "Ghana", "Nigeria"),
        ("NG-BJ", "Nigeria", "Benin"),
    ]
    for name, origin, dest in lanes:
        if not frappe.db.exists("Trade Lane", name):
            # Only seed if Countries exist to avoid Link validation errors
            if not (frappe.db.exists("Country", origin) and frappe.db.exists("Country", dest)):
                continue
            doc = frappe.new_doc("Trade Lane")
            doc.update({
                "name": name,
                "origin_country": origin,
                "destination_country": dest,
            })
            try:
                doc.insert(ignore_permissions=True)
            except Exception:
                frappe.db.rollback()

    # A Border Crossing sample (minimal to avoid missing links)
    # Only create if Journey Plan exists
    jp = frappe.db.get_value("Journey Plan", {"docstatus": ["!=", 2]}, "name")
    if jp and not frappe.db.exists("Border Crossing", {"journey_plan": jp}):
        bc = frappe.new_doc("Border Crossing")
        bc.update({
            "journey_plan": jp,
            "border_post": "Noe-Gb",
            "arrival_time": now_datetime(),
        })
        try:
            bc.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
