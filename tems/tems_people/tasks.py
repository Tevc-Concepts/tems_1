"""Scheduled tasks for TEMS People domain."""
from __future__ import annotations

import frappe
from frappe.utils import nowdate, add_days, getdate


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][People] {msg}")


def remind_expiring_driver_docs(days_ahead: int = 30) -> None:
    """Notify HR / Operations of driver qualifications or medical clearance expiring within N days.
    Idempotent: only logs or creates a Notification Log if not already created for the day per driver.
    """
    today = getdate()
    cutoff = add_days(today, days_ahead)
    expiring = frappe.get_all(
        "Driver Qualification",
        filters={"expiry_date": ["between", [nowdate(), cutoff]]},
        fields=["name", "employee", "expiry_date"],
    )
    if not expiring:
        _log("No driver qualifications expiring soon")
        return
    for row in expiring:
        key = f"DQ-EXP-{row.name}-{nowdate()}"
        exists = frappe.db.exists("Communication", {"reference_doctype": "Driver Qualification", "reference_name": row.name, "subject": key})
        if exists:
            continue
        try:
            frappe.get_doc(
                {
                    "doctype": "Communication",
                    "communication_type": "Notification",
                    "subject": key,
                    "content": f"Driver Qualification {row.name} for Employee {row.employee} expiring on {row.expiry_date}",
                    "reference_doctype": "Driver Qualification",
                    "reference_name": row.name,
                }
            ).insert(ignore_permissions=True)
        except Exception:
            _log(f"Failed to create reminder for {row.name}")
    _log(f"Created/verified reminders for {len(expiring)} expiring driver qualifications")
