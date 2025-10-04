from __future__ import annotations
import frappe
from frappe.model.document import Document
from typing import Any


class JourneyCosting(Document):
    def validate(self):
        total_revenue = getattr(self, "total_revenue", 0) or 0
        total_cost = getattr(self, "total_cost", 0) or 0
        self.margin = (total_revenue - total_cost)
