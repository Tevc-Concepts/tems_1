"""Scheduled task stubs for TEMS Safety (no-op)."""
from __future__ import annotations

import frappe


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Safety] {msg}")


def aggregate_emissions_daily() -> None:
    _log("safety.aggregate_emissions_daily noop")


def aggregate_emissions_monthly() -> None:
    _log("safety.aggregate_emissions_monthly noop")

# from tems_safety.doctype.journey_plan.journey_plan updated status to expired when end time is passed
def update_journey_plan_status() -> None:
    from tems_safety.doctype.journey_plan.journey_plan import JourneyPlan

    now = frappe.utils.now_datetime()
    journey_plans = frappe.get_all(
        "Journey Plan",
        filters={"end_time": ("<", now), "status": "Active"},
        fields=["name"],
    )
    for plan in journey_plans:
        jp = frappe.get_doc("Journey Plan", plan.name)
        jp.status = "Expired"
        jp.save()
        _log(f"Updated Journey Plan {plan.name} to Expired")
