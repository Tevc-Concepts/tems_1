from __future__ import annotations
import random
import frappe
from frappe.utils import nowdate

VEHICLE_MODELS = ["DAF CF", "MAN TGS", "Volvo FH", "Scania R450", "Iveco Stralis", "Mercedes Actros"]


def seed_vehicles_and_attach_assets(context, count: int = 10):
    assets = context.get("assets", [])
    vehicles = []
    # Ensure a basic UOM exists for fuel if not present
    # Ensure fuel and distance UOMs
    if not frappe.db.exists("UOM", "Litre"):
        try:
            frappe.get_doc({"doctype": "UOM", "uom_name": "Litre"}).insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
    if not frappe.db.exists("UOM", "Km"):
        try:
            frappe.get_doc({"doctype": "UOM", "uom_name": "Km"}).insert(ignore_permissions=True)
        except Exception:
            frappe.db.rollback()
    for i in range(count):
        plate = f"KJA-{random.randint(100,999)}-TRK"
        if frappe.db.exists("Vehicle", {"license_plate": plate}):
            continue
        # Pick a random driver if field custom_assigned_driver is mandatory
        driver_field = "custom_assigned_driver" if frappe.db.has_column("Vehicle", "custom_assigned_driver") else None
        asset_link_field = "custom_asset_id" if frappe.db.has_column("Vehicle", "custom_asset_id") else None
        assigned_driver = None
        if driver_field:
            emps = context.get("employees") or frappe.get_all("Employee", pluck="name")
            if not emps:
                # create a placeholder driver because custom field is mandatory
                try:
                    emp_doc = frappe.get_doc({
                        "doctype": "Employee",
                        "employee_name": "Seed Driver",
                        "first_name": "Seed",
                        "gender": "Male",
                        "date_of_birth": nowdate(),
                        "date_of_joining": nowdate(),
                        "status": "Active"
                    }).insert(ignore_permissions=True)
                    emps = [emp_doc.name]
                    context.setdefault("employees", []).append(emp_doc.name)
                except Exception:
                    frappe.db.rollback()
            assigned_driver = emps[0] if emps else None
        attach_asset = None
        if asset_link_field and assets:
            attach_asset = assets[i % len(assets)]
        vdoc = frappe.get_doc({
            "doctype": "Vehicle",
            "license_plate": plate,
            "make": random.choice(VEHICLE_MODELS),
            "model": "2024",
            "chassis_no": f"CHS{random.randint(100000,999999)}",
            "acquisition_date": nowdate(),
            # Mandatory core fields
            "last_odometer": random.randint(1000, 50000),
            "fuel_type": "Diesel",
            "uom": "Litre" if frappe.db.exists("UOM", "Litre") else None,
            **({driver_field: assigned_driver} if driver_field else {}),
            **({asset_link_field: attach_asset} if asset_link_field else {}),
        })
        try:
            # Use ignore_mandatory to bypass any unexpected custom mandatory constraints
            vdoc.insert(ignore_permissions=True, ignore_mandatory=True)
            vehicles.append(vdoc.name)
        except Exception:
            frappe.db.rollback()
            continue
    context.setdefault("vehicles", []).extend(vehicles)

    # Distribute many assets -> one vehicle (aim ~2 per vehicle) if Asset has vehicle field
    if frappe.db.has_column("Asset", "vehicle") and assets:
        v_cycle = vehicles or frappe.get_all("Vehicle", pluck="name")
        if v_cycle:
            per_vehicle_target = 2
            assigned_counts = {v: 0 for v in v_cycle}
            v_index = 0
            for asset in assets:
                # Skip already linked assets
                if frappe.db.get_value("Asset", asset, "vehicle"):
                    continue
                # Find next vehicle with < per_vehicle_target
                attempts = 0
                while attempts < len(v_cycle) and assigned_counts[v_cycle[v_index]] >= per_vehicle_target:
                    v_index = (v_index + 1) % len(v_cycle)
                    attempts += 1
                vehicle_name = v_cycle[v_index]
                try:
                    frappe.db.set_value("Asset", asset, "vehicle", vehicle_name)
                    assigned_counts[vehicle_name] += 1
                except Exception:
                    frappe.db.rollback()
                v_index = (v_index + 1) % len(v_cycle)


def seed_maintenance(context, count: int = 20):
    vehicles = context.get("vehicles", [])
    work_orders = []
    for i in range(count):
        if not vehicles:
            break
        v = random.choice(vehicles)
        wo = frappe.get_doc({
            "doctype": "Maintenance Work Order",
            "vehicle": v,
            "status": "Open"
        })
        try:
            wo.insert(ignore_permissions=True)
            work_orders.append(wo.name)
        except Exception:
            frappe.db.rollback()
    context.setdefault("maintenance_work_orders", []).extend(work_orders)
