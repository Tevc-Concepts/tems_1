import frappe
from frappe.utils import now_datetime, add_to_date

def test_journey_plan_time_validation():
    jp = frappe.get_doc({
        "doctype": "Journey Plan",
        "route": None,
        "driver": None,
        "vehicle": None,
        "start_time": now_datetime(),
        "end_time": add_to_date(now_datetime(), hours=2)
    })
    jp.insert()
    assert jp.name
