import frappe
from datetime import datetime, date
from typing import Any, Union
from frappe.utils import nowdate, getdate, get_datetime, now_datetime


def daily_sync_checkpoint():
    frappe.logger().info("TEMS.daily_sync_checkpoint ran")


def daily_interest_compute():
    frappe.logger().info("TEMS.daily_interest_compute ran")


def compute_nightly_jobs():
    frappe.logger().info("TEMS.compute_nightly_jobs ran")


def update_tariffs():
    frappe.logger().info("TEMS.update_tariffs (Trade) ran")


def rotate_rosca():
    frappe.logger().info("TEMS.rotate_rosca (Informal) ran")


def aggregate_emissions_daily():
    # stub aggregation; real logic can precompute summaries
    frappe.logger().info("TEMS.aggregate_emissions_daily (Climate) ran")

DateLike = Union[str, datetime, date]


def _safe_days_since(val: DateLike | None) -> int:
    try:
        dt = get_datetime(val) if val else None
        if not dt:
            return 0
        delta = now_datetime() - dt
        return getattr(delta, "days", 0) or 0
    except Exception:
        return 0


def notify_overdue_investigations():
    # Incidents 'Under Investigation' older than 7 days
    incidents = frappe.get_all(
        "Safety Incident",
        filters={"status": "Under Investigation"},
        fields=[
            "name",
            "incident_date",
            "severity",
            "target_resolution_date",
            "escalation_level",
            "escalated_on",
        ],
        order_by="incident_date asc",
    )
    if not incidents:
        return
    overdue = []
    for inc in incidents:
        try:
            trd = inc.get("target_resolution_date")
            base_date = trd or inc.get("incident_date") or nowdate()
            sev = (inc.get("severity") or "").lower()
            threshold_days = 3 if sev in ["critical"] else 7
            if _safe_days_since(base_date) > threshold_days:
                overdue.append(inc)
        except Exception:
            continue
    if not overdue:
        return
    # Notify Safety Officer role
    users = [d.parent for d in frappe.get_all("Has Role", filters={"role": "Safety Officer"}, fields=["parent"])]
    if not users:
        return
    msg = "\n".join([f"{d.get('name')} — {d.get('severity')} ({d.get('incident_date')})" for d in overdue])
    for user in users:
        try:
            frappe.sendmail(
                recipients=user,
                subject="Overdue Safety Investigations",
                message=f"The following incidents are overdue for closure:<br><pre>{msg}</pre>",
            )
        except Exception:
            continue

    # Escalations
    for inc in overdue:
        try:
            sev = (inc.get("severity") or "").lower()
            level = (inc.get("escalation_level") or "").strip()
            name = inc.get("name")
            # L1 for critical if not escalated yet
            if sev == "critical" and not level:
                frappe.db.set_value(
                    "Safety Incident",
                    name,
                    {"escalation_level": "L1", "escalated_on": get_datetime()},
                )
                continue

            # L2 if already L1 and still overdue by >3 days from escalation
            if level == "L1":
                if _safe_days_since(inc.get("escalated_on")) > 3:
                    frappe.db.set_value(
                        "Safety Incident",
                        name,
                        {"escalation_level": "L2", "escalated_on": get_datetime()},
                    )
                    # Notify Safety Manager and Operations Manager
                    roles = ["Safety Manager", "Operations Manager"]
                    role_users = set()
                    for r in roles:
                        role_users.update(
                            [d.parent for d in frappe.get_all("Has Role", filters={"role": r}, fields=["parent"])]
                        )
                    if role_users:
                        try:
                            frappe.sendmail(
                                recipients=list(role_users),
                                subject=f"L2 Escalation: Safety Incident {name}",
                                message=(
                                    f"Incident <b>{name}</b> remains overdue after L1. "
                                    f"It has been escalated to <b>L2</b>. Please prioritize resolution."
                                ),
                            )
                        except Exception:
                            pass
        except Exception:
            continue
