import frappe
from frappe.utils import add_days, nowdate


def execute():
    _seed_policies()
    _seed_obligations()
    _seed_meetings()


def _seed_policies():
    if frappe.db.exists("Governance Policy", {"title": "Code of Conduct"}):
        return
    for i, title in enumerate([
        "Code of Conduct",
        "Driver Fatigue SOP",
        "Vehicle Maintenance Guideline",
        "Data Privacy Policy",
        "Incident Reporting SOP",
    ], start=1):
        doc = frappe.get_doc({
            "doctype": "Governance Policy",
            "title": title,
            "code": f"POL-{i:03d}",
            "effective_from": nowdate(),
            "review_cycle": "Annually",
            "next_review_date": add_days(nowdate(), 300),
            "status": "Active",
        })
        doc.insert(ignore_permissions=True)


def _seed_obligations():
    titles = [
        "Annual Vehicle License",
        "Road Worthiness Certificate",
        "Insurance Renewal",
        "Fire Safety Audit",
        "Environmental Compliance Check",
        "Tax Filing",
        "Data Protection Audit",
        "Medical Fitness Assessments",
        "Training Compliance",
        "Driving Permit Audit",
    ]
    for i, title in enumerate(titles, start=1):
        if frappe.db.exists("Compliance Obligation", {"title": title}):
            continue
        doc = frappe.get_doc({
            "doctype": "Compliance Obligation",
            "title": title,
            "code": f"OBL-{i:03d}",
            "regulator": "Regulatory Body",
            "due_frequency": "Annually",
            "next_due_date": add_days(nowdate(), 30 + i),
            "evidence_required": 1 if i % 2 == 0 else 0,
            "status": "Open",
        })
        doc.insert(ignore_permissions=True)


def _seed_meetings():
    if frappe.db.exists("Governance Meeting", {"meeting_date": ["between", [add_days(nowdate(), -1), add_days(nowdate(), 1)]]}):
        return
    doc = frappe.get_doc({
        "doctype": "Governance Meeting",
        "meeting_date": add_days(nowdate(), -2),
        "agenda": "Quarterly review",
        "decisions": "Proceed with fleet renewal plan.",
    })
    doc.append("action_items", {"action": "Draft fleet renewal proposal", "due_date": add_days(nowdate(), 14), "status": "Open"})
    doc.insert(ignore_permissions=True)
