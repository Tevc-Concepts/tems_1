import frappe
from frappe.model.document import Document


class ComplianceAudit(Document):
    def validate(self):
        status = (getattr(self, "status", "") or "").lower()
        if status == "closed":
            sev = (getattr(self, "severity", "") or "").lower()
            if sev in ["medium", "high", "critical"]:
                evidence = getattr(self, "evidence", None)
                if not evidence or len(evidence) == 0:
                    frappe.throw("Evidence is required to close Medium+ severity audits")
