from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate, now_datetime, add_days
from .seed_utils import log_error, write_debug_json, log


def seed_governance_records(context, policy_target=20, obligation_target=20, goal_target=10, leadership_target=10, governance_target=10, audit_target=20):
    """Top-up governance doctypes individually to their targets with instrumentation."""
    debug_pre = {}
    targets_map = {
        "Governance Policy": policy_target,
        "Compliance Obligation": obligation_target,
        "Strategic Goal": goal_target,
        "Leadership Meeting": leadership_target,
        "Governance Meeting": governance_target,
        "Compliance Audit": audit_target,
    }
    for dt, tgt in targets_map.items():
        try:
            debug_pre[dt] = {"before": frappe.db.count(dt), "target": tgt}
        except Exception as e:  # noqa
            debug_pre[dt] = {"error": str(e), "target": tgt}
    write_debug_json("demo_dbg_governance_pre.json", {"phase": "pre", "data": debug_pre})
    owner_emp = None
    if frappe.db.exists("DocType", "Employee"):
        emps = frappe.get_all("Employee", pluck="name", limit=1)
        owner_emp = emps[0] if emps else None
    # Helper creators
    def create_policy(idx):
        gp = frappe.get_doc({
            "doctype": "Governance Policy",
            "title": f"Logistics Safety Policy {idx}",
            "code": f"POL-{idx:03d}",
            "category": "Policy",
            "effective_from": nowdate(),
            "status": "Active",
            "owner_employee": owner_emp,
            "review_cycle": "Annually",
            "next_review_date": add_days(nowdate(), 365),
        })
        gp.insert(ignore_permissions=True)
        return gp.name
    def create_obligation(idx):
        co = frappe.get_doc({
            "doctype": "Compliance Obligation",
            "title": f"Regulatory Filing {idx}",
            "code": f"OBL-{idx:03d}",
            "regulator": "Transport Agency",
            "due_frequency": "Quarterly",
            "status": "Open",
            "next_due_date": add_days(nowdate(), 90),
        })
        co.insert(ignore_permissions=True)
        return co.name
    def create_goal(idx):
        sg = frappe.get_doc({
            "doctype": "Strategic Goal",
            "code": f"SG-{idx:03d}",
            "title": f"Reduce Fleet Downtime {idx}",
            "description": "Strategic objective to optimize fleet utilization",
            "status": "Active",
            "owner_employee": owner_emp,
            "effective_from": nowdate(),
            "effective_to": add_days(nowdate(), 365),
        })
        sg.insert(ignore_permissions=True)
        return sg.name
    def create_leadership(idx):
        lm = frappe.get_doc({
            "doctype": "Leadership Meeting",
            "meeting_date": now_datetime(),
            "agenda": "Quarterly performance review",
            "decisions": "Proceed with maintenance optimization",
        })
        if hasattr(lm, "participants") and owner_emp:
            lm.append("participants", {"employee": owner_emp, "role": "Chair"})
        if hasattr(lm, "action_items") and owner_emp:
            lm.append("action_items", {"action": "Prepare cost reduction plan", "responsible_employee": owner_emp, "status": "Open"})
        lm.insert(ignore_permissions=True)
        return lm.name
    def create_governance_meeting(idx):
        gm = frappe.get_doc({
            "doctype": "Governance Meeting",
            "meeting_date": now_datetime(),
            "agenda": "Policy alignment and oversight",
            "decisions": "Approve new compliance framework",
        })
        if hasattr(gm, "participants") and owner_emp:
            gm.append("participants", {"employee": owner_emp, "role": "Secretary"})
        if hasattr(gm, "action_items") and owner_emp:
            gm.append("action_items", {"action": "Circulate approved framework", "responsible_employee": owner_emp, "status": "Open"})
        gm.insert(ignore_permissions=True)
        return gm.name
    def create_audit(idx):
        ca = frappe.get_doc({
            "doctype": "Compliance Audit",
            "audit_title": f"Audit {idx}",
        })
        ca.insert(ignore_permissions=True)
        return ca.name
    # Generic top-up helper
    def top_up(doctype, target, creator, context_key):
        if not frappe.db.exists("DocType", doctype):
            return
        existing = frappe.db.count(doctype)
        needed = target - existing
        if needed <= 0:
            return
        created = []
        for i in range(existing + 1, existing + needed + 1):
            try:
                nm = creator(i)
                created.append(nm)
            except Exception as e:
                log_error(context, doctype, e, capture_tb=True)
                frappe.db.rollback()
        context.setdefault(context_key, []).extend(created)
        if created:
            log(context, f"Governance top_up {doctype}: created {len(created)} (before={existing} target={target})")
        else:
            log(context, f"Governance top_up {doctype}: attempted none (existing={existing} target={target})")
    top_up("Governance Policy", policy_target, create_policy, "governance_policies")
    top_up("Compliance Obligation", obligation_target, create_obligation, "compliance_obligations")
    top_up("Strategic Goal", goal_target, create_goal, "strategic_goals")
    top_up("Leadership Meeting", leadership_target, create_leadership, "leadership_meetings")
    top_up("Governance Meeting", governance_target, create_governance_meeting, "governance_meetings")
    top_up("Compliance Audit", audit_target, create_audit, "compliance_audits")

    debug_post = {}
    for dt, tgt in targets_map.items():
        try:
            debug_post[dt] = {"after": frappe.db.count(dt), "target": tgt}
        except Exception as e:  # noqa
            debug_post[dt] = {"error": str(e), "target": tgt}
    write_debug_json("demo_dbg_governance_post.json", {"phase": "post", "data": debug_post})
