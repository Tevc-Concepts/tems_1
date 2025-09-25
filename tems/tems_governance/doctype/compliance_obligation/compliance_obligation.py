import frappe
from frappe.model.document import Document


class ComplianceObligation(Document):
    def validate(self):
        if getattr(self, "status", "") == "Compliant" and getattr(self, "evidence_required", 0):
            files = self.get("evidence_files") or []
            if not files:
                frappe.throw("Evidence required — attach at least one file before marking as Compliant.")
