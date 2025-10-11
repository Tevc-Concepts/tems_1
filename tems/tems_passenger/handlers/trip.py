from __future__ import annotations
import frappe


def validate_vehicle_type(doc, method=None):
    vehicle = getattr(doc, "vehicle", None)
    if not vehicle:
        return
    vt = frappe.db.get_value("Vehicle", vehicle, "vehicle_type") or frappe.db.get_value("Vehicle", vehicle, "custom_vehicle_type")
    vt_s = str(vt or "").strip().lower()
    if vt_s != "passenger":
        frappe.throw(f"Vehicle {vehicle} is not of type Passenger.")
