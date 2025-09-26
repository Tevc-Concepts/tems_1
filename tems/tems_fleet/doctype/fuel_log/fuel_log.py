import frappe
from frappe.model.document import Document
from typing import Any


class FuelLog(Document):
    def validate(self):
        liters_val: Any = self.get("liters")
        price_val: Any = self.get("price_per_liter")
        try:
            liters = float(liters_val or 0)
            price = float(price_val or 0)
        except Exception:
            liters = 0.0
            price = 0.0
        self.total_cost = liters * price if (liters and price) else 0.0
