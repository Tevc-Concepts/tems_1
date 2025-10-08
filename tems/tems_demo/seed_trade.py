from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate
from .seed_utils import ensure_min_records, log_error

COUNTRIES = ["NG", "GH", "BJ", "TG", "CM"]


def seed_trade_records(context, count: int = 20):
    vehicles = context.get("vehicles", [])
    borders = []
    compliances = []
    for i in range(count):
        if not vehicles:
            break
        if frappe.db.exists("DocType", "Border Crossing"):
            bc = frappe.get_doc({
                "doctype": "Border Crossing",
                "vehicle": random.choice(vehicles),
                "from_country": random.choice(COUNTRIES) if frappe.db.has_column("Border Crossing", "from_country") else None,
                "to_country": random.choice(COUNTRIES) if frappe.db.has_column("Border Crossing", "to_country") else None,
                "crossing_date": nowdate() if frappe.db.has_column("Border Crossing", "crossing_date") else None,
            })
            try:
                bc.insert(ignore_permissions=True)
                borders.append(bc.name)
            except Exception as e:
                log_error(context, "Border Crossing", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Trade Compliance Log"):
            tc = frappe.get_doc({
                "doctype": "Trade Compliance Log",
                "vehicle": random.choice(vehicles),
                "compliance_status": random.choice(["Pass", "Warn", "Fail"]) if frappe.db.has_column("Trade Compliance Log", "compliance_status") else None,
            })
            try:
                tc.insert(ignore_permissions=True)
                compliances.append(tc.name)
            except Exception as e:
                log_error(context, "Trade Compliance Log", e)
                frappe.db.rollback()
    context.setdefault("border_crossings", []).extend([b for b in borders if b not in context.get("border_crossings", [])])
    context.setdefault("trade_compliance_logs", []).extend([c for c in compliances if c not in context.get("trade_compliance_logs", [])])
