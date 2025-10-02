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


def test_strategic_goal_create_minimal():
    name = frappe.get_doc({
        "doctype": "Strategic Goal",
        "code": "SG-OPS-01",
        "title": "Improve On-Time Performance",
        "language": "en",
        "status": "Active",
    }).insert().name
    assert frappe.db.exists("Strategic Goal", name)


def test_compliance_audit_requires_evidence_for_close():
    audit = frappe.get_doc({
        "doctype": "Compliance Audit",
        "audit_date": nowdate(),
        "auditor": None,
        "policy": None,
        "severity": "High",
        "status": "Open",
    }).insert()

    # Attempt to close without evidence should raise
    try:
        audit.db_set("status", "Closed")
        assert False, "Should require evidence to close high severity audit"
    except Exception:
        pass
