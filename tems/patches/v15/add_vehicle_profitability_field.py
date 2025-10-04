from __future__ import annotations

import frappe


def execute():  # pragma: no cover - patch execution side-effect oriented
    """Ensure Vehicle.custom_profitability custom field exists.

    We previously shipped this via a large corrupted Custom Field fixture which has been
    disabled while fixtures are minimized. This patch idempotently creates the field.
    """
    fieldname = "custom_profitability"
    doctype = "Vehicle"
    df_name = f"{doctype}-{fieldname}"

    if frappe.db.exists("Custom Field", df_name):
        return

    try:
        cf = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": doctype,
            "name": df_name,
            "fieldname": fieldname,
            "label": "Profitability",
            "fieldtype": "Currency",
            "insert_after": "license_plate" if frappe.db.has_column("Vehicle", "license_plate") else None,
            "read_only": 1,
            "no_copy": 1,
            "in_list_view": 1,
            "in_standard_filter": 0,
            "translatable": 0,
        })
        cf.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error(title="add_vehicle_profitability_field patch failed", message=frappe.get_traceback())
