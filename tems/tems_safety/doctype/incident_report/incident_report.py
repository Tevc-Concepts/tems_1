import frappe
from frappe.model.document import Document
from frappe.utils import nowdate


class IncidentReport(Document):
    def validate(self):
        if self.incident_date and self.reported_date:
            if self.reported_date < self.incident_date:
                frappe.throw("Reported Date cannot be earlier than Incident Date")

        if self.closed_date and self.reported_date:
            if self.closed_date < self.reported_date:
                frappe.throw("Closed Date cannot be earlier than Reported Date")
        if self.closed_date and self.incident_date:
            if self.closed_date < self.incident_date:
                frappe.throw("Closed Date cannot be earlier than Incident Date")
        
        if self.status == "Closed":
            self.closed_date = nowdate()
            self.reporter = frappe.session.user
            self.reported_date = nowdate()
            self.save()

        
