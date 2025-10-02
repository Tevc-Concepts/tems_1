"""Scheduled task stubs for TEMS Operations.
These are no-op implementations to satisfy hooks and avoid import errors.
"""
from __future__ import annotations

import frappe


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        # Fallback if frappe isn't fully initialized (e.g., during bench commands)
        print(f"[TEMS][Operations] {msg}")


def sync_vehicle_status() -> None:
    _log("operations.sync_vehicle_status noop")


def hourly_sync_checkpoint() -> None:
    _log("operations.hourly_sync_checkpoint noop")
    try:
        # Escalate overdue Control Exceptions
        overdue = frappe.get_all(
            "Control Exception",
            filters={"status": ["in", ["Open", "Acknowledged"]], "sla_breached": 1},
            fields=["name"],
        )
        for r in overdue:
            try:
                frappe.sendmail(
                    recipients=["Operations Manager"],
                    subject=f"Overdue Control Exception {r['name']}",
                    content=f"Control Exception {r['name']} breached SLA.",
                )
            except Exception:
                pass
    except Exception:
        pass


def check_vehicle_availability() -> None:
    _log("operations.check_vehicle_availability noop")


def daily_sync_checkpoint() -> None:
    _log("operations.daily_sync_checkpoint noop")


def generate_daily_operations_report() -> None:
    _log("operations.generate_daily_operations_report noop")


def validate_driver_vehicle_assignments() -> None:
    _log("operations.validate_driver_vehicle_assignments noop")


def weekly_sync_checkpoint() -> None:
    _log("operations.weekly_sync_checkpoint noop")


def monthly_sync_checkpoint() -> None:
    _log("operations.monthly_sync_checkpoint noop")
