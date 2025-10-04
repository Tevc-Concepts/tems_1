"""Scheduled task stubs for TEMS Fleet (no-op)."""
from __future__ import annotations

import frappe
from frappe.utils import nowdate


def _log(msg: str) -> None:
    try:
        frappe.logger("tems").info(msg)
    except Exception:
        print(f"[TEMS][Fleet] {msg}")


def sync_asset_costs() -> None:
    _log("fleet.sync_asset_costs noop")


def compute_predictive_maintenance() -> None:
    """Identify assets approaching maintenance interval and create draft Work Orders.

    Threshold: 90% of maintenance_interval_hours; uses total_utilization_hours.
    """
    try:
        rows = frappe.get_all(
            "Asset",
            fields=["name", "maintenance_interval_hours", "total_utilization_hours"],
            filters=[["maintenance_interval_hours", ">", 0]],
        )
        for r in rows:
            interval = (r.get("maintenance_interval_hours") or 0) or 0
            used = (r.get("total_utilization_hours") or 0) or 0
            if interval == 0:
                continue
            if used / interval >= 0.9 and used / interval < 1.05:  # near due
                existing = frappe.get_all(
                    "Maintenance Work Order",
                    filters={"asset": r["name"], "status": ["in", ["Open", "In Progress"]]},
                    limit=1,
                )
                if not existing:
                    mwo = frappe.get_doc(
                        {
                            "doctype": "Maintenance Work Order",
                            "asset": r["name"],
                            "status": "Open",
                            "planned_date": nowdate(),
                        }
                    )
                    mwo.insert(ignore_permissions=True)
                    # Notification log
                    try:
                        frappe.get_doc(
                            {
                                "doctype": "Notification Log",
                                "subject": f"Maintenance due soon for Asset {r['name']}",
                                "email_content": f"Asset {r['name']} at {used}/{interval}h (>=90%). Work Order {mwo.name} created.",
                                "for_user": frappe.session.user if frappe.session.user else "Administrator",
                                "document_type": "Asset",
                                "document_name": r["name"],
                            }
                        ).insert(ignore_permissions=True)
                    except Exception:
                        pass
        frappe.db.commit()
        _log("fleet.compute_predictive_maintenance executed")
    except Exception as e:  # pragma: no cover
        _log(f"fleet.compute_predictive_maintenance error: {e}")
