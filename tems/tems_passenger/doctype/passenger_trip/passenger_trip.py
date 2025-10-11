from frappe.model.document import Document
import frappe


class PassengerTrip(Document):
    def validate(self):
        if self.vehicle:
            vt = frappe.db.get_value("Vehicle", self.vehicle, "vehicle_type") or frappe.db.get_value("Vehicle", self.vehicle, "custom_vehicle_type")
            if str(vt or "").strip().lower() != "passenger":
                frappe.throw(f"Vehicle {self.vehicle} is not of type Passenger.")
        if self.operation_plan:
            mode = frappe.db.get_value("Operation Plan", self.operation_plan, "operation_mode") or ""
            if str(mode or "").strip().lower() != "passenger":
                frappe.throw("Operation Plan is not in Passenger mode.")
