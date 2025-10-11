import frappe
from frappe.model.document import Document


class JourneyPlan(Document):
    def validate(self):
        # Basic temporal validation
        if self.end_time and self.start_time and self.end_time < self.start_time:
            frappe.throw("End Time cannot be before Start Time")

        # Check for overlapping journey plans for the same vehicle
        overlapping_plans = frappe.db.sql("""
            SELECT name FROM `tabJourney Plan`
            WHERE vehicle = %s
            AND name != %s
            AND (
                (start_time <= %s AND end_time >= %s) OR
                (start_time <= %s AND end_time >= %s) OR
                (start_time >= %s AND end_time <= %s)
            )
        """, (self.vehicle, self.name or '', self.start_time, self.start_time,
              self.end_time, self.end_time, self.start_time, self.end_time), as_dict=True)  
        if overlapping_plans:
            frappe.throw(f"Overlapping journey plan exists for vehicle {self.vehicle}: {', '.join([plan.name for plan in overlapping_plans])}") 

        # Ensure all required fields are filled
        required_fields = ['vehicle', 'driver', 'start_time', 'end_time', 'route']
        for field in required_fields:
            if not getattr(self, field):
                frappe.throw(f"{field.replace('_', ' ').title()} is required.")     
        # Additional custom validations can be added here

        