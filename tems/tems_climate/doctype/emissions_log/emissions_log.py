import frappe
from frappe.model.document import Document


class EmissionsLog(Document):
    def validate(self):
        liters = getattr(self, "fuel_liters", 0) or 0
        factor = getattr(self, "emission_factor", 0) or 0
        if liters and factor:
            self.co2e_kg = liters * factor
