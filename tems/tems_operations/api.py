from __future__ import annotations

import frappe
from frappe.utils import getdate


@frappe.whitelist()
def compute_otp(from_date: str, to_date: str, route: str | None = None) -> dict:
    """Compute On-time Performance between dates optionally filtered by route.

    Returns { total: int, on_time: int, otp_percent: float }
    """
    filters = {"event_type": "Arrive", "event_time": ["between", [from_date, to_date]]}
    if route:
        filters["journey_reference"] = ["like", f"%{route}%"]

    events = frappe.get_all(
        "Operations Event",
        filters=filters,
        fields=["name", "variance_minutes"],
    )
    total = len(events)
    if total == 0:
        return {"total": 0, "on_time": 0, "otp_percent": 0.0}
    on_time = sum(1 for e in events if (e.get("variance_minutes") or 0) <= 5)
    otp = round(on_time * 100.0 / total, 2)
    return {"total": total, "on_time": on_time, "otp_percent": otp}
