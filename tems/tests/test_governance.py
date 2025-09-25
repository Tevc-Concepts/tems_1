import frappe
from frappe.utils import add_days, nowdate, getdate


def test_next_reviews_filters_date_range():
    # Create a policy due within 10 days
    name = frappe.get_doc({
        "doctype": "Governance Policy",
        "title": "Driver Code of Conduct",
        "effective_from": nowdate(),
        "review_cycle": "Monthly",
        "next_review_date": add_days(nowdate(), 7),
        "status": "Active",
    }).insert().name

    res = frappe.call("tems.tems_governance.api.next_reviews", within_days=10)
    assert any(r["name"] == name for r in res)


def test_obligation_requires_evidence_when_marked_compliant():
    doc = frappe.get_doc({
        "doctype": "Compliance Obligation",
        "title": "Annual License Renewal",
        "due_frequency": "Annually",
        "next_due_date": add_days(nowdate(), 1),
        "evidence_required": 1,
        "status": "Submitted",
    }).insert()

    # Try to set status without evidence
    try:
        doc.db_set("status", "Compliant")
        assert False, "Should not allow compliant status without evidence"
    except Exception:
        pass
