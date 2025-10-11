from frappe.model.document import Document
import frappe


class CargoManifest(Document):
    def validate(self):
        veh = getattr(self, "vehicle", None)
        if veh:
            vt = frappe.db.get_value("Vehicle", veh, "vehicle_type") or frappe.db.get_value("Vehicle", veh, "custom_vehicle_type")
            if str(vt or "").strip().lower() != "cargo":
                frappe.throw(f"Vehicle {veh} is not of type Cargo.")
        op = getattr(self, "operation_plan", None)
        if op:
            mode = frappe.db.get_value("Operation Plan", op, "operation_mode")
            if str(mode or "").strip().lower() != "cargo":
                frappe.throw("Operation Plan must be Cargo mode for Cargo Manifest.")
