from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate
from .seed_utils import ensure_min_records, log_error


def seed_documents(context, count: int = 20):
    vehicles = context.get("vehicles", [])
    compliance_docs = []
    signatures = []
    for i in range(count):
        if frappe.db.exists("DocType", "Compliance Document") and vehicles:
            cd = frappe.get_doc({
                "doctype": "Compliance Document",
                "vehicle": random.choice(vehicles) if frappe.db.has_column("Compliance Document", "vehicle") else None,
                "document_type": "Insurance" if frappe.db.has_column("Compliance Document", "document_type") else None,
                "issue_date": nowdate() if frappe.db.has_column("Compliance Document", "issue_date") else None,
            })
            try:
                cd.insert(ignore_permissions=True)
                compliance_docs.append(cd.name)
            except Exception as e:
                log_error(context, "Compliance Document", e)
                frappe.db.rollback()
        if frappe.db.exists("DocType", "Signature Log"):
            sl = frappe.get_doc({
                "doctype": "Signature Log",
                "signed_by": random.choice(context.get("employees", [])) if frappe.db.has_column("Signature Log", "signed_by") else None,
            })
            try:
                sl.insert(ignore_permissions=True)
                signatures.append(sl.name)
            except Exception as e:
                log_error(context, "Signature Log", e)
                frappe.db.rollback()
    context.setdefault("compliance_documents", []).extend([c for c in compliance_docs if c not in context.get("compliance_documents", [])])
    context.setdefault("signature_logs", []).extend([s for s in signatures if s not in context.get("signature_logs", [])])
