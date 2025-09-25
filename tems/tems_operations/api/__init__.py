import frappe


@frappe.whitelist()
def compute_otp(from_date: str, to_date: str, route: str | None = None):
    """Stub for Operations OTP computation. To be implemented in Operations domain.

    Returns a dict with basic structure for now.
    """
    return {"from_date": from_date, "to_date": to_date, "route": route, "otp_percent": None}
