"""High-level orchestration for TEMS demo dataset generation.

Sequence strictly follows DemoDataAgent specification to ensure
referential integrity and realistic lifecycle progression.
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import now_datetime

from .seed_core import seed_core_items_suppliers, seed_purchase_and_stock, seed_assets, ensure_infrastructure
from .seed_utils import summarize_missing, write_error_file, write_debug_json
from .seed_fleet import seed_vehicles_and_attach_assets, seed_maintenance
from .seed_people import seed_employees_and_qualifications
from .seed_crm import seed_customers_and_orders
from .seed_operations import seed_operation_plans_and_movements
from .seed_finance import seed_costs_and_revenues
from .seed_safety import seed_safety_records
from .seed_supply_chain import seed_supply_chain_records
from .seed_trade import seed_trade_records
from .seed_climate import seed_climate_records
from .seed_governance import seed_governance_records
from .seed_documents import seed_documents
from .seed_informal import seed_informal_records
from .seed_insights import seed_kpis_and_subscriptions


def _ensure_company(context):
    existing = frappe.get_all("Company", pluck="name", limit=1)
    if existing:
        context["company"] = existing[0]
        return
    # Create only if truly absent
    try:
        company = frappe.get_doc({
            "doctype": "Company",
            "company_name": "Demo Logistics Ltd",
            "abbr": "DML",
            "default_currency": "USD"
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        context["company"] = company.name
    except Exception:
        frappe.db.rollback()
        # Fallback to any company now present (race condition or parallel)
        existing = frappe.get_all("Company", pluck="name", limit=1)
        if existing:
            context["company"] = existing[0]


def _db_count(doctype: str) -> int:
    if frappe.db.exists("DocType", doctype):
        try:
            return frappe.db.count(doctype)
        except Exception:
            return 0
    return 0


def _top_up_db(doctype: str, target: int) -> int:
    """Return how many to create based on authoritative DB count for doctype."""
    existing = _db_count(doctype)
    return 0 if existing >= target else target - existing


def run_all(site: str | None = None):
    """Entry point used via bench execute.

    Example:
        bench --site tems.local execute "tems.tems.tems_demo.orchestrator.run_all"
    """
    context: dict[str, list[str] | str] = {}
    _ensure_company(context)
    context["started_at"] = str(now_datetime())

    frappe.logger().info("[TEMS DEMO] Start full seeding sequence")

    ensure_infrastructure(context)
    # Core masters
    seed_core_items_suppliers(context, count=_top_up_db("Item", 25) or 0)
    po_gap = _top_up_db("Purchase Order", 25)
    se_gap = _top_up_db("Stock Entry", 20)
    try:
        write_debug_json("demo_dbg_po_se_gaps.json", {"po_gap": po_gap, "se_gap": se_gap})
    except Exception:
        pass
    seed_purchase_and_stock(context, count=po_gap, stock_target=se_gap)
    # Assets (ensure at least 20)
    seed_assets(context, count=_top_up_db("Asset", 20) or 0)
    # Seed employees earlier than originally specified due to custom mandatory driver field on Vehicle
    seed_employees_and_qualifications(context, count=_top_up_db("Employee", 30) or 0, drivers=15)
    # Only add vehicles if below threshold
    v_add = _top_up_db("Vehicle", 20)
    if v_add:
        seed_vehicles_and_attach_assets(context, count=v_add)
    seed_customers_and_orders(context)
    if _top_up_db("Operation Plan", 20):
        seed_operation_plans_and_movements(context, count=_top_up_db("Operation Plan", 20) or 0)
    if _top_up_db("Cost And Revenue Ledger", 40):
        seed_costs_and_revenues(context, count=_top_up_db("Cost And Revenue Ledger", 40) or 0)
    if frappe.db.exists("DocType", "Journey Plan") and _top_up_db("Journey Plan", 20):
        seed_safety_records(context, count=_top_up_db("Journey Plan", 20) or 0)
    if frappe.db.exists("DocType", "Logistics Task") and _top_up_db("Logistics Task", 20):
        seed_supply_chain_records(context, count=_top_up_db("Logistics Task", 20) or 0)
    if frappe.db.exists("DocType", "Trade Compliance Log") and _top_up_db("Trade Compliance Log", 20):
        seed_trade_records(context, count=_top_up_db("Trade Compliance Log", 20) or 0)
    if frappe.db.exists("DocType", "Emission Log") and _top_up_db("Emission Log", 20):
        seed_climate_records(context, count=_top_up_db("Emission Log", 20) or 0)
    # Governance: always attempt (instrumentation inside seeder will capture counts)
    try:
        pre_gov = {}
        for dt in ["Governance Policy", "Compliance Obligation", "Strategic Goal", "Leadership Meeting", "Governance Meeting", "Compliance Audit"]:
            if frappe.db.exists("DocType", dt):
                pre_gov[dt] = frappe.db.count(dt)
            else:
                pre_gov[dt] = "missing"
        write_debug_json("demo_dbg_governance_orchestrator_pre.json", pre_gov)
    except Exception:
        pass
    seed_governance_records(context)
    if frappe.db.exists("DocType", "Compliance Document") and _top_up_db("Compliance Document", 20):
        seed_documents(context, count=_top_up_db("Compliance Document", 20) or 0)
    if frappe.db.exists("DocType", "Informal Operator Profile") and _top_up_db("Informal Operator Profile", 20):
        seed_informal_records(context, count=_top_up_db("Informal Operator Profile", 20) or 0)
    if frappe.db.exists("DocType", "KPI Config") and _top_up_db("KPI Config", 20):
        seed_kpis_and_subscriptions(context, count=_top_up_db("KPI Config", 20) or 0)
    # Re-run operations enrichment to push counts up (after other links maybe created)
    # Second pass operations enrichment only if we still have fewer than 120 movement logs (avoid runaway)
    if frappe.db.exists("DocType", "Movement Log"):
        existing_movements = _db_count("Movement Log")
        if existing_movements < 120 and _top_up_db("Operation Plan", 25):
            seed_operation_plans_and_movements(context, count=_top_up_db("Operation Plan", 25) or 0, movement_multiplier=4)

    frappe.db.commit()
    # Write errors if any
    write_error_file(context)
    _write_summary(context)
    frappe.logger().info("[TEMS DEMO] Completed seeding.")
    summary: dict[str, object] = {}
    for k, v in context.items():
        if k in {"company", "started_at", "_missing_doctypes"}:
            continue
        summary[k] = len(v) if isinstance(v, list) else v
    # Integrity counts (DB authoritative)
    expected_doctypes = [
        "Item", "Supplier", "Purchase Order", "Asset", "Vehicle", "Employee", "Driver Qualification",
        "Customer", "Operation Plan", "Movement Log", "Cost And Revenue Ledger", "Journey Plan",
        "Incident Report", "Risk Assessment", "Compliance Audit", "Governance Policy", "Compliance Obligation",
        "Leadership Meeting", "Governance Meeting", "Strategic Goal", "Spot Check", "Supplier Rating",
        "Logistics Task", "Border Crossing", "Emission Log", "Compliance Document", "Informal Operator Profile",
        "Trip Match", "Savings Group", "KPI Config", "Report Subscription"
    ]
    integrity = {}
    for dt in expected_doctypes:
        if frappe.db.exists("DocType", dt):
            try:
                integrity[dt] = frappe.db.count(dt)
            except Exception:
                integrity[dt] = "error"
        else:
            integrity[dt] = "missing"
    summary["integrity_counts"] = integrity
    summary["missing_doctypes"] = summarize_missing(context)
    if context.get("_errors"):
        summary["error_count"] = len(context["_errors"])
    return summary


def run_fleet_only():
    """Helper for debugging just employees + vehicles + maintenance."""
    context: dict[str, object] = {}
    _ensure_company(context)
    ensure_infrastructure(context)
    seed_employees_and_qualifications(context, count=8, drivers=5)
    seed_vehicles_and_attach_assets(context, count=5)
    seed_maintenance(context, count=5)
    frappe.db.commit()
    return {k: len(v) if isinstance(v, list) else v for k, v in context.items()}


def run_minimal():
    """Lightweight dataset for quick CI smoke (creates a handful only)."""
    # Use a relaxed typing container
    context: dict[str, object] = {"minimal": True}
    _ensure_company(context)
    seed_core_items_suppliers(context, count=3)
    seed_purchase_and_stock(context, count=3)
    seed_assets(context, count=3)
    seed_vehicles_and_attach_assets(context, count=2)
    seed_employees_and_qualifications(context, count=5, drivers=3)
    frappe.db.commit()
    _write_summary(context, filename="demo_data_summary_minimal.md")
    return context


def _write_summary(context, filename: str = "demo_data_summary.md"):
    lines = ["# TEMS Demo Data Summary", "", f"Generated: {now_datetime()}", ""]
    for k, v in sorted(context.items()):
        if isinstance(v, list):
            lines.append(f"- {k}: {len(v)}")
    path = frappe.get_site_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
