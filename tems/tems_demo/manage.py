"""Management utilities for demo data (bench execute entrypoints).

Example:
  bench --site tems.local execute "tems.tems.tems_demo.manage.reset_domains" --kwargs '{"domains":["safety"],"confirm":1}'
"""
from __future__ import annotations
import frappe

DOMAIN_MAP = {
    "safety": ["Journey Plan", "Incident Report", "Risk Assessment", "Spot Check"],
    "governance": ["Governance Policy", "Compliance Obligation", "Strategic Goal", "Leadership Meeting", "Governance Meeting", "Compliance Audit"],
    "informal": ["Informal Operator Profile"],
    "insights": ["KPI Config", "Report Subscription"],
    "operations": ["Operation Plan", "Movement Log"],
    "finance": ["Cost And Revenue Ledger"],
}

def _cancel_and_delete(name: str, doctype: str):
    doc = frappe.get_doc(doctype, name)
    if getattr(doc, "docstatus", 0) == 1:
        try:
            doc.cancel()
        except Exception:
            frappe.db.rollback()
            return False
    try:
        doc.delete(ignore_permissions=True)
        return True
    except Exception:
        frappe.db.rollback()
        return False

def reset_domains(domains: list[str] | None = None, confirm: int = 0):
    if not confirm:
        return {"error": "Pass confirm=1 to proceed."}
    domains = domains or []
    summary = {}
    for dom in domains:
        doctypes = DOMAIN_MAP.get(dom, [])
        deleted = 0
        for dt in doctypes:
            if not frappe.db.exists("DocType", dt):
                continue
            names = frappe.get_all(dt, pluck="name")
            for nm in names:
                if _cancel_and_delete(nm, dt):
                    deleted += 1
        summary[dom] = deleted
    frappe.db.commit()
    return {"reset": summary}