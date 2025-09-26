import frappe
from frappe.utils import now_datetime, nowdate, add_days


def execute():
    # Idempotent seed for Fleet domain
    make_routes()
    make_journey_plans()
    make_fuel_logs()
    make_work_orders()


def make_routes():
    if frappe.db.exists("Route Planning", {"route_name": "City Loop"}):
        return
    rp = frappe.get_doc({
        "doctype": "Route Planning",
        "route_name": "City Loop",
        "distance_km": 24.5,
        "duration_estimate": 60,
        "waypoints": [
            {"doctype": "Way Points", "stop_name": "Depot", "location": None, "stop_type": "Pickup", "mandatory_stop": 1},
            {"doctype": "Way Points", "stop_name": "Central", "location": None, "stop_type": "Checkpoint", "mandatory_stop": 0},
            {"doctype": "Way Points", "stop_name": "Harbor", "location": None, "stop_type": "Drop-off", "mandatory_stop": 1}
        ],
    })
    rp.insert(ignore_permissions=True)


def any_employee():
    emp = frappe.db.get_value("Employee", {"status": "Active"}, "name")
    return emp or "HR-EMP-0001"


def any_vehicle():
    veh = frappe.db.get_value("Vehicle", {}, "name")
    if veh:
        return veh
    # Try to create a minimal vehicle if Vehicle DocType exists
    try:
        doc = frappe.get_doc({
            "doctype": "Vehicle",
            "license_plate": "TEMP-VEH-0001",
            "make": "TEMS",
            "model": "Seed",
        })
        doc.insert(ignore_permissions=True)
        return doc.name
    except Exception:
        # Fall back to using Asset link path
        return None


def any_asset():
    ast = frappe.db.get_value("Asset", {}, "name")
    if ast:
        return ast
    # Try to create a minimal Asset
    try:
        company = frappe.db.get_value("Company", {}, "name") or frappe.db.get_default("company")
        doc = frappe.get_doc({
            "doctype": "Asset",
            "asset_name": "Seed Asset",
            "asset_category": frappe.db.get_value("Asset Category", {}, "name") or "Computers",
            "company": company,
            "purchase_date": nowdate(),
            "gross_purchase_amount": 100000,
        })
        doc.insert(ignore_permissions=True)
        return doc.name
    except Exception:
        return None


def make_journey_plans():
    route = frappe.db.get_value("Route Planning", {"route_name": "City Loop"}, "name")
    if not route:
        return
    if frappe.db.exists("Journey Plan", {"route": route}):
        return
    vehicle = any_vehicle()
    jp = frappe.get_doc({
        "doctype": "Journey Plan",
        "route": route,
        "driver": any_employee(),
        "vehicle": vehicle or None,
        "start_time": now_datetime(),
        "risk_score": 3.2,
        "sos_contact": "+2348000000000",
    })
    jp.insert(ignore_permissions=True)


def make_fuel_logs():
    if frappe.db.exists("Fuel Log", {"station": "Main Station"}):
        return
    asset = any_asset()
    if not asset:
        # Skip if Asset cannot be determined in this environment
        return
    fl = frappe.get_doc({
        "doctype": "Fuel Log",
        "vehicle": any_vehicle() or asset,
        "odometer": 10234,
        "liters": 45.5,
        "price_per_liter": 650,
        "station": "Main Station",
        "date": nowdate(),
    })
    fl.insert(ignore_permissions=True)


def make_work_orders():
    if frappe.db.exists("Maintenance Work Order", {"status": "Open"}):
        return
    asset = any_asset()
    if not asset:
        return
    supplier = frappe.db.get_value("Supplier", {}, "name")
    item = frappe.db.get_value("Item", {}, "name")
    wo = frappe.get_doc({
        "doctype": "Maintenance Work Order",
        "asset": asset,
        "vendor": supplier,
        "status": "Open",
        "planned_date": add_days(nowdate(), 2),
        "parts_used": ([{"doctype": "Maintenance Part Item", "item": item, "qty": 2}] if item else []),
    })
    wo.insert(ignore_permissions=True)
