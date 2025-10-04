import frappe
from frappe.utils import now_datetime

def test_incident_report_insert():
    ir = frappe.get_doc({
        "doctype": "Incident Report",
        "vehicle": None,
        "description": "Test incident",
        "incident_date": now_datetime()
    })
    ir.insert()
    assert ir.name
