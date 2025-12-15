from pydoc import doc
from frappe.model.document import Document
from frappe.utils import nowdate

class DriverQualification(Document):
    def before_save(self):
        # Auto compute qualification status
        # Auto compute qualification status

        license_ok = self.license_status == "Valid"
        medical_ok = self.medical_status == "Fit"
        training_ok = self.training_status == "Completed"

        # Risk category logic
        risk_ok = self.risk_category in ["Low", "Medium"]
        if license_ok and medical_ok and training_ok and risk_ok:
            self.overall_qualification_status = "Active"
            self.reason_for_status = "All requirements met"
        else:
            self.overall_qualification_status = "Inactive"
            reasons = []

            if not license_ok:
                reasons.append("License issue")
            if not medical_ok:
                reasons.append("Medical issue")
            if not training_ok:
                reasons.append("Training incomplete")
            if not risk_ok:
                reasons.append("High or Critical risk score")

            self.reason_for_status = ", ".join(reasons)

        self.auto_computed = 1