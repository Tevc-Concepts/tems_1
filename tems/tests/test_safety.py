import frappe
from frappe.utils import now_datetime

def test_journey_plan_minimum_insert():
    jp = frappe.get_doc({
        "doctype": "Journey Plan",
        "route": None,
        "driver": None,
        "vehicle": None,
        "start_time": now_datetime(),
    })
    jp.insert()
    assert jp.name

def test_safety_incident_insert():
    si = frappe.get_doc({
        "doctype": "Safety Incident",
        "title": "Test Incident",
        "incident_date": now_datetime(),
        "severity": "minor",
        "status": "Open"
    })
    si.insert()
    si.reload()
    assert getattr(si, "status", None) == "Open"
