"""
TEMS Operations Handlers
Event handlers for Operations module
"""
from __future__ import annotations

import frappe
from frappe.utils import now, get_datetime


def ensure_vehicle_available(doc, method=None):
    """Before submitting an Operation Plan, ensure the linked Vehicle is available.
    Vehicle is the operational unit; we must not allow allocation if under maintenance or already allocated.
    """
    vehicle = getattr(doc, "vehicle", None)
    if not vehicle:
        # Operation Plan must carry a Vehicle link by architecture rule
        frappe.throw("Operation Plan requires a Vehicle.")

    status = frappe.db.get_value("Vehicle", vehicle, "status")
    if isinstance(status, str) and status.lower() in {"maintenance", "unavailable"}:
        frappe.throw(f"Vehicle {vehicle} is not available (status: {status}).")

    # Check for overlapping Trip Allocations or Operation Plans
    start_time = getattr(doc, "start_time", None)
    end_time = getattr(doc, "end_time", None)
    if start_time and end_time:
        overlapping = frappe.db.exists(
            "Trip Allocation",
            {
                "vehicle": vehicle,
                "status": ["in", ["Planned", "Assigned", "In Progress"]],
            },
        )
        # Simple existence check; detailed overlap can be added when we track times on Trip Allocation
        if overlapping:
            frappe.msgprint(
                f"Vehicle {vehicle} has other active allocations. Proceed if intentional.",
                alert=True,
            )


def log_movement_start(doc, method=None):
    """On Operation Plan submit, create a Movement Log entry with Check-Out state."""
    vehicle = getattr(doc, "vehicle", None)
    if not vehicle:
        return
    frappe.get_doc(
        {
            "doctype": "Movement Log",
            "vehicle": vehicle,
            "operation_plan": doc.name,
            "state": "Check-Out",
            "event_time": now(),
        }
    ).insert(ignore_permissions=True)


def update_vehicle_status(doc, method=None):
    """When Movement Log updates, reflect state progression and set Vehicle operational status."""
    state = getattr(doc, "state", "") or ""
    veh = getattr(doc, "vehicle", None)
    if not veh:
        return

    new_status = None
    if state == "Check-In":
        new_status = "Available"
    elif state in {"Check-Out", "In Transit", "Diversion", "Out Transit"}:
        new_status = "On Trip"
    elif state in {"Delivered", "Delivery Confirmation"}:
        new_status = "Available"

    if new_status:
        # Only attempt if status column actually exists on Vehicle (guard for demo environment)
        if frappe.db.has_column("Vehicle", "status"):
            frappe.db.set_value("Vehicle", veh, "status", new_status)


def ensure_driver_vehicle_valid(doc, method=None):
    """Before inserting Trip Allocation, ensure driver is valid for the Vehicle per People API."""
    driver = getattr(doc, "driver", None)
    veh = getattr(doc, "vehicle", None)
    if not driver or not veh:
        frappe.throw("Trip Allocation requires both Driver and Vehicle.")

    # People validation API (optional, return truthy)
    try:
        is_ok = frappe.call("tems.tems_people.api.validate_driver_active", employee=driver)
    except Exception:
        is_ok = None
    if is_ok is False:
        frappe.throw(f"Driver {driver} is not active/qualified.")


def publish_operations_event(doc, method=None):
    """Realtime publish for Operations Event creation/update."""
    try:
        frappe.publish_realtime(
            event="operations_event",
            message={
                "name": doc.name,
                "journey_plan": getattr(doc, "journey_plan", None),
                "event_time": getattr(doc, "event_time", None),
                "event_type": getattr(doc, "event_type", None),
                "vehicle": getattr(doc, "vehicle", None),
            },
            user="",
        )
    except Exception:
        pass


def publish_sos_event(doc, method=None):
    """Realtime publish for SOS events and notify Safety team immediately."""
    try:
        frappe.publish_realtime(
            event="sos_event",
            message={
                "name": doc.name,
                "status": getattr(doc, "status", None),
                "vehicle": getattr(doc, "vehicle", None),
                "location": {
                    "lat": getattr(doc, "lat", None),
                    "lng": getattr(doc, "lng", None),
                },
            },
            user="",
        )
        
        # Notify Safety Manager and Operations Manager roles
        try:
            recipients = [u.name for u in frappe.get_all("User", filters={"roles.role": ["in", ["Safety Manager", "Operations Manager"]]}, fields=["name"])]
            if recipients:
                frappe.sendmail(
                    recipients=recipients,
                    subject=f"SOS Event: {doc.name}",
                    content=f"SOS raised for vehicle {getattr(doc, 'vehicle', '')} at {getattr(doc, 'creation', '')}",
                )
        except Exception:
            pass
    except Exception:
        pass


def validate_operation_plan(doc, method=None):
    """Ensure Operation Plan.operation_mode matches Vehicle.vehicle_type and auto-sync it."""
    veh = getattr(doc, "vehicle", None)
    if veh:
        vt = frappe.db.get_value("Vehicle", veh, "vehicle_type") or frappe.db.get_value("Vehicle", veh, "custom_vehicle_type")
        vt_norm = str(vt or "").strip().title()
        if vt_norm in {"Cargo", "Passenger"}:
            doc.operation_mode = vt_norm
    # If explicitly set and inconsistent, block
    if getattr(doc, "operation_mode", None) and veh:
        vt = frappe.db.get_value("Vehicle", veh, "vehicle_type") or frappe.db.get_value("Vehicle", veh, "custom_vehicle_type")
        vt_norm = str(vt or "").strip().title()
        if vt_norm in {"Cargo", "Passenger"} and doc.operation_mode != vt_norm:
            frappe.throw("Operation Mode must match Vehicle Type.")
