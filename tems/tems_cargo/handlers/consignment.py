from __future__ import annotations
import frappe

def validate_vehicle_type(doc, method=None):
    vehicle = getattr(doc, "vehicle", None)
    if not vehicle:
        return
    vtype = frappe.db.get_value("Vehicle", vehicle, "vehicle_type") or frappe.db.get_value("Vehicle", vehicle, "custom_vehicle_type")
    vtype_s = str(vtype or "").strip().lower()
    if vtype_s != "cargo":
        frappe.throw(f"Vehicle {vehicle} is not of type Cargo.")
