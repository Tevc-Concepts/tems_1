from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate
from .seed_utils import ensure_min_records


def seed_supply_chain_records(context, count: int = 20):
    # Example: Supplier Rating, Logistics Task (if exist)
    suppliers = context.get("suppliers", [])
    ratings = []
    tasks = []
    for i in range(count):
        if frappe.db.exists("DocType", "Supplier Rating") and suppliers:
            r = frappe.get_doc({
                "doctype": "Supplier Rating",
                "supplier": random.choice(suppliers),
                "rating": random.randint(1, 5) if frappe.db.has_column("Supplier Rating", "rating") else None,
                "rating_date": nowdate() if frappe.db.has_column("Supplier Rating", "rating_date") else None,
            })
            try:
                r.insert(ignore_permissions=True)
                ratings.append(r.name)
            except Exception:
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Logistics Task"):
            t = frappe.get_doc({
                "doctype": "Logistics Task",
                "subject": f"Task {i+1}",
            })
            try:
                t.insert(ignore_permissions=True)
                tasks.append(t.name)
            except Exception:
                frappe.db.rollback()
    context.setdefault("supplier_ratings", []).extend([r for r in ratings if r not in context.get("supplier_ratings", [])])
    context.setdefault("logistics_tasks", []).extend([t for t in tasks if t not in context.get("logistics_tasks", [])])
