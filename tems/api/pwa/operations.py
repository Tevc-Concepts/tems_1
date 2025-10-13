import frappe
from frappe import _
from frappe.utils import now_datetime, getdate, add_days

@frappe.whitelist()
def get_operations_dashboard():
    """Get operations dashboard - real-time fleet status"""
    today = getdate()
    
    # Active trips
    active_operations = frappe.get_all(
        "Operation Plan",
        filters={
            "status": ["in", ["Assigned", "Active"]],
            "start_time": [">=", today]
        },
        fields=["name", "title", "vehicle", "driver", "operation_mode", "start_time", "status"],
        order_by="start_time asc"
    )
    
    # Get real-time vehicle positions (last movement log per vehicle)
    vehicle_positions = frappe.db.sql("""
        SELECT 
            ml.vehicle,
            ml.state,
            ml.event_time,
            ml.location_lat,
            ml.location_lng,
            ml.geohash,
            v.license_plate
        FROM `tabMovement Log` ml
        INNER JOIN `tabVehicle` v ON v.name = ml.vehicle
        WHERE ml.event_time >= %s
        AND ml.name IN (
            SELECT MAX(name) 
            FROM `tabMovement Log` 
            GROUP BY vehicle
        )
        ORDER BY ml.event_time DESC
    """, (add_days(today, -1),), as_dict=True)
    
    # Exception alerts
    exceptions = frappe.get_all(
        "Control Exception",
        filters={
            "status": ["in", ["Open", "Acknowledged"]],
            "occurred_at": [">=", add_days(today, -1)]
        },
        fields=["name", "type", "severity", "occurred_at", "vehicle", "status"],
        order_by="occurred_at desc",
        limit=20
    )
    
    # SOS events
    sos_events = frappe.get_all(
        "SOS Event",
        filters={
            "status": ["in", ["Open", "Acknowledged"]],
            "created_at": [">=", add_days(today, -1)]
        },
        fields=["name", "created_at", "reporter_employee", "vehicle", "lat", "lng", "status"],
        order_by="created_at desc"
    )
    
    # Fleet utilization summary
    total_vehicles = frappe.db.count("Vehicle", {"disabled": 0})
    active_vehicles = len(set([op.vehicle for op in active_operations if op.vehicle]))
    
    return {
        "active_operations": active_operations,
        "vehicle_positions": vehicle_positions,
        "exceptions": exceptions,
        "sos_events": sos_events,
        "fleet_summary": {
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "utilization_rate": (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
        },
        "timestamp": now_datetime()
    }


@frappe.whitelist()
def create_dispatch_schedule(data):
    """Create new dispatch schedule"""
    schedule = frappe.get_doc({
        "doctype": "Dispatch Schedule",
        "date": data.get("date"),
        "route": data.get("route"),
        "shift": data.get("shift"),
        "dispatcher": frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name"),
        "notes": data.get("notes")
    })
    
    # Add planned departures
    if data.get("departures"):
        for dep in data["departures"]:
            schedule.append("planned_departures", {
                "departure_time": dep.get("departure_time"),
                "vehicle": dep.get("vehicle"),
                "notes": dep.get("notes")
            })
    
    schedule.insert()
    
    return {
        "success": True,
        "schedule": schedule.name,
        "message": _("Dispatch schedule created successfully")
    }


@frappe.whitelist()
def assign_trip(journey_plan, vehicle, driver, assistant=None):
    """Assign driver and vehicle to journey"""
    trip_allocation = frappe.get_doc({
        "doctype": "Trip Allocation",
        "journey_plan": journey_plan,
        "vehicle": vehicle,
        "driver": driver,
        "assistant": assistant,
        "status": "Assigned",
        "schedule_slot": now_datetime()
    })
    
    trip_allocation.insert()
    
    # Update journey plan
    journey = frappe.get_doc("Journey Plan", journey_plan)
    journey.driver = driver
    journey.vehicle = vehicle
    journey.save()
    
    return {
        "success": True,
        "allocation": trip_allocation.name,
        "message": _("Trip assigned successfully")
    }