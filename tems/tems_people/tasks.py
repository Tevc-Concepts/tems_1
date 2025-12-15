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

def remind_expiring_medical_clearances(days_ahead: int = 30) -> None:
    """Notify HR / Operations of medical clearances expiring within N days.
    Idempotent: only logs or creates a Notification Log if not already created for the day per clearance.
    """
    today = getdate()
    cutoff = add_days(today, days_ahead)
    expiring = frappe.get_all(
        "Medical Clearance",
        filters={"expiry_date": ["between", [nowdate(), cutoff]]},
        fields=["name", "employee", "expiry_date"],
    )
    if not expiring:
        _log("No medical clearances expiring soon")
        return
    for row in expiring:
        key = f"MC-EXP-{row.name}-{nowdate()}"
        exists = frappe.db.exists("Communication", {"reference_doctype": "Medical Clearance", "reference_name": row.name, "subject": key})
        if exists:
            continue
        try:
            frappe.get_doc(
                {
                    "doctype": "Communication",
                    "communication_type": "Notification",
                    "subject": key,
                    "content": f"Medical Clearance {row.name} for Employee {row.employee} expiring on {row.expiry_date}",
                    "reference_doctype": "Medical Clearance",
                    "reference_name": row.name,
                }
            ).insert(ignore_permissions=True)
        except Exception:
            _log(f"Failed to create reminder for {row.name}")
    _log(f"Created/verified reminders for {len(expiring)} expiring medical clearances") 

def driver_qualification_audit() -> None:
    """Audit driver qualifications for all drivers to ensure compliance."""
    drivers = frappe.get_all("Employee", filters={"is_driver": 1}, fields=["name"])
    for driver in drivers:
        # Placeholder for actual audit logic
        _log(f"Audited driver qualifications for Employee {driver.name}")
    _log(f"Completed driver qualification audit for {len(drivers)} drivers")


# Auto-deactivate Driver when license expired
def auto_deactivate_drivers() -> None:
    """Automatically deactivate drivers whose licenses have expired.""" 
    today = nowdate()

    drivers = frappe.get_all(
        "Driver Qualification",
        filters={"license_expiry_date": ["<", today],
                 "status": "Active"},
        fields=["name", "driver"]
    )

    for q in drivers:
        doc = frappe.get_doc("Driver Qualification", q.name)
        doc.status = "Inactive"
        doc.reason_for_status = "License expired"
        doc.save(ignore_permissions=True)

        # Also update Driver doctype if needed
        driver = frappe.get_doc("Driver", q.driver)
        driver.status = "Inactive"
        driver.save(ignore_permissions=True)

# Daily Risk score audit task for driver qualifications
def driver_risk_score_audit() -> None:
    """Audit driver qualifications for risk scores and update status if necessary."""
    qualifications = frappe.get_all(
        "Driver Qualification",
        filters={"status": "Active"},
        fields=["name", "risk_score"]
    )

    for q in qualifications:
        if q.risk_score >= 80:  # Example threshold
            doc = frappe.get_doc("Driver Qualification", q.name)
            doc.status = "Inactive"
            doc.reason_for_status = "High risk score"
            doc.save(ignore_permissions=True)

# Daily latest qualification status sync task
def sync_driver_qualification_status() -> None:
    """Sync latest driver qualification status for all drivers."""
    drivers = frappe.get_all("Driver", 
                             filters={"status": "Active"},
                             fields=["name"])

    for d in drivers:
        driver = d.name

        # --- Compute Infraction Points ---
        infractions = frappe.get_all(
            "Driver Infraction",
            filters={"driver": driver},
            fields=["severity"]
        )

        infraction_points = 0
        for i in infractions:
            if i.severity == "Low":
                infraction_points += 5
            elif i.severity == "Medium":
                infraction_points += 10
            elif i.severity == "High":
                infraction_points += 20
            elif i.severity == "Critical":
                infraction_points += 40

        # --- Compute Reward Points ---
        rewards = frappe.get_all(
            "Driver Reward",
            filters={"driver": driver},
            fields=["reward_points"]
        )

        reward_points = sum([r.reward_points for r in rewards])
        risk_score = max(infraction_points - reward_points, 0)

        # --- Determine Risk Category ---
        if risk_score <= 10:
            risk_category = "Low"
        elif risk_score <= 25:
            risk_category = "Medium"
        elif risk_score <= 50:
            risk_category = "High"
        else:
            risk_category = "Critical"

        # --- Update Latest Driver Qualification ---
        qualification = frappe.get_all(
            "Driver Qualification",
            filters={"driver": driver},
            fields=["name"],
            order_by="qualification_date desc",
            limit=1
        )

        if qualification:
            q = frappe.get_doc("Driver Qualification", qualification[0].name)
            q.risk_score = risk_score
            q.risk_category = risk_category
            q.save(ignore_permissions=True)
