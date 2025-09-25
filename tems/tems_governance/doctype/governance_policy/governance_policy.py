import frappe
from frappe.model.document import Document


class GovernancePolicy(Document):
    def validate(self):
        attached = self.get("attached_files") or []
        if getattr(self, "acknowledgement_required", 0) and not attached:
            frappe.msgprint("Acknowledgement required — attach at least one file.")
        next_review = self.get("next_review_date")
        review_cycle = self.get("review_cycle")
        effective_from = self.get("effective_from")
        if not next_review and review_cycle and effective_from:
            self.next_review_date = _compute_next_review_date(str(effective_from), str(review_cycle))


def _compute_next_review_date(effective_from: str, cycle: str) -> str:
    from frappe.utils import add_months, getdate

    months_map = {"Monthly": 1, "Quarterly": 3, "Biannually": 6, "Annually": 12}
    months = months_map.get(cycle)
    if not months:
        return effective_from
    return str(add_months(getdate(effective_from), months))
