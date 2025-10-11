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
try:
    from . import settings as demo_settings
except Exception:  # pragma: no cover
    demo_settings = None
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
    # Capture pre-run counts for delta tracking
    pre_counts = {}
    tracked = [
        "Purchase Order", "Stock Entry", "Movement Log", "Governance Policy", "Compliance Obligation",
        "Strategic Goal", "Leadership Meeting", "Governance Meeting", "Asset", "Journey Plan"
    ]
    for dt in tracked:
        if frappe.db.exists("DocType", dt):
            try:
                pre_counts[dt] = frappe.db.count(dt)
            except Exception:
                pre_counts[dt] = None
    # Core masters
    targets_cfg = getattr(demo_settings, 'TARGETS', {}) if demo_settings else {}
    seed_core_items_suppliers(context, count=_top_up_db("Item", targets_cfg.get("Item", 25)) or 0)
    po_gap = _top_up_db("Purchase Order", targets_cfg.get("Purchase Order", 25))
    se_gap = _top_up_db("Stock Entry", targets_cfg.get("Stock Entry", 20))
    try:
        write_debug_json("demo_dbg_po_se_gaps.json", {"po_gap": po_gap, "se_gap": se_gap})
    except Exception:
        pass
    seed_purchase_and_stock(context, count=po_gap, stock_target=se_gap)
    # Assets (ensure at least 20)
    seed_assets(context, count=_top_up_db("Asset", targets_cfg.get("Asset", 20)) or 0)
    # Seed employees earlier than originally specified due to custom mandatory driver field on Vehicle
    seed_employees_and_qualifications(context, count=_top_up_db("Employee", targets_cfg.get("Employee", 30)) or 0, drivers=15)
    # Only add vehicles if below threshold
    v_add = _top_up_db("Vehicle", targets_cfg.get("Vehicle", 20))
    if v_add:
        seed_vehicles_and_attach_assets(context, count=v_add)
    seed_customers_and_orders(context)
    if _top_up_db("Operation Plan", targets_cfg.get("Operation Plan", 20)):
        seed_operation_plans_and_movements(context, count=_top_up_db("Operation Plan", targets_cfg.get("Operation Plan", 20)) or 0)
    if _top_up_db("Cost And Revenue Ledger", targets_cfg.get("Cost And Revenue Ledger", 40)):
        seed_costs_and_revenues(context, count=_top_up_db("Cost And Revenue Ledger", targets_cfg.get("Cost And Revenue Ledger", 40)) or 0)
    # Safety seeding: run if any safety-related target still not met (Journey Plan / Incident / Risk / Spot Check)
    if frappe.db.exists("DocType", "Journey Plan"):
        jp_gap = _top_up_db("Journey Plan", targets_cfg.get("Journey Plan", 20))
        spot_target = targets_cfg.get("Spot Check", 0)
        spot_current = _db_count("Spot Check") if frappe.db.exists("DocType", "Spot Check") else 0
        inc_gap = _top_up_db("Incident Report", targets_cfg.get("Incident Report", 20)) if frappe.db.exists("DocType", "Incident Report") else 0
        risk_gap = _top_up_db("Risk Assessment", targets_cfg.get("Risk Assessment", 20)) if frappe.db.exists("DocType", "Risk Assessment") else 0
        # Ensure context has vehicles/employees if existing in DB (for safety seeder loops)
        if not context.get("vehicles") and frappe.db.exists("DocType", "Vehicle"):
            context["vehicles"] = frappe.get_all("Vehicle", pluck="name", limit=targets_cfg.get("Vehicle", 50))
        if not context.get("employees") and frappe.db.exists("DocType", "Employee"):
            context["employees"] = frappe.get_all("Employee", pluck="name", limit=targets_cfg.get("Employee", 60))
        if jp_gap or (spot_target and spot_current < spot_target) or inc_gap or risk_gap:
            seed_safety_records(
                context,
                count=targets_cfg.get("Journey Plan", 20),  # pass absolute target; seeder checks existing
                spot_check_target=spot_target,
            )
    if frappe.db.exists("DocType", "Logistics Task") and _top_up_db("Logistics Task", targets_cfg.get("Logistics Task", 20)):
        seed_supply_chain_records(context, count=_top_up_db("Logistics Task", targets_cfg.get("Logistics Task", 20)) or 0)
    if frappe.db.exists("DocType", "Trade Compliance Log") and _top_up_db("Trade Compliance Log", targets_cfg.get("Trade Compliance Log", 20)):
        seed_trade_records(context, count=_top_up_db("Trade Compliance Log", targets_cfg.get("Trade Compliance Log", 20)) or 0)
    if frappe.db.exists("DocType", "Emission Log") and _top_up_db("Emission Log", targets_cfg.get("Emission Log", 20)):
        seed_climate_records(context, count=_top_up_db("Emission Log", targets_cfg.get("Emission Log", 20)) or 0)
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
    if frappe.db.exists("DocType", "Compliance Document") and _top_up_db("Compliance Document", targets_cfg.get("Compliance Document", 20)):
        seed_documents(context, count=_top_up_db("Compliance Document", targets_cfg.get("Compliance Document", 20)) or 0)
    if frappe.db.exists("DocType", "Informal Operator Profile") and _top_up_db("Informal Operator Profile", targets_cfg.get("Informal Operator Profile", 20)):
        seed_informal_records(context, count=_top_up_db("Informal Operator Profile", targets_cfg.get("Informal Operator Profile", 20)) or 0)
    if frappe.db.exists("DocType", "KPI Config") and _top_up_db("KPI Config", targets_cfg.get("KPI Config", 20)):
        seed_kpis_and_subscriptions(context, count=_top_up_db("KPI Config", targets_cfg.get("KPI Config", 20)) or 0)
    # Movement Log pruning & second pass using settings
    if frappe.db.exists("DocType", "Movement Log"):
        ceiling_ml = getattr(demo_settings, 'CEILINGS', {}).get('Movement Log', 120) if demo_settings else 120
        pruning_enabled = getattr(demo_settings, 'PRUNING', {}).get('enable_movement_log_prune', True) if demo_settings else True
        existing_movements = _db_count("Movement Log")
        if pruning_enabled and existing_movements > ceiling_ml:
            surplus = existing_movements - ceiling_ml
            oldies = frappe.get_all("Movement Log", order_by="creation asc", pluck="name", limit=surplus)
            for nm in oldies:
                try:
                    frappe.db.delete("Movement Log", nm)
                except Exception:
                    frappe.db.rollback()
            frappe.db.commit()
            existing_movements = _db_count("Movement Log")
        if existing_movements < ceiling_ml and _top_up_db("Operation Plan", targets_cfg.get("Operation Plan", 25)):
            seed_operation_plans_and_movements(context, count=_top_up_db("Operation Plan", targets_cfg.get("Operation Plan", 25)) or 0, movement_multiplier=3)

    frappe.db.commit()
    # Write errors if any
    write_error_file(context)
    _write_summary(context)
    # Truncate historic error log to recent 200 entries (keep file size manageable)
    try:
        path_err = frappe.get_site_path("demo_data_errors.md")
        if frappe.utils.file_manager.os.path.exists(path_err):  # type: ignore[attr-defined]
            with open(path_err, "r", encoding="utf-8") as fh:
                lines = fh.readlines()
            header = []
            body = []
            for ln in lines:
                if ln.startswith('- '):
                    body.append(ln)
                else:
                    header.append(ln)
            body = body[-200:]
            with open(path_err, "w", encoding="utf-8") as fh:
                fh.writelines(header + body)
    except Exception:
        pass

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
    # Context sync for visibility (populate if empty)
    for key, dt in [
        ("purchase_orders", "Purchase Order"),
        ("stock_entries", "Stock Entry"),
        ("movement_logs", "Movement Log"),
    ]:
        if not context.get(key) and frappe.db.exists("DocType", dt):
            context[key] = frappe.get_all(dt, pluck="name", limit=50)
    # Compute deltas
    deltas = {}
    for dt, before in pre_counts.items():
        if frappe.db.exists("DocType", dt):
            try:
                after = frappe.db.count(dt)
                if before is not None:
                    deltas[dt] = after - before
            except Exception:
                continue
    summary["deltas"] = deltas
    # Dashboard generation (markdown & html)
    try:
        _generate_dashboard(summary, deltas)
    except Exception:
        pass
    # STRICT MODE rebalancing (post-dashboard; may adjust integrity/deltas again)
    if demo_settings and getattr(demo_settings, 'STRICT_MODE', False):
        rules = getattr(demo_settings, 'REBALANCE_BEHAVIOR', {})
        backup_dir = getattr(demo_settings, 'BACKUP_DIR', 'demo_backups')
        _ensure_backup_dir(backup_dir)
        for dt, target in targets_cfg.items():
            if not frappe.db.exists("DocType", dt):
                continue
            # iterative passes until at/below target or no progress
            safety_pass = 0
            last_count = None
            while True:
                try:
                    current = frappe.db.count(dt)
                except Exception:
                    break
                if current <= target:
                    break
                remove_qty = current - target
                allow_cancel = rules.get(dt, {}).get("cancel_submitted", False)
                victims = frappe.get_all(
                    dt,
                    order_by="creation asc",
                    fields=["name", "docstatus", "modified"],
                    limit=min(remove_qty * 3, 500),
                )
                removed = 0
                for row in victims:
                    if removed >= remove_qty:
                        break
                    ds = row.get("docstatus", 0)
                    if ds == 1 and not allow_cancel:
                        continue
                    try:
                        doc = frappe.get_doc(dt, row["name"])
                        _backup_doc_minimal(doc, backup_dir)
                        if ds == 1 and allow_cancel:
                            doc.cancel()
                        doc.delete(ignore_permissions=True)
                        removed += 1
                    except Exception:
                        frappe.db.rollback()
                if removed:
                    frappe.db.commit()
                    integrity[dt] = frappe.db.count(dt)
                    if "_rebalance" not in summary or not isinstance(summary.get("_rebalance"), dict):
                        summary["_rebalance"] = {}
                    rb = summary["_rebalance"]  # type: ignore[assignment]
                    if dt not in rb:  # type: ignore[operator]
                        rb[dt] = {"removed": 0, "post": None}  # type: ignore[index]
                    rb[dt]["removed"] += removed  # type: ignore[index]
                    rb[dt]["post"] = integrity[dt]  # type: ignore[index]
                    last_count = integrity[dt]
                else:
                    # No removals possible (likely only submitted docs and cancel not allowed)
                    break
                # Safety guard against runaway loop
                safety_pass += 1
                if safety_pass > 10:  # guard against runaway loop
                    break
        # Regenerate dashboard + JSON to reflect rebalanced state
        try:
            _generate_dashboard(summary, deltas)
        except Exception:
            pass
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


def _generate_dashboard(summary: dict, deltas: dict):
    try:
        from . import settings as demo_settings  # type: ignore
    except Exception:  # pragma: no cover
        demo_settings = None
    targets = getattr(demo_settings, 'TARGETS', {}) if demo_settings else {}
    ceilings = getattr(demo_settings, 'CEILINGS', {}) if demo_settings else {}
    integrity = summary.get('integrity_counts', {})
    rows = []
    for dt, current in sorted(integrity.items()):
        if isinstance(current, (int, float)):
            tgt = targets.get(dt)
            cap = ceilings.get(dt)
            delta = deltas.get(dt)
            status = []
            if tgt is not None:
                if current < tgt:
                    status.append('BELOW')
                elif current == tgt:
                    status.append('TARGET')
                else:
                    status.append('ABOVE')
            if cap is not None and current > cap:
                status.append('>CAP')
            rows.append({
                'doctype': dt,
                'current': current,
                'target': tgt,
                'cap': cap,
                'delta': delta,
                'status': ','.join(status) if status else ''
            })
    # Markdown
    md_lines = ["# TEMS Demo Dashboard", "", "| Doctype | Current | Target | Cap | Delta | Status |", "|---------|---------|--------|-----|-------|--------|"]
    for r in rows:
        md_lines.append(f"| {r['doctype']} | {r['current']} | {r.get('target','')} | {r.get('cap','')} | {r.get('delta','')} | {r['status']} |")
    md_path = frappe.get_site_path(getattr(demo_settings, 'DASHBOARD_MD', 'demo_dashboard.md') if demo_settings else 'demo_dashboard.md')
    with open(md_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(md_lines))
    # HTML
    html_rows = ''.join([f"<tr><td>{r['doctype']}</td><td>{r['current']}</td><td>{r.get('target','')}</td><td>{r.get('cap','')}</td><td>{r.get('delta','')}</td><td>{r['status']}</td></tr>" for r in rows])
    html_doc = f"<html><head><title>TEMS Demo Dashboard</title></head><body><h1>TEMS Demo Dashboard</h1><table border='1' cellpadding='4' cellspacing='0'><thead><tr><th>Doctype</th><th>Current</th><th>Target</th><th>Cap</th><th>Delta</th><th>Status</th></tr></thead><tbody>{html_rows}</tbody></table></body></html>"
    html_path = frappe.get_site_path(getattr(demo_settings, 'DASHBOARD_HTML', 'demo_dashboard.html') if demo_settings else 'demo_dashboard.html')
    with open(html_path, 'w', encoding='utf-8') as fh:
        fh.write(html_doc)
    # JSON export
    try:
        json_path = frappe.get_site_path('demo_dashboard.json')
        import json
        with open(json_path, 'w', encoding='utf-8') as fh:
            json.dump(rows, fh, default=str, indent=2)
    except Exception:
        pass


def _ensure_backup_dir(backup_dir: str):
    try:
        import os
        path = frappe.get_site_path(backup_dir)
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass


def _backup_doc_minimal(doc, backup_dir: str):
    """Append a minimal JSON line backup for a doc before deletion/cancel."""
    try:
        import json, os
        path = frappe.get_site_path(backup_dir, f"{doc.doctype}.jsonl")
        payload = {
            "doctype": doc.doctype,
            "name": doc.name,
            "docstatus": doc.docstatus,
            "creation": getattr(doc, 'creation', None),
            "modified": getattr(doc, 'modified', None),
        }
        with open(path, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(payload, default=str) + "\n")
    except Exception:
        pass
