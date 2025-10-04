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


def after_insert(doc, method=None):
    # Placeholder for post-insert logic such as scheduling tracking or notifications
    pass
