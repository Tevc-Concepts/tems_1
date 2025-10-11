from frappe.model.document import Document
import frappe
from frappe.utils import nowdate
from datetime import datetime
from frappe import _

class OperationPlan(Document):
    # on save checks if vehicle is available in the given time range
    def validate(self):
        if not self.is_vehicle_available():
            frappe.throw(_("Vehicle is not available in the selected time range"))

    def is_vehicle_available(self):
        # Ensure required attributes exist
        if not hasattr(self, "vehicle") or not hasattr(self, "start_time") or not hasattr(self, "end_time"):
            return True
        if not self.vehicle or not self.start_time or not self.end_time:
            return True
        overlapping_plans = frappe.get_all(
            "Operation Plan",
            filters={
                "vehicle": self.vehicle,
                "name": ["!=", self.name],
                "status": ["in", ["Assigned", "Active"]],
                # Overlap logic: (start_time < self.end_time) and (end_time > self.start_time)
                "start_time": ["<", self.end_time],
                "end_time": [">", self.start_time],
            },
            limit=1,
        )
        return len(overlapping_plans) == 0
    
    def on_save(self):
    # if end time is past and vehicle assigned, set status to completed
        if hasattr(self, "end_time") and self.end_time:
            # Parse end_time and nowdate to datetime objects for accurate comparison
            try:
                end_time_dt = datetime.strptime(str(self.end_time), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                end_time_dt = datetime.strptime(str(self.end_time), "%Y-%m-%d")
            now_dt = datetime.strptime(nowdate(), "%Y-%m-%d")
            if end_time_dt.date() < now_dt.date() and self.status == "Assigned":
                self.status = "Completed"
            elif end_time_dt.date() < now_dt.date() and self.status == "Active":
                self.status = "Expired"

