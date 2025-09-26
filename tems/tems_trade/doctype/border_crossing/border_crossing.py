import frappe
from frappe.model.document import Document
from frappe.utils import cint, time_diff_in_seconds


class BorderCrossing(Document):
    def validate(self):
        arrival = getattr(self, "arrival_time", None)
        departure = getattr(self, "departure_time", None)
        if arrival and departure and departure >= arrival:
            delta = time_diff_in_seconds(departure, arrival) // 60
            self.wait_duration = cint(delta)

