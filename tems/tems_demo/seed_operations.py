from __future__ import annotations
import random
import frappe
from frappe.utils import now_datetime, add_to_date
from .seed_utils import ensure_min_records, log_error
try:
    from . import settings as demo_settings
except Exception:  # pragma: no cover
    demo_settings = None

STATES = ["Check-In", "In Transit", "Delivery Confirmation", "Delivered"]


def seed_operation_plans(context, target: int = 20):
    """Ensure at least `target` Operation Plans exist."""
    vehicles = context.get("vehicles", [])
    employees = context.get("employees", [])
    plans = context.setdefault("operation_plans", [])
    if not vehicles:
        return plans
    # Add existing
    if not plans:
        plans.extend(frappe.get_all("Operation Plan", pluck="name", limit=target))
    attempt = 0
    while len(plans) < target and attempt < target * 3:
        attempt += 1
        veh = random.choice(vehicles)
        drv = random.choice(employees) if employees else None
        doc = frappe.get_doc({
            "doctype": "Operation Plan",
            "title": f"Plan {len(plans)+1}",
            "vehicle": veh,
            "driver": drv,
            "start_time": now_datetime(),
        })
        try:
            doc.insert(ignore_permissions=True, ignore_mandatory=True)
            frappe.db.commit()
            plans.append(doc.name)
        except Exception as e:
            frappe.db.rollback()
            log_error(context, "Operation Plan", e)
            continue
    return plans


MAX_MOVEMENT_LOGS = getattr(demo_settings, 'CEILINGS', {}).get('Movement Log', 120) if demo_settings else 120

def seed_movement_logs(context, target: int = 100):
    """Generate movement logs across existing operation plans and vehicles with ceiling & pruning.

    If existing logs exceed MAX_MOVEMENT_LOGS, prune oldest surplus (soft delete via db delete)
    and then top-up only up to target (capped by MAX_MOVEMENT_LOGS).
    """
    vehicles = context.get("vehicles", [])
    plans = context.get("operation_plans", []) or frappe.get_all("Operation Plan", pluck="name", limit=20)
    logs = context.setdefault("movement_logs", [])
    if not vehicles or not plans:
        return logs
    # Sync logs cache if empty
    if not logs:
        logs.extend(frappe.get_all("Movement Log", pluck="name", limit=MAX_MOVEMENT_LOGS))
    # Prune if above ceiling
    existing_total = frappe.db.count("Movement Log") if frappe.db.exists("DocType", "Movement Log") else 0
    if existing_total > MAX_MOVEMENT_LOGS:
        surplus = existing_total - MAX_MOVEMENT_LOGS
        oldies = frappe.get_all("Movement Log", order_by="creation asc", pluck="name", limit=surplus)
        for nm in oldies:
            try:
                frappe.db.delete("Movement Log", nm)
            except Exception:
                frappe.db.rollback()
        frappe.db.commit()
        existing_total = frappe.db.count("Movement Log")
    # Adjust effective target respecting ceiling
    effective_target = min(target, MAX_MOVEMENT_LOGS)
    attempt = 0
    while len(logs) < effective_target and attempt < effective_target * 3:
        attempt += 1
        plan = random.choice(plans)
        veh = random.choice(vehicles)
        state = random.choice(STATES)
        mv = frappe.get_doc({
            "doctype": "Movement Log",
            "operation_plan": plan if frappe.db.has_column("Movement Log", "operation_plan") else None,
            "vehicle": veh,
            "state": state,
            "event_time": now_datetime(),
            "location_lat": random.uniform(-1, 1),
            "location_lng": random.uniform(-1, 1),
        })
        try:
            mv.insert(ignore_permissions=True, ignore_mandatory=True)
            frappe.db.commit()
            logs.append(mv.name)
        except Exception as e:
            frappe.db.rollback()
            log_error(context, "Movement Log", e)
            continue
    return logs


def seed_operation_plans_and_movements(context, count: int = 20, movement_multiplier: int = 5):
    # Backward compatibility wrapper now using dedicated helpers.
    seed_operation_plans(context, target=count)
    # movement target scaled
    # Cap requested movement target
    movement_target = min(count * movement_multiplier, MAX_MOVEMENT_LOGS)
    seed_movement_logs(context, target=movement_target)
