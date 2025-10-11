from frappe.model.document import Document
import frappe
from frappe.utils import nowdate
from datetime import datetime
from frappe import _

class OperationPlan(Document):
    # on save checks if vehicle is available in the given time range
    def validate(self):
        # sync operation_mode from vehicle.vehicle_type if vehicle present
        veh = getattr(self, "vehicle", None)
        if veh:
            vtype = frappe.db.get_value("Vehicle", veh, "vehicle_type") or frappe.db.get_value("Vehicle", veh, "custom_vehicle_type")
            if vtype:
                vtype_norm = str(vtype).strip().title()
                # normalize to Title case matching Select options
                if vtype_norm in {"Cargo", "Passenger"}:
                    self.operation_mode = vtype_norm
        # availability check
        if not self.is_vehicle_available():
            frappe.throw(_("Vehicle is not available in the selected time range"))

    def is_vehicle_available(self):
        # Ensure required attributes exist
        veh = getattr(self, "vehicle", None)
        st = getattr(self, "start_time", None)
        et = getattr(self, "end_time", None)
        if veh is None or st is None or et is None:
            return True
        if not veh or not st or not et:
            return True
        overlapping_plans = frappe.get_all(
            "Operation Plan",
            filters={
                "vehicle": veh,
                "name": ["!=", self.name],
                "status": ["in", ["Assigned", "Active"]],
                # Overlap logic: (start_time < self.end_time) and (end_time > self.start_time)
                "start_time": ["<", et],
                "end_time": [">", st],
            },
            limit=1,
        )
        return len(overlapping_plans) == 0
    
    def on_save(self):
    # if end time is past and vehicle assigned, set status to completed
        et = getattr(self, "end_time", None)
        if et:
            # Parse end_time and nowdate to datetime objects for accurate comparison
            try:
                end_time_dt = datetime.strptime(str(et), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                end_time_dt = datetime.strptime(str(et), "%Y-%m-%d")
            now_dt = datetime.strptime(nowdate(), "%Y-%m-%d")
            if end_time_dt.date() < now_dt.date() and self.status == "Assigned":
                self.status = "Completed"
            elif end_time_dt.date() < now_dt.date() and self.status == "Active":
                self.status = "Expired"

