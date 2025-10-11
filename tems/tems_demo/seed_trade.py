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
    if not vehicles:
        return borders
    # Limit to a smaller, safe number for Border Crossing to avoid mandatory field spam
    border_target = min(count, 5)
    border_attempts = 0
    if frappe.db.exists("DocType", "Border Crossing"):
        required_cols = {c for c in ("vehicle", "from_country", "to_country", "crossing_date") if frappe.db.has_column("Border Crossing", c)}
        while len(borders) < border_target and border_attempts < border_target * 3:
            border_attempts += 1
            bc_doc = {
                "doctype": "Border Crossing",
                "vehicle": random.choice(vehicles) if "vehicle" in required_cols else None,
                "from_country": random.choice(COUNTRIES) if "from_country" in required_cols else None,
                "to_country": random.choice(COUNTRIES) if "to_country" in required_cols else None,
                "crossing_date": nowdate() if "crossing_date" in required_cols else None,
            }
            # If any required column missing (value None) skip to avoid error spam
            if any(v is None for k, v in bc_doc.items() if k != "doctype" and k in required_cols):
                continue
            try:
                bc = frappe.get_doc(bc_doc)
                bc.insert(ignore_permissions=True, ignore_mandatory=True)
                borders.append(bc.name)
                frappe.db.commit()
            except Exception as e:
                # Log only first 3 unique errors to keep log concise
                if len({e.__class__.__name__ for e_line in context.get("_errors", [])}) < 3:
                    log_error(context, "Border Crossing", e)
                frappe.db.rollback()
    # Trade Compliance Logs (unchanged logic but with cap equal to count)
    if frappe.db.exists("DocType", "Trade Compliance Log"):
        for _ in range(min(count, 20)):
            tc = frappe.get_doc({
                "doctype": "Trade Compliance Log",
                "vehicle": random.choice(vehicles),
                "compliance_status": random.choice(["Pass", "Warn", "Fail"]) if frappe.db.has_column("Trade Compliance Log", "compliance_status") else None,
            })
            try:
                tc.insert(ignore_permissions=True, ignore_mandatory=True)
                compliances.append(tc.name)
                frappe.db.commit()
            except Exception as e:
                log_error(context, "Trade Compliance Log", e)
                frappe.db.rollback()
    context.setdefault("border_crossings", []).extend([b for b in borders if b not in context.get("border_crossings", [])])
    context.setdefault("trade_compliance_logs", []).extend([c for c in compliances if c not in context.get("trade_compliance_logs", [])])
