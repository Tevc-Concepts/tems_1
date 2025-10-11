from __future__ import annotations

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def execute():
    if frappe.db.exists("Custom Field", {"dt": "Vehicle", "fieldname": "vehicle_type"}):
        return
    create_custom_field(
        "Vehicle",
        {
            "fieldname": "vehicle_type",
            "label": "Vehicle Type",
            "fieldtype": "Select",
            "options": "Cargo\nPassenger",
            "insert_after": "custom_tems_details",
            "in_standard_filter": 1,
            "reqd": 1,
        },
    )
