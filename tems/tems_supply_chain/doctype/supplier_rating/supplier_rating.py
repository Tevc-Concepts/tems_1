from __future__ import annotations
import frappe
from frappe.model.document import Document


class SupplierRating(Document):
    def validate(self):
        scores = [getattr(self, "on_time_score", None), getattr(self, "quality_score", None), getattr(self, "cost_score", None)]
        nums = [float(s) for s in scores if s not in (None, "", [])]
        if nums:
            self.composite_score = round(sum(nums) / len(nums), 2)
