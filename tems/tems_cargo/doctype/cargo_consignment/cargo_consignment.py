from frappe.model.document import Document
import frappe


def _get_vehicle_type(vehicle: str) -> str:
    vt = frappe.db.get_value("Vehicle", vehicle, "vehicle_type")
    if not vt:
        vt = frappe.db.get_value("Vehicle", vehicle, "custom_vehicle_type")
    return str(vt or "").strip().lower()


class CargoConsignment(Document):
    def validate(self):
        if self.vehicle:
            vtype = _get_vehicle_type(self.vehicle)
            if vtype != "cargo":
                frappe.throw(f"Vehicle {self.vehicle} is not of type Cargo.")
        # Ensure linked Operation Plan is Cargo mode if present
        if self.operation_plan:
            mode = frappe.db.get_value("Operation Plan", self.operation_plan, "operation_mode") or ""
            if str(mode or "").lower() != "cargo":
                frappe.throw("Operation Plan is not in Cargo mode.")
