"""Seed rich connected demo data for the TEMS app.

Run with:
    bench --site tems.local execute tems.tems_demo.seed_demo_data.run

The script is designed to be idempotent: it will skip creating a record
if a deterministic name already exists. It follows the business flow
outlined in `doc/agents/DemoDataAgent.md`.

NOTE: Some listed doctypes in the DemoDataAgent brief may not yet exist
in the codebase. These will be reported as *missing* and skipped so the
script can still complete without failing the whole run.
"""
from __future__ import annotations

import random
import string
from datetime import datetime, timedelta, date
from typing import Dict, List, Iterable, Optional

import frappe
from frappe import _
from frappe.utils import now_datetime, nowdate, add_days


LOGGER = frappe.logger("tems_demo")


# --------------------------- Utility Helpers --------------------------- #

def _exists(doctype: str, name: str) -> bool:
    return bool(frappe.db.exists(doctype, name))


def _doctype_available(doctype: str) -> bool:
    try:
        frappe.get_meta(doctype)
        return True
    except Exception:
        return False


def _random_code(prefix: str, length: int = 6) -> str:
    return f"{prefix}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=length))}"


def _commit_every(batch_size: int, counter: int):
    if counter % batch_size == 0:
        frappe.db.commit()


def _safe_insert(doc_dict: dict, unique_fields: Iterable[str] | None = None):
    """Insert document if not already existing by unique_fields (or name if given).

    Args:
        doc_dict: Document payload
        unique_fields: tuple/list of fields whose values form a deterministic key
    Returns: (doc, created: bool)
    """
    doctype = doc_dict.get("doctype")
    if not _doctype_available(doctype):  # skip silently, log once
        LOGGER.warning(f"[SKIP] Doctype missing: {doctype}")
        return None, False

    # Determine key
    if unique_fields:
        filters = {f: doc_dict.get(f) for f in unique_fields}
        existing_name = frappe.db.get_value(doctype, filters, "name")
        if existing_name:
            return frappe.get_doc(doctype, existing_name), False
    elif doc_dict.get("name") and frappe.db.exists(doctype, doc_dict["name"]):
        return frappe.get_doc(doctype, doc_dict["name"]), False

    doc = frappe.get_doc(doc_dict)
    try:
        doc.insert(ignore_permissions=True)
        return doc, True
    except Exception as e:  # log & return
        LOGGER.error(f"Failed to insert {doctype}: {e}")
        frappe.log_error(title=f"TEMS Demo Seed Insert Failure: {doctype}")
        return None, False


# --------------------------- Seeding Steps ----------------------------- #

def seed_suppliers(n: int = 10) -> List[str]:
    names = []
    for i in range(1, n + 1):
        supplier_name = f"Demo Supplier {i:02d}"
        doc, created = _safe_insert({
            "doctype": "Supplier",
            "supplier_name": supplier_name,
            "supplier_group": "All Supplier Groups" if frappe.db.exists("Supplier Group", "All Supplier Groups") else None,
            "supplier_type": "Company",
        }, unique_fields=["supplier_name"])
        if doc:
            names.append(doc.name)
    return names


def seed_customers(n: int = 20) -> List[str]:
    names = []
    for i in range(1, n + 1):
        customer_name = f"Demo Customer {i:02d}"
        doc, created = _safe_insert({
            "doctype": "Customer",
            "customer_name": customer_name,
            "customer_group": "All Customer Groups" if frappe.db.exists("Customer Group", "All Customer Groups") else None,
            "territory": "All Territories" if frappe.db.exists("Territory", "All Territories") else None,
        }, unique_fields=["customer_name"])
        if doc:
            names.append(doc.name)
    return names


def seed_items(n: int = 25) -> List[str]:
    # Ensure an Item Group exists
    if not frappe.db.exists("Item Group", "All Item Groups"):
        _safe_insert({"doctype": "Item Group", "item_group_name": "All Item Groups", "is_group": 1})
    names = []
    for i in range(1, n + 1):
        item_code = f"SPARE-{i:03d}"
        doc, created = _safe_insert({
            "doctype": "Item",
            "item_code": item_code,
            "item_name": f"Spare Part {i:03d}",
            "item_group": "All Item Groups",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "description": f"Demo spare part {i:03d} for fleet maintenance"
        }, unique_fields=["item_code"])
        if doc:
            names.append(doc.name)
    return names


def ensure_warehouse() -> str:
    wh_name = "Main Stores - TEMS"
    if not frappe.db.exists("Warehouse", wh_name):
        parent = frappe.db.exists("Warehouse", {"is_group": 1}) or None
        _safe_insert({
            "doctype": "Warehouse",
            "warehouse_name": wh_name.split(" - ")[0],
            "company": frappe.defaults.get_defaults().get("company") or "TEMS Demo Company",
            "is_group": 0,
        }, unique_fields=["warehouse_name"])
    return wh_name


def seed_purchase_orders(items: List[str], suppliers: List[str], target: int = 20) -> List[str]:
    po_names = []
    if not _doctype_available("Purchase Order"):
        return po_names
    schedule_date = add_days(nowdate(), 1)
    for i in range(1, target + 1):
        supplier = random.choice(suppliers)
        po_name = f"DEMO-PO-{i:04d}"
        if frappe.db.exists("Purchase Order", po_name):
            po_names.append(po_name)
            continue
        line_items = []
        for _ in range(random.randint(1, 3)):
            item_code = random.choice(items)
            line_items.append({
                "item_code": item_code,
                "qty": random.randint(1, 10),
                "schedule_date": schedule_date,
                "rate": random.randint(50, 500),
            })
        doc = frappe.get_doc({
            "doctype": "Purchase Order",
            "name": po_name,
            "supplier": supplier,
            "transaction_date": nowdate(),
            "schedule_date": schedule_date,
            "items": line_items,
        })
        try:
            doc.insert(ignore_permissions=True)
            if hasattr(doc, "submit"):
                doc.submit()
            po_names.append(doc.name)
        except Exception as e:
            LOGGER.error(f"Failed PO {po_name}: {e}")
    return po_names


def seed_stock_entries(items: List[str], warehouse: str, target: int = 20) -> List[str]:
    se_names = []
    if not _doctype_available("Stock Entry"):
        return se_names
    for i in range(1, target + 1):
        name = f"DEMO-STOCK-{i:04d}"
        if frappe.db.exists("Stock Entry", name):
            se_names.append(name)
            continue
        doc = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "posting_date": nowdate(),
            "items": [
                {
                    "item_code": random.choice(items),
                    "t_warehouse": warehouse,
                    "qty": random.randint(1, 5),
                    "uom": "Nos",
                    "conversion_factor": 1,
                    "basic_rate": random.randint(40, 400),
                }
                for _ in range(random.randint(1, 3))
            ],
        })
        try:
            doc.insert(ignore_permissions=True)
            se_names.append(doc.name)
        except Exception as e:
            LOGGER.error(f"Failed Stock Entry {name}: {e}")
    return se_names


def seed_assets(items: List[str], target: int = 25) -> List[str]:
    asset_names = []
    if not _doctype_available("Asset"):
        return asset_names
    for i in range(1, target + 1):
        item_code = random.choice(items)
        asset_name = f"DEMO-ASSET-{i:04d}"
        if frappe.db.exists("Asset", asset_name):
            asset_names.append(asset_name)
            continue
        # Minimal Asset creation (ERPNext expects purchase details; use broad defaults)
        purchase_date = nowdate()
        doc = frappe.get_doc({
            "doctype": "Asset",
            "asset_name": asset_name,
            "item_code": item_code,
            "location": "Main Yard",
            "purchase_date": purchase_date,
            "available_for_use_date": purchase_date,
            "gross_purchase_amount": random.randint(100, 2000),
            "company": frappe.defaults.get_defaults().get("company") or "TEMS Demo Company",
        })
        try:
            doc.insert(ignore_permissions=True)
            asset_names.append(doc.name)
        except Exception as e:
            LOGGER.error(f"Failed Asset {asset_name}: {e}")
    return asset_names


def seed_vehicles(target: int = 10) -> List[str]:
    veh_names = []
    if not _doctype_available("Vehicle"):
        return veh_names
    for i in range(1, target + 1):
        name = f"DEMO-VH-{i:03d}"
        if frappe.db.exists("Vehicle", name):
            veh_names.append(name)
            continue
        doc = frappe.get_doc({
            "doctype": "Vehicle",
            "name": name,
            "license_plate": f"KJA-{random.randint(1000,9999)}",
            "make": random.choice(["Volvo", "Scania", "MAN", "Mercedes"]),
            "model": random.choice(["FH", "R500", "TGS", "Actros"]),
            "chassis_no": _random_code("VIN", 10),
        })
        try:
            doc.insert(ignore_permissions=True)
            veh_names.append(doc.name)
        except Exception as e:
            LOGGER.error(f"Failed Vehicle {name}: {e}")
    return veh_names


def seed_employees(drivers: int = 20, others: int = 10) -> List[str]:
    emp_names = []
    if not _doctype_available("Employee"):
        return emp_names
    total = drivers + others
    for i in range(1, total + 1):
        name = f"DEMO-EMP-{i:03d}"
        if frappe.db.exists("Employee", name):
            emp_names.append(name)
            continue
        is_driver = i <= drivers
        doc = frappe.get_doc({
            "doctype": "Employee",
            "name": name,
            "first_name": f"Emp{i:03d}",
            "employee_name": f"Demo Employee {i:03d}",
            "status": "Active",
            "date_of_joining": nowdate(),
            "designation": "Driver" if is_driver else "Operations Officer",
        })
        try:
            doc.insert(ignore_permissions=True)
            emp_names.append(doc.name)
        except Exception as e:
            LOGGER.error(f"Failed Employee {name}: {e}")
    return emp_names


def seed_driver_qualifications(employees: List[str], vehicles: List[str]):
    if not _doctype_available("Driver Qualification"):
        return []
    dq = []
    drivers = [e for e in employees if frappe.get_value("Employee", e, "designation") == "Driver"]
    for emp in drivers:
        vehicle = random.choice(vehicles) if vehicles else None
        license_no = _random_code("LIC", 8)
        doc, created = _safe_insert({
            "doctype": "Driver Qualification",
            "employee": emp,
            "license_number": license_no,
            "expiry_date": (date.today() + timedelta(days=random.randint(30, 720))).isoformat(),
            "assigned_vehicle": vehicle,
        }, unique_fields=["employee"])
        if doc:
            dq.append(doc.name)
    return dq


def seed_operation_plans(vehicles: List[str], employees: List[str], target: int = 20):
    if not _doctype_available("Operation Plan"):
        return []
    plans = []
    drivers = [e for e in employees if frappe.get_value("Employee", e, "designation") == "Driver"]
    for i in range(1, target + 1):
        name = f"Demo Operation Plan {i:03d}"
        if frappe.db.exists("Operation Plan", {"title": name}):
            continue
        doc, created = _safe_insert({
            "doctype": "Operation Plan",
            "title": name,
            "vehicle": random.choice(vehicles) if vehicles else None,
            "driver": random.choice(drivers) if drivers else None,
            "start_time": (now_datetime() + timedelta(hours=i)).isoformat(),
            "end_time": (now_datetime() + timedelta(hours=i + 4)).isoformat(),
            "notes": "Demo generated plan",
        }, unique_fields=["title"])
        if doc:
            plans.append(doc.name)
    return plans


def seed_movement_logs(vehicles: List[str], target: int = 20):
    if not _doctype_available("Movement Log"):
        return []
    logs = []
    for i in range(1, target + 1):
        doc, created = _safe_insert({
            "doctype": "Movement Log",
            "vehicle": random.choice(vehicles) if vehicles else None,
            "status": random.choice(["Departed", "In Transit", "Arrived"]),
            "start_time": (now_datetime() - timedelta(hours=random.randint(1, 48))).isoformat(),
            "end_time": (now_datetime() + timedelta(hours=random.randint(1, 12))).isoformat(),
        })
        if doc:
            logs.append(doc.name)
    return logs


def seed_cost_revenue(vehicles: List[str], assets: List[str], target: int = 40):
    if not _doctype_available("Cost And Revenue Ledger"):
        return []
    entries = []
    for i in range(1, target + 1):
        doc, created = _safe_insert({
            "doctype": "Cost And Revenue Ledger",
            "date": nowdate(),
            "vehicle": random.choice(vehicles) if vehicles else None,
            "type": random.choice(["Cost", "Revenue"]),
            "amount": random.randint(100, 2000),
            "currency": random.choice(["USD", "NGN", "EUR"]),
            "asset": random.choice(assets) if random.random() < 0.5 and assets else None,
            "notes": "Demo auto generated",
        })
        if doc:
            entries.append(doc.name)
    return entries


def seed_journey_plans(vehicles: List[str], employees: List[str], target: int = 20):
    if not _doctype_available("Journey Plan"):
        return []
    plans = []
    drivers = [e for e in employees if frappe.get_value("Employee", e, "designation") == "Driver"]
    for i in range(1, target + 1):
        title = f"DEMO-JOURNEY-{i:04d}"
        if frappe.db.exists("Journey Plan", title):
            plans.append(title)
            continue
        start = now_datetime() + timedelta(days=1, hours=i)
        doc = frappe.get_doc({
            "doctype": "Journey Plan",
            "name": title,
            "vehicle": random.choice(vehicles) if vehicles else None,
            "driver": random.choice(drivers) if drivers else None,
            "start_time": start,
            "end_time": start + timedelta(hours=6),
            "risk_score": random.randint(1, 10),
            "weather_snapshot": random.choice(["Clear", "Rain", "Storm", "Cloudy"]),
            "sos_contact": "+2348000000000",
        })
        try:
            doc.insert(ignore_permissions=True)
            plans.append(doc.name)
        except Exception as e:
            LOGGER.error(f"Failed Journey Plan {title}: {e}")
    return plans


# Placeholder seeders for other domains to maintain structure & counters
def seed_placeholder(expected_doctypes: List[str]) -> Dict[str, int]:
    counts = {}
    for dt in expected_doctypes:
        if not _doctype_available(dt):
            LOGGER.info(f"[MISSING] {dt} not defined yet – skipping.")
            counts[dt] = 0
            continue
        # If available but not implemented above, we simply ensure at least 1 stub record for smoke
        for i in range(1, 21):
            name = f"DEMO-{dt.upper().replace(' ', '-')}-{i:03d}"[:139]
            if frappe.db.exists(dt, name):
                continue
            try:
                doc = frappe.get_doc({"doctype": dt, "name": name})
                doc.insert(ignore_permissions=True)
            except Exception:
                # If mandatory fields block creation, break to avoid spam
                break
        counts[dt] = frappe.db.count(dt)
    return counts


# --------------------------- Main Run Function ------------------------- #

def run():  # bench execute entry point
    frappe.only_for("System Manager") if hasattr(frappe, "only_for") else None
    random.seed(42)  # deterministic-ish
    summary: Dict[str, int] = {}
    LOGGER.info("Starting TEMS demo data seeding …")

    suppliers = seed_suppliers(10)
    summary["Supplier"] = len(suppliers)
    customers = seed_customers(20)
    summary["Customer"] = len(customers)
    items = seed_items(25)
    summary["Item"] = len(items)
    warehouse = ensure_warehouse()
    purchase_orders = seed_purchase_orders(items, suppliers, 20)
    summary["Purchase Order"] = len(purchase_orders)
    stock_entries = seed_stock_entries(items, warehouse, 20)
    summary["Stock Entry"] = len(stock_entries)
    assets = seed_assets(items, 25)
    summary["Asset"] = len(assets)
    vehicles = seed_vehicles(10)
    summary["Vehicle"] = len(vehicles)
    employees = seed_employees(20, 10)
    summary["Employee"] = len(employees)
    driver_quals = seed_driver_qualifications(employees, vehicles)
    summary["Driver Qualification"] = len(driver_quals)
    op_plans = seed_operation_plans(vehicles, employees, 20)
    summary["Operation Plan"] = len(op_plans)
    move_logs = seed_movement_logs(vehicles, 20)
    summary["Movement Log"] = len(move_logs)
    cr_entries = seed_cost_revenue(vehicles, assets, 40)
    summary["Cost And Revenue Ledger"] = len(cr_entries)
    journey_plans = seed_journey_plans(vehicles, employees, 20)
    summary["Journey Plan"] = len(journey_plans)

    # Placeholder for not-yet-implemented domain doctypes
    expected_remaining = [
        "Asset Utilization Log", "Maintenance Work Order", "Incident Report", "Risk Assessment",
        "Training Record", "Competency Matrix", "Journey Costing", "FX Risk Log", "SLA Log",
        "Feedback Ticket", "Supplier Rating", "Logistics Task", "Border Crossing",
        "Trade Compliance Log", "Informal Operator", "Trip Match", "Savings Group",
        "Emission Log", "Climate Alert", "Policy", "Spot Check", "Compliance Audit",
        "Compliance Document", "Signature Log", "KPI Config", "Report Subscription"
    ]
    placeholder_counts = seed_placeholder(expected_remaining)
    summary.update(placeholder_counts)

    frappe.db.commit()

    # Generate summary markdown inside app (developer oriented)
    md_lines = ["# TEMS Demo Data Summary", "", f"Generated on: {now_datetime()}", "", "| Doctype | Count |", "|--------|-------|"]
    for dt, cnt in sorted(summary.items()):
        md_lines.append(f"| {dt} | {cnt} |")

    content = "\n".join(md_lines)
    path = frappe.get_app_path("tems", "tems_demo", "demo_data_summary.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)

    LOGGER.info("TEMS demo data seeding complete.")
    print(content)  # bench execute output

    return summary


if __name__ == "__main__":  # Allow local python execution inside bench shell
    run()
import random, string, frappe, datetime, os
from frappe.utils import nowdate, add_days, now_datetime

"""Seed rich demo data for TEMS.
Run with: bench execute tems.tems.tems_demo.seed_demo_data.run
"""

BATCH_SIZE = 20

VEHICLE_MODELS = ["DAF XF", "Volvo FH16", "Scania R500", "MAN TGX", "Iveco S-Way"]
ROUTES = [
    ("Lagos", "Accra"),
    ("Lagos", "Kano"),
    ("Accra", "Abidjan"),
    ("Cotonou", "Lagos"),
    ("Lagos", "Port Harcourt"),
]
CURRENCIES = ["USD", "NGN", "EUR"]
SUPPLIERS = [f"Supplier {i}" for i in range(1, 15)]
CUSTOMERS = [f"Customer {i}" for i in range(1, 25)]


def _rand_code(prefix, n=5):
    return prefix + "-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def ensure(name, doctype, **values):
    if frappe.db.exists(doctype, name):
        return frappe.get_doc(doctype, name)
    doc = frappe.new_doc(doctype)
    doc.update({"name": name, **values})
    doc.insert(ignore_permissions=True)
    return doc


def create_items():
    items = []
    for i in range(1, BATCH_SIZE + 1):
        code = _rand_code("ITM")
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": code,
            "item_name": f"Spare Part {i}",
            "item_group": "All Item Groups",
            "stock_uom": "Nos",
            "is_stock_item": 1
        })
        try:
            item.insert(ignore_permissions=True)
        except frappe.DuplicateEntryError:
            continue
        items.append(item)
    return items


def create_suppliers():
    res = []
    for name in SUPPLIERS:
        res.append(ensure(name, "Supplier", supplier_name=name, supplier_group="All Supplier Groups"))
    return res


def create_customers():
    res = []
    for name in CUSTOMERS:
        res.append(ensure(name, "Customer", customer_name=name, customer_group="All Customer Groups", territory="All Territories"))
    return res


def create_purchase_orders(items, suppliers):
    pos = []
    for i in range(BATCH_SIZE):
        supplier = random.choice(suppliers)
        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "supplier": supplier.name,
            "schedule_date": nowdate(),
            "items": [
                {
                    "item_code": random.choice(items).item_code,
                    "qty": random.randint(1,5),
                    "rate": random.randint(50,300)
                }
                for _ in range(random.randint(1,3))
            ]
        })
        po.insert(ignore_permissions=True)
        if po.docstatus == 0:
            po.submit()
        pos.append(po)
    return pos


def create_stock_entries(purchase_orders):
    ses = []
    for po in purchase_orders:
        for poi in po.items:
            se = frappe.get_doc({
                "doctype": "Stock Entry",
                "stock_entry_type": "Material Receipt",
                "items": [
                    {
                        "item_code": poi.item_code,
                        "qty": poi.qty,
                        "t_warehouse": "Stores - TEMS"
                    }
                ]
            })
            try:
                se.insert(ignore_permissions=True)
                se.submit()
                ses.append(se)
            except Exception:
                frappe.db.rollback()
    return ses


def create_assets_from_items(items):
    assets = []
    for item in items[:BATCH_SIZE]:
        asset = frappe.get_doc({
            "doctype": "Asset",
            "item_code": item.item_code,
            "asset_name": f"Asset {item.item_code}",
            "asset_category": "All Asset Categories",
            "purchase_date": nowdate(),
            "gross_purchase_amount": random.randint(1000,5000)
        })
        try:
            asset.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
            continue
        assets.append(asset)
    return assets


def create_vehicles(assets):
    vehicles = []
    for i in range(1, 11):
        v = ensure(f"TMS-{100+i}", "Vehicle", license_plate=f"KT{i:02d}-AB-{random.randint(1000,9999)}", make=random.choice(VEHICLE_MODELS), model_year=2018+ (i % 7))
        vehicles.append(v)
    # simple attach first N assets to vehicles via custom child table if exists
    for idx, asset in enumerate(assets):
        if idx < len(vehicles):
            asset.db_set("vehicle", vehicles[idx].name, commit=True)
    return vehicles


def create_employees_and_drivers():
    employees = []
    for i in range(1, 31):
        emp = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": f"Employee {i}",
            "date_of_joining": add_days(nowdate(), -random.randint(30,400)),
            "status": "Active",
            "company": frappe.db.get_single_value("Global Defaults", "default_company") or "TEMS Logistics"
        })
        try:
            emp.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
            continue
        employees.append(emp)
    drivers = employees[:20]
    return employees, drivers


def qualify_drivers(drivers, vehicles):
    for drv, veh in zip(drivers, vehicles):
        try:
            q = frappe.get_doc({
                "doctype": "Driver Qualification",
                "employee": drv.name,
                "vehicle": veh.name,
                "license_number": _rand_code("LIC", 7),
                "expiry_date": add_days(nowdate(), random.randint(90, 900))
            })
            q.insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
            continue


def create_operation_plans(vehicles, drivers):
    plans = []
    for i in range(BATCH_SIZE):
        veh = random.choice(vehicles)
        drv = random.choice(drivers).name if drivers else None
        (o, d) = random.choice(ROUTES)
        start = now_datetime() - datetime.timedelta(days=random.randint(1,10))
        plan = frappe.get_doc({
            "doctype": "Operation Plan",
            "title": f"Trip {o}-{d} #{i+1}",
            "vehicle": veh.name,
            "driver": drv,
            "start_time": start,
            "end_time": start + datetime.timedelta(hours=random.randint(5,48)),
            "notes": f"Auto-generated demo plan from {o} to {d}."
        })
        try:
            plan.insert(ignore_permissions=True)
            if plan.docstatus == 0:
                plan.submit()
        except Exception:
            frappe.db.rollback()
            continue
        plans.append(plan)
    return plans


def create_movement_logs(plans):
    statuses = ["Check-In", "Departed", "Transit", "Delivered"]
    logs = []
    for plan in plans:
        for s in statuses:
            log = frappe.get_doc({
                "doctype": "Movement Log",
                "operation_plan": plan.name,
                "vehicle": plan.vehicle,
                "status": s,
                "log_time": now_datetime() - datetime.timedelta(hours=random.randint(1,72)),
            })
            try:
                log.insert(ignore_permissions=True)
            except Exception:
                frappe.db.rollback()
                continue
            logs.append(log)
    return logs


def create_cost_revenue_entries(vehicles, assets):
    entries = []
    for veh in vehicles:
        for _ in range(5):
            asset = random.choice(assets) if assets else None
            doc = frappe.get_doc({
                "doctype": "Cost And Revenue Ledger",
                "date": nowdate(),
                "vehicle": veh.name,
                "type": random.choice(["Cost", "Revenue"]),
                "amount": random.randint(100, 1500),
                "currency": random.choice(CURRENCIES),
                "asset": asset.name if asset else None,
                "notes": "Auto demo entry"
            })
            try:
                doc.insert(ignore_permissions=True)
            except Exception:
                frappe.db.rollback()
                continue
            entries.append(doc)
    return entries


def run():
    frappe.flags.mute_emails = True
    items = create_items()
    suppliers = create_suppliers()
    customers = create_customers()
    pos = create_purchase_orders(items, suppliers)
    ses = create_stock_entries(pos)
    assets = create_assets_from_items(items)
    vehicles = create_vehicles(assets)
    employees, drivers = create_employees_and_drivers()
    qualify_drivers(drivers, vehicles)
    plans = create_operation_plans(vehicles, drivers)
    movement_logs = create_movement_logs(plans)
    ledger = create_cost_revenue_entries(vehicles, assets)

    frappe.db.commit()
    # summary file
    summary = {
        "Item": len(items),
        "Supplier": len(suppliers),
        "Customer": len(customers),
        "Purchase Order": len(pos),
        "Stock Entry": len(ses),
        "Asset": len(assets),
        "Vehicle": len(vehicles),
        "Employee": len(employees),
        "Driver Qualification": len(drivers),
        "Operation Plan": len(plans),
        "Movement Log": len(movement_logs),
        "Cost And Revenue Ledger": len(ledger),
    }
    lines = ["# Demo Data Summary", "", "| DocType | Records |", "|---------|---------|"]
    for k,v in summary.items():
        lines.append(f"| {k} | {v} |")
    # Write summary inside app path (not per-site public). Resolve base path from this file location.
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, "demo_data_summary.md"), "w") as fh:
        fh.write("\n".join(lines))
    return summary

if __name__ == "__main__":
    run()
