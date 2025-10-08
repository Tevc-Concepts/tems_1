from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate
from .seed_utils import ensure_min_records, log_error


def seed_climate_records(context, count: int = 20):
    vehicles = context.get("vehicles", [])
    emissions = []
    alerts = []
    for i in range(count):
        if not vehicles:
            break
        if frappe.db.exists("DocType", "Emission Log"):
            em = frappe.get_doc({
                "doctype": "Emission Log",
                "vehicle": random.choice(vehicles),
                "emission_date": nowdate() if frappe.db.has_column("Emission Log", "emission_date") else None,
                "co2_kg": random.uniform(10, 120) if frappe.db.has_column("Emission Log", "co2_kg") else None,
            })
            try:
                em.insert(ignore_permissions=True)
                emissions.append(em.name)
            except Exception as e:
                log_error(context, "Emission Log", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Climate Alert"):
            ca = frappe.get_doc({
                "doctype": "Climate Alert",
                "vehicle": random.choice(vehicles),
                "alert_type": random.choice(["Heat", "Flood", "Storm"]) if frappe.db.has_column("Climate Alert", "alert_type") else None,
                "alert_date": nowdate() if frappe.db.has_column("Climate Alert", "alert_date") else None,
            })
            try:
                ca.insert(ignore_permissions=True)
                alerts.append(ca.name)
            except Exception as e:
                log_error(context, "Climate Alert", e)
                frappe.db.rollback()
    context.setdefault("emission_logs", []).extend([e for e in emissions if e not in context.get("emission_logs", [])])
    context.setdefault("climate_alerts", []).extend([a for a in alerts if a not in context.get("climate_alerts", [])])
