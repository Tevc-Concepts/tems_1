from __future__ import annotations
import frappe
from .seed_utils import ensure_min_records, log_error


def seed_kpis_and_subscriptions(context, count: int = 20):
    # KPI Config, Report Subscription if doctypes exist
    kpis = []
    subs = []
    if frappe.db.exists("DocType", "KPI Config"):
        for i in range(count):
            if len(kpis) >= count:
                break
            k = frappe.get_doc({
                "doctype": "KPI Config",
                "title": f"Vehicle Profit KPI {i+1}" if frappe.db.has_column("KPI Config", "title") else None,
            })
            try:
                k.insert(ignore_permissions=True, ignore_mandatory=True)
                kpis.append(k.name)
            except Exception as e:
                log_error(context, "KPI Config", e)
                frappe.db.rollback()
    if frappe.db.exists("DocType", "Report Subscription"):
        for i in range(count):
            if len(subs) >= count:
                break
            r = frappe.get_doc({
                "doctype": "Report Subscription",
                "report": None,
            })
            try:
                r.insert(ignore_permissions=True, ignore_mandatory=True)
                subs.append(r.name)
            except Exception as e:
                log_error(context, "Report Subscription", e)
                frappe.db.rollback()
    context.setdefault("kpi_configs", []).extend(kpis)
    context.setdefault("report_subscriptions", []).extend(subs)
