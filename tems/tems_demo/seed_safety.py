from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate, now_datetime, add_to_date
from .seed_utils import ensure_min_records, log_error
try:
    from . import settings as demo_settings
except Exception:  # pragma: no cover
    demo_settings = None

INCIDENT_TYPES = ["Minor", "Major", "Near Miss"]


def seed_safety_records(context, count: int = 20, spot_check_target: int | None = None):
    vehicles = context.get("vehicles", [])
    employees = context.get("employees", [])
    journey_plans = context.setdefault("journey_plans", [])
    incidents = context.setdefault("incident_reports", [])
    risks = context.setdefault("risk_assessments", [])
    if not journey_plans:
        journey_plans.extend(frappe.get_all("Journey Plan", pluck="name", limit=count))
    if not incidents:
        incidents.extend(frappe.get_all("Incident Report", pluck="name", limit=count))
    if not risks:
        risks.extend(frappe.get_all("Risk Assessment", pluck="name", limit=count))
    i = 0
    # Continue looping until each target met or safety cap
    safety_cap = count * 5
    spot_checks_ctx = context.setdefault("spot_checks", [])
    if spot_check_target is None and demo_settings:
        spot_check_target = demo_settings.TARGETS.get("Spot Check", 0)
    if spot_check_target is None:
        spot_check_target = 0
    while ((len(journey_plans) < count) or (len(incidents) < count) or (len(risks) < count) or (len(spot_checks_ctx) < spot_check_target)) and i < safety_cap:
        i += 1
        if not vehicles:
            break
        veh = random.choice(vehicles)
        drv = random.choice(employees) if employees else None
        if frappe.db.exists("DocType", "Journey Plan"):
            start = now_datetime()
            end = add_to_date(start, hours=5)
            jp = frappe.get_doc({
                "doctype": "Journey Plan",
                "vehicle": veh,
                "driver": drv,
                "start_time": start if frappe.db.has_column("Journey Plan", "start_time") else None,
                "end_time": end if frappe.db.has_column("Journey Plan", "end_time") else None,
            })
            try:
                if len(journey_plans) < count:
                    jp.insert(ignore_permissions=True, ignore_mandatory=True)
                    frappe.db.commit()
                    journey_plans.append(jp.name)
            except Exception as e:
                log_error(context, "Journey Plan", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Incident Report") and len(incidents) < count:
            inc = frappe.get_doc({
                "doctype": "Incident Report",
                "vehicle": veh if frappe.db.has_column("Incident Report", "vehicle") else None,
                "severity": random.choice(INCIDENT_TYPES) if frappe.db.has_column("Incident Report", "severity") else None,
            })
            try:
                if len(incidents) < count:
                    inc.insert(ignore_permissions=True, ignore_mandatory=True)
                    frappe.db.commit()
                    incidents.append(inc.name)
            except Exception as e:
                log_error(context, "Incident Report", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Risk Assessment") and len(risks) < count:
            risk = frappe.get_doc({
                "doctype": "Risk Assessment",
                "vehicle": veh if frappe.db.has_column("Risk Assessment", "vehicle") else None,
                "risk_score": random.randint(1, 25) if frappe.db.has_column("Risk Assessment", "risk_score") else None,
            })
            try:
                if len(risks) < count:
                    risk.insert(ignore_permissions=True, ignore_mandatory=True)
                    frappe.db.commit()
                    risks.append(risk.name)
            except Exception as e:
                log_error(context, "Risk Assessment", e)
                frappe.db.rollback()
        if spot_check_target and frappe.db.exists("DocType", "Spot Check") and len(spot_checks_ctx) < spot_check_target:
            sc_doc = frappe.get_doc({
                "doctype": "Spot Check",
                "vehicle": veh if frappe.db.has_column("Spot Check", "vehicle") else None,
                "inspection_time": now_datetime() if frappe.db.has_column("Spot Check", "inspection_time") else None,
                "notes": "Auto-generated demo spot check" if frappe.db.has_column("Spot Check", "notes") else None,
            })
            try:
                sc_doc.insert(ignore_permissions=True, ignore_mandatory=True)
                frappe.db.commit()
                spot_checks_ctx.append(sc_doc.name)
            except Exception as e:
                log_error(context, "Spot Check", e)
                frappe.db.rollback()
