from __future__ import annotations
import random
import frappe
from .seed_utils import ensure_min_records, log_error


def seed_informal_records(context, count: int = 20):
    # Informal Operator, Trip Match, Savings Group
    operators = []
    matches = []
    savings = []
    for i in range(count):
        # Using Informal Operator Profile (actual existing doctype)
        if frappe.db.exists("DocType", "Informal Operator Profile"):
            op = frappe.get_doc({
                "doctype": "Informal Operator Profile",
                "phone": f"0803{random.randint(100000,999999)}" if frappe.db.has_column("Informal Operator Profile", "phone") else None,
                "ussd_id": f"USSD{i+1}" if frappe.db.has_column("Informal Operator Profile", "ussd_id") else None,
            })
            try:
                op.insert(ignore_permissions=True)
                operators.append(op.name)
            except Exception as e:
                log_error(context, "Informal Operator Profile", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Trip Match"):
            tm = frappe.get_doc({
                "doctype": "Trip Match",
                "status": "Open" if frappe.db.has_column("Trip Match", "status") else None,
            })
            try:
                tm.insert(ignore_permissions=True)
                matches.append(tm.name)
            except Exception as e:
                log_error(context, "Trip Match", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Savings Group"):
            sg = frappe.get_doc({
                "doctype": "Savings Group",
                "group_name": f"ROSCA {i+1}" if frappe.db.has_column("Savings Group", "group_name") else None,
            })
            try:
                sg.insert(ignore_permissions=True)
                savings.append(sg.name)
            except Exception as e:
                log_error(context, "Savings Group", e)
                frappe.db.rollback()
    context.setdefault("informal_operator_profiles", []).extend([o for o in operators if o not in context.get("informal_operator_profiles", [])])
    context.setdefault("trip_matches", []).extend([m for m in matches if m not in context.get("trip_matches", [])])
    context.setdefault("savings_groups", []).extend([s for s in savings if s not in context.get("savings_groups", [])])
