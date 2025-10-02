from __future__ import annotations

import frappe


def link_spare_parts_to_asset(doc, method=None):
    # Placeholder to satisfy hook; real implementation can create Spare Requests if shortages
    frappe.logger("tems").info("Procurement Order submitted: %s", getattr(doc, "name", None))
