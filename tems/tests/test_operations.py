import frappe
from frappe.utils import now_datetime, nowdate


def test_compute_otp_smoke():
    # Insert sample events
    for vmin in [0, 3, 12]:
        doc = frappe.get_doc({
            "doctype": "Operations Event",
            "event_time": now_datetime(),
            "event_type": "Arrive",
            "variance_minutes": vmin,
        })
        doc.insert(ignore_permissions=True)

    res = frappe.call("tems.tems_operations.api.compute_otp", from_date=nowdate(), to_date=nowdate())
    assert "otp_percent" in res
    assert res["total"] >= 3


def test_compute_otp_edge_zero_total():
    res = frappe.call("tems.tems_operations.api.compute_otp", from_date="2099-01-01", to_date="2099-01-02")
    assert res["total"] == 0
    assert res["otp_percent"] == 0.0


def test_sos_event_publish_smoke():
    # Just ensure insert doesn't error and handler path exists
    doc = frappe.get_doc({
        "doctype": "SOS Event",
        "status": "Open",
    })
    doc.insert(ignore_permissions=True)
