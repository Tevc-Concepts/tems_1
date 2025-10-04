import frappe
from frappe import _


def validate_driver_competence(doc, method=None):
    """Lightweight validation: ensure driver is an Active Employee.

    TODO: Extend with Driver Qualification (license, medical, training) checks.
    """
    if not getattr(doc, "driver", None):
        return
    status = frappe.db.get_value("Employee", doc.driver, "status")  # type: ignore[assignment]
    if status and isinstance(status, str) and status.lower() not in {"active", "enabled"}:  # type: ignore[attr-defined]
        frappe.throw(_("Driver {0} is not active").format(doc.driver))

    # Extended rule: if a Driver Qualification exists and is expired, block Journey Plan
    dq_list = frappe.get_all(
        "Driver Qualification",
        filters={"employee": doc.driver},
        fields=["name", "expiry_date"],
        limit=1,
    )
    if dq_list:
        dq = dq_list[0]
        expiry = dq.get("expiry_date")
        if expiry:
            try:
                from frappe.utils import getdate, nowdate
                exp_date = getdate(str(expiry))  # type: ignore[assignment]
                today = getdate(nowdate())       # type: ignore[assignment]
                # Assert non-None for type checking
                assert exp_date is not None and today is not None
                if exp_date < today:
                    frappe.throw(_("Driver Qualification expired for {0}").format(doc.driver))
            except Exception:
                frappe.throw(_("Driver Qualification invalid for {0}").format(doc.driver))


def after_insert(doc, method=None):
    # Placeholder for post-insert logic such as scheduling tracking or notifications
    pass
