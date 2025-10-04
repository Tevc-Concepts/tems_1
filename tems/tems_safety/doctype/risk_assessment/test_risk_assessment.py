import frappe
from frappe.utils import nowdate

def test_risk_assessment_positive():
    ra = frappe.get_doc({
        "doctype": "Risk Assessment",
        "vehicle": None,
        "risk_score": 5,
        "assessment_date": nowdate()
    })
    ra.insert()
    assert ra.name
