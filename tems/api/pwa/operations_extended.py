"""
Operations PWA API Endpoints - Extended
Additional endpoints to match Operations PWA frontend needs
"""

import frappe
from frappe import _
from frappe.utils import nowdate, now_datetime, add_days, getdate
import json


@frappe.whitelist()
def get_vehicles(filters=None):
    """
    Get list of vehicles with optional filters
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        elif filters is None:
            filters = {}
        
        conditions = []
        values = {}
        
        if filters.get('status'):
            conditions.append("disabled = 0" if filters['status'] == 'Active' else "disabled = 1")
        
        if filters.get('vehicle_type'):
            conditions.append("vehicle_type = %(vehicle_type)s")
            values['vehicle_type'] = filters['vehicle_type']
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        vehicles = frappe.db.sql(f"""
            SELECT 
                name,
                license_plate,
                make,
                model,
                vehicle_type,
                fuel_type,
                last_odometer,
                disabled
            FROM `tabVehicle`
            {where_clause}
            ORDER BY license_plate
            LIMIT 100
        """, values, as_dict=True)
        
        return {
            "success": True,
            "data": vehicles,
            "count": len(vehicles)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching vehicles: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_vehicle_locations():
    """
    Get real-time vehicle locations from latest movement logs
    """
    try:
        # Get latest location for each vehicle from last 24 hours
        locations = frappe.db.sql("""
            SELECT 
                ml.vehicle,
                ml.location_lat as lat,
                ml.location_lng as lng,
                ml.geohash,
                ml.state,
                ml.event_time as last_update,
                v.license_plate,
                v.make,
                v.model
            FROM `tabMovement Log` ml
            INNER JOIN `tabVehicle` v ON v.name = ml.vehicle
            WHERE ml.event_time >= %(start_time)s
            AND ml.name IN (
                SELECT MAX(name) 
                FROM `tabMovement Log` 
                GROUP BY vehicle
            )
            ORDER BY ml.event_time DESC
        """, {"start_time": add_days(nowdate(), -1)}, as_dict=True)
        
        return {
            "success": True,
            "data": locations,
            "count": len(locations),
            "timestamp": now_datetime()
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching vehicle locations: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_dispatch_queue():
    """
    Get pending dispatch operations
    """
    try:
        today = getdate()
        
        # Get scheduled operations
        operations = frappe.db.sql("""
            SELECT 
                name,
                title,
                vehicle,
                driver,
                operation_mode,
                start_time,
                end_time,
                status,
                priority
            FROM `tabOperation Plan`
            WHERE status IN ('Scheduled', 'Pending')
            AND start_time >= %(today)s
            ORDER BY priority DESC, start_time ASC
            LIMIT 50
        """, {"today": today}, as_dict=True)
        
        return {
            "success": True,
            "data": operations,
            "count": len(operations)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching dispatch queue: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_active_trips():
    """
    Get currently active trips
    """
    try:
        active_trips = frappe.db.sql("""
            SELECT 
                name,
                title,
                vehicle,
                driver,
                operation_mode,
                start_time,
                end_time,
                status,
                route
            FROM `tabOperation Plan`
            WHERE status = 'Active'
            ORDER BY start_time DESC
            LIMIT 100
        """, as_dict=True)
        
        return {
            "success": True,
            "data": active_trips,
            "count": len(active_trips)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching active trips: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_route_optimization(origin=None, destination=None, waypoints=None):
    """
    Get route optimization suggestions (placeholder for future implementation)
    """
    try:
        # This is a placeholder - actual implementation would integrate with
        # Google Maps API, OpenRouteService, or similar routing service
        
        return {
            "success": True,
            "data": {
                "origin": origin,
                "destination": destination,
                "waypoints": waypoints,
                "optimized_route": [],
                "total_distance": 0,
                "estimated_time": 0,
                "message": "Route optimization feature coming soon"
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in route optimization: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_driver_availability(date=None):
    """
    Get available drivers for a given date
    """
    try:
        if not date:
            date = nowdate()
        
        # Get all drivers
        all_drivers = frappe.get_all(
            "Employee",
            filters={
                "designation": "Driver",
                "status": "Active"
            },
            fields=["name", "employee_name", "cell_number"]
        )
        
        # Get assigned drivers for the date
        assigned_drivers = frappe.db.sql("""
            SELECT DISTINCT driver
            FROM `tabOperation Plan`
            WHERE DATE(start_time) = %(date)s
            AND status IN ('Scheduled', 'Active')
        """, {"date": date}, as_dict=True)
        
        assigned_driver_ids = [d.driver for d in assigned_drivers if d.driver]
        
        # Filter available drivers
        available_drivers = [
            d for d in all_drivers 
            if d.name not in assigned_driver_ids
        ]
        
        return {
            "success": True,
            "data": {
                "available": available_drivers,
                "assigned": assigned_driver_ids,
                "total_drivers": len(all_drivers),
                "available_count": len(available_drivers)
            },
            "count": len(available_drivers)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching driver availability: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_operations_statistics(period='today'):
    """
    Get operations dashboard statistics
    """
    try:
        if period == 'today':
            start_date = nowdate()
        elif period == 'week':
            start_date = add_days(nowdate(), -7)
        elif period == 'month':
            start_date = add_days(nowdate(), -30)
        else:
            start_date = nowdate()
        
        # Total operations
        total_operations = frappe.db.count(
            "Operation Plan",
            {"start_time": [">=", start_date]}
        )
        
        # Completed operations
        completed_operations = frappe.db.count(
            "Operation Plan",
            {
                "start_time": [">=", start_date],
                "status": "Completed"
            }
        )
        
        # Active operations
        active_operations = frappe.db.count(
            "Operation Plan",
            {"status": "Active"}
        )
        
        # Pending operations
        pending_operations = frappe.db.count(
            "Operation Plan",
            {
                "status": ["in", ["Scheduled", "Pending"]],
                "start_time": [">=", nowdate()]
            }
        )
        
        # Fleet utilization
        total_vehicles = frappe.db.count("Vehicle", {"disabled": 0})
        active_vehicles = frappe.db.sql("""
            SELECT COUNT(DISTINCT vehicle)
            FROM `tabOperation Plan`
            WHERE status = 'Active'
            AND vehicle IS NOT NULL
        """)[0][0]
        
        # Exceptions/alerts
        open_exceptions = frappe.db.count(
            "Control Exception",
            {
                "status": ["in", ["Open", "Acknowledged"]],
                "occurred_at": [">=", start_date]
            }
        )
        
        return {
            "success": True,
            "data": {
                "total_operations": total_operations,
                "completed_operations": completed_operations,
                "active_operations": active_operations,
                "pending_operations": pending_operations,
                "completion_rate": (completed_operations / total_operations * 100) if total_operations > 0 else 0,
                "fleet": {
                    "total_vehicles": total_vehicles,
                    "active_vehicles": active_vehicles,
                    "utilization_rate": (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
                },
                "alerts": {
                    "open_exceptions": open_exceptions
                },
                "period": period
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching operations statistics: {str(e)}", "Operations API")
        return {"success": False, "message": str(e)}
