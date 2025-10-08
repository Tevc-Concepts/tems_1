from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate
from .seed_utils import ensure_min_records, log_error

CURRENCIES = ["USD", "NGN", "EUR"]


def seed_costs_and_revenues(context, count: int = 40):
    vehicles = context.get("vehicles", [])
    assets = context.get("assets", [])
    ledger_entries = context.setdefault("cost_revenue_ledger", [])
    if not ledger_entries:
        existing = frappe.get_all("Cost And Revenue Ledger", pluck="name", limit=count)
        ledger_entries.extend(existing)
    attempt_limit = count * 4
    i = 0
    while len(ledger_entries) < count and i < attempt_limit:
        i += 1
        if not vehicles:
            break
        veh = random.choice(vehicles)
        asset = random.choice(assets) if assets else None
        typ = "Revenue" if (len(ledger_entries) % 2) else "Cost"
        amount = random.randint(50, 800) * (1 if typ == "Revenue" else 1)
        cur = random.choice(CURRENCIES)
        if not frappe.db.exists("DocType", "Cost And Revenue Ledger"):
            break
        doc = frappe.get_doc({
            "doctype": "Cost And Revenue Ledger",
            "date": nowdate(),
            "vehicle": veh,
            "type": typ,
            "amount": amount,
            "currency": cur,
            "asset": asset
        })
        try:
            if len(ledger_entries) < count:
                doc.insert(ignore_permissions=True, ignore_mandatory=True)
                frappe.db.commit()
                ledger_entries.append(doc.name)
        except Exception as e:
            log_error(context, "Cost And Revenue Ledger", e)
            frappe.db.rollback()
