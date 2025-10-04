import frappe
from frappe.model.document import Document


class RiskAssessment(Document):
    def validate(self):
        if self.risk_score is not None and self.risk_score < 0:
            frappe.throw("Risk Score cannot be negative")
