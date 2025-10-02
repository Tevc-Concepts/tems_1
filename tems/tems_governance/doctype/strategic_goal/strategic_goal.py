import frappe
from frappe.model.document import Document


class StrategicGoal(Document):
    def validate(self):
        eff_from = getattr(self, "effective_from", None)
        eff_to = getattr(self, "effective_to", None)
        if eff_from and eff_to and eff_to < eff_from:
            frappe.throw("Effective To cannot be earlier than Effective From")
