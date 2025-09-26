import frappe


@frappe.whitelist()
def validate_driver_active(employee: str) -> bool:
    """Return True if employee has a non-expired Driver Qualification with status Active."""
    dq = frappe.db.get_value(
        "Driver Qualification",
        {"employee": employee, "status": ["in", ["Active", "Verified"]]},
        ["expiry_date"],
        as_dict=False,
    )
    if not dq:
        return False
    expiry = dq
    if not expiry:
        return False
    return frappe.utils.getdate(expiry) >= frappe.utils.getdate()
