"""
Tyre Lifecycle Event Handlers
Manages tyre lifecycle events and vehicle integration
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import flt, now_datetime


def on_tyre_install(doc, method=None):
    """
    Handle tyre installation event
    Updates vehicle tyre map and asset tracking
    """
    if not doc.tyre or not doc.vehicle:
        return
    
    # Update tyre status
    tyre = frappe.get_doc("Tyre", doc.tyre)
    tyre.status = "Installed"
    tyre.vehicle = doc.vehicle
    tyre.db_update()
    
    # Update vehicle tyre mapping if custom field exists
    update_vehicle_tyre_map(doc.vehicle)
    
    frappe.logger("tems_tyre").info(f"Tyre {doc.tyre} installed on vehicle {doc.vehicle}")


def on_tyre_removal(doc, method=None):
    """
    Handle tyre removal event
    """
    if not doc.tyre or not doc.removed_date:
        return
    
    # Update tyre status
    tyre = frappe.get_doc("Tyre", doc.tyre)
    tyre.status = "In Stock"
    tyre.vehicle = None
    tyre.db_update()
    
    # Update vehicle tyre mapping
    if doc.vehicle:
        update_vehicle_tyre_map(doc.vehicle)
    
    frappe.logger("tems_tyre").info(f"Tyre {doc.tyre} removed from vehicle {doc.vehicle}")


def on_tyre_rotation(doc, method=None):
    """
    Handle tyre rotation event
    Updates position and mileage tracking
    """
    if not doc.tyre or not doc.vehicle:
        return
    
    # Update tyre mileage
    tyre = frappe.get_doc("Tyre", doc.tyre)
    if doc.mileage_at_rotation:
        tyre.current_mileage = doc.mileage_at_rotation
        tyre.db_update()
    
    # Update vehicle tyre mapping
    update_vehicle_tyre_map(doc.vehicle)
    
    frappe.logger("tems_tyre").info(f"Tyre {doc.tyre} rotated on vehicle {doc.vehicle}")


def on_tyre_inspection(doc, method=None):
    """
    Handle tyre inspection event
    Updates health status and triggers alerts if needed
    """
    if not doc.tyre:
        return
    
    tyre = frappe.get_doc("Tyre", doc.tyre)
    
    # Update inspection date
    tyre.last_inspection_date = doc.inspection_date or now_datetime()
    
    # Update AI health status if available
    if doc.ai_condition_classification:
        tyre.ai_health_status = doc.ai_condition_classification
        
        # Trigger alerts for critical conditions
        if doc.ai_condition_classification in ["Replace Soon", "Replace Immediately"]:
            create_tyre_alert(tyre, doc.ai_condition_classification, doc.observations)
    
    # Update pressure if captured
    if doc.pressure_psi:
        tyre.last_pressure_psi = doc.pressure_psi
    
    # Update tread depth
    if doc.tread_depth_mm:
        tyre.last_tread_depth_mm = doc.tread_depth_mm
        
        # Calculate estimated remaining life based on tread
        update_estimated_life(tyre, doc.tread_depth_mm)
    
    tyre.db_update()
    
    frappe.logger("tems_tyre").info(f"Tyre {doc.tyre} inspected with status: {doc.ai_condition_classification}")


def on_tyre_disposal(doc, method=None):
    """
    Handle tyre disposal event
    Marks tyre as disposed and records final costs
    """
    if not doc.tyre:
        return
    
    tyre = frappe.get_doc("Tyre", doc.tyre)
    tyre.status = "Disposed"
    tyre.disposal_date = doc.disposal_date
    tyre.disposal_reason = doc.reason
    tyre.scrap_value = doc.scrap_value or 0
    tyre.db_update()
    
    # Create cost ledger entry
    create_tyre_cost_entry(
        tyre=doc.tyre,
        vehicle=doc.vehicle,
        amount=doc.final_cost_impact or 0,
        cost_type="Tyre Disposal",
        reference_doctype="Tyre Disposal Log",
        reference_name=doc.name
    )
    
    frappe.logger("tems_tyre").info(f"Tyre {doc.tyre} disposed: {doc.reason}")


def update_vehicle_tyre_map(vehicle: str):
    """
    Update vehicle's tyre position mapping
    Queries all installed tyres for this vehicle
    """
    if not vehicle or not frappe.db.exists("Vehicle", vehicle):
        return
    
    # Get all currently installed tyres for this vehicle
    installations = frappe.get_all(
        "Tyre Installation Log",
        filters={
            "vehicle": vehicle,
            "removed_date": ["is", "not set"]
        },
        fields=["tyre", "position"],
        order_by="installation_date desc"
    )
    
    # Build tyre map as JSON
    tyre_map = {inst.position: inst.tyre for inst in installations}
    
    # Update vehicle custom field if it exists
    if frappe.db.has_column("Vehicle", "custom_tyre_map"):
        frappe.db.set_value("Vehicle", vehicle, "custom_tyre_map", frappe.as_json(tyre_map))
    
    return tyre_map


def update_estimated_life(tyre_doc, current_tread_depth: float):
    """
    Calculate estimated remaining tyre life based on tread depth
    Assumes new tyre has 16mm tread, legal minimum is 1.6mm
    """
    NEW_TREAD = 16.0  # mm
    MIN_TREAD = 1.6   # mm
    
    usable_tread = NEW_TREAD - MIN_TREAD
    remaining_tread = max(0, current_tread_depth - MIN_TREAD)
    
    if usable_tread <= 0:
        return
    
    # Calculate percentage remaining
    percentage_remaining = (remaining_tread / usable_tread) * 100
    
    # Estimate remaining km based on historical wear rate
    # This is a simplified model - should be enhanced with ML
    if tyre_doc.current_mileage and tyre_doc.initial_tread_depth:
        km_traveled = tyre_doc.current_mileage
        tread_worn = tyre_doc.initial_tread_depth - current_tread_depth
        
        if tread_worn > 0:
            km_per_mm = km_traveled / tread_worn
            estimated_remaining_km = remaining_tread * km_per_mm
            tyre_doc.estimated_remaining_life = estimated_remaining_km


def create_tyre_alert(tyre_doc, condition: str, observations: str = None):
    """
    Create notification alert for tyre condition
    """
    try:
        # Create a notification record
        alert_doc = frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Tyre Alert: {tyre_doc.name} - {condition}",
            "email_content": f"""
                Tyre: {tyre_doc.name}
                Vehicle: {tyre_doc.vehicle or 'Not Installed'}
                Status: {condition}
                Current Mileage: {tyre_doc.current_mileage} km
                {f'Observations: {observations}' if observations else ''}
            """,
            "document_type": "Tyre",
            "document_name": tyre_doc.name,
            "type": "Alert"
        })
        alert_doc.insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create tyre alert: {str(e)}")


def create_tyre_cost_entry(tyre: str, vehicle: str, amount: float, cost_type: str,
                           reference_doctype: str = None, reference_name: str = None):
    """
    Create cost ledger entry for tyre-related expenses
    Integrates with TEMS Finance module
    """
    if not amount or amount == 0:
        return
    
    try:
        # Get asset link from tyre
        asset_link = frappe.db.get_value("Tyre", tyre, "asset_link")
        
        # Create entry in Cost And Revenue Ledger
        cost_entry = frappe.get_doc({
            "doctype": "Cost And Revenue Ledger",
            "date": frappe.utils.today(),
            "vehicle": vehicle,
            "asset": asset_link,
            "type": "Cost",
            "amount": abs(amount),
            "category": cost_type,
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "remarks": f"Tyre {tyre}: {cost_type}"
        })
        cost_entry.insert(ignore_permissions=True)
        
        frappe.logger("tems_tyre").info(f"Cost entry created: {cost_type} - {amount}")
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create cost entry: {str(e)}")


def rollup_tyre_costs_to_vehicle(vehicle: str):
    """
    Aggregate all tyre costs for a vehicle
    Used by Fleet profitability calculations
    """
    if not vehicle:
        return 0
    
    # Get all tyres currently or previously on this vehicle
    tyres = frappe.get_all(
        "Tyre",
        filters={"vehicle": vehicle},
        pluck="name"
    )
    
    total_cost = 0
    
    for tyre in tyres:
        # Sum up all costs for this tyre
        costs = frappe.db.sql("""
            SELECT SUM(amount) as total
            FROM `tabCost And Revenue Ledger`
            WHERE vehicle = %s
            AND (asset IN (SELECT asset_link FROM `tabTyre` WHERE name = %s)
                 OR remarks LIKE %s)
            AND type = 'Cost'
        """, (vehicle, tyre, f"%{tyre}%"), as_dict=True)
        
        if costs and costs[0].total:
            total_cost += flt(costs[0].total)
    
    return total_cost
