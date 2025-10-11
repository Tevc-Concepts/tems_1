from frappe.model.document import Document
import frappe


class PassengerManifest(Document):
    def validate(self):
        veh = getattr(self, "vehicle", None)
        if veh:
            vt = frappe.db.get_value("Vehicle", veh, "vehicle_type") or frappe.db.get_value("Vehicle", veh, "custom_vehicle_type")
            if str(vt or "").strip().lower() != "passenger":
                frappe.throw(f"Vehicle {veh} is not of type Passenger.")
