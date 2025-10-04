import frappe
from frappe.model.document import Document


class JourneyPlan(Document):
    def validate(self):
        # Basic temporal validation
        if self.end_time and self.start_time and self.end_time < self.start_time:
            frappe.throw("End Time cannot be before Start Time")
