import frappe
from frappe import _
from frappe.utils import now_datetime, get_datetime, getdate
import json

@frappe.whitelist()
def get_driver_dashboard(driver_email=None):
    """Get driver dashboard data - today's trips, pending tasks, alerts"""
    if not driver_email:
        driver_email = frappe.session.user
    
    employee = frappe.db.get_value("Employee", {"user_id": driver_email}, "name")
    if not employee:
        frappe.throw(_("No employee record found for this user"))
    
    today = getdate()
    
    # Get today's journey plans
    journey_plans = frappe.get_all(
        "Journey Plan",
        filters={
            "driver": employee,
            "start_time": [">=", today]
        },
        fields=["name", "route", "vehicle", "start_time", "end_time", "risk_score", "sos_contact"],
        order_by="start_time asc"
    )
    
    # Get active operation plans
    operation_plans = frappe.get_all(
        "Operation Plan",
        filters={
            "driver": employee,
            "status": ["in", ["Assigned", "Active"]],
            "start_time": [">=", today]
        },
        fields=["name", "title", "vehicle", "operation_mode", "start_time", "status"],
        order_by="start_time asc"
    )
    
    # Get pending spot checks (if any assigned)
    pending_checks = frappe.get_all(
        "Spot Check",
        filters={
            "driver": employee,
            "date": today,
            "docstatus": 0
        },
        fields=["name", "vehicle", "location"],
        limit=5
    )
    
    # Get recent incidents involving driver via Incident Participant child table
    incident_participants = frappe.get_all(
        "Incident Participant",
        filters={
            "employee": employee,
            "parenttype": "Safety Incident"
        },
        fields=["parent"],
        distinct=True
    )
    
    incident_names = [p.parent for p in incident_participants]
    
    recent_incidents = []
    if incident_names:
        recent_incidents = frappe.get_all(
            "Safety Incident",
            filters={
                "name": ["in", incident_names],
                "incident_date": [">=", frappe.utils.add_days(today, -7)]
            },
            fields=["name", "title", "incident_date", "severity", "status"],
            order_by="incident_date desc",
            limit=5
        )
    
    # Get driver qualification status
    qualification = frappe.db.get_value(
        "Driver Qualification",
        {"employee": employee, "status": "Active"},
        ["license_no", "expiry_date", "status"],
        as_dict=True
    )
    
    return {
        "employee": employee,
        "journey_plans": journey_plans,
        "operation_plans": operation_plans,
        "pending_checks": pending_checks,
        "recent_incidents": recent_incidents,
        "qualification": qualification,
        "timestamp": now_datetime()
    }


@frappe.whitelist()
def get_journey_details(journey_plan_name):
    """Get full journey plan details with route waypoints"""
    journey = frappe.get_doc("Journey Plan", journey_plan_name)
    
    # Get route details with waypoints
    route = None
    if journey.route:
        route = frappe.get_doc("Route Planning", journey.route)
    
    return {
        "journey": journey.as_dict(),
        "route": route.as_dict() if route else None,
        "vehicle_details": get_vehicle_info(journey.vehicle) if journey.vehicle else None
    }


@frappe.whitelist()
def start_trip(journey_plan_name, odometer_reading=None, location_data=None):
    """Mark journey as started"""
    journey = frappe.get_doc("Journey Plan", journey_plan_name)
    
    # Create movement log for check-in
    movement = frappe.get_doc({
        "doctype": "Movement Log",
        "vehicle": journey.vehicle,
        "operation_plan": None,  # Link if available
        "state": "Check-In",
        "event_time": now_datetime(),
        "location_lat": location_data.get("lat") if location_data else None,
        "location_lng": location_data.get("lng") if location_data else None,
        "notes": f"Trip started by driver for Journey Plan {journey_plan_name}"
    })
    movement.insert(ignore_permissions=True)
    
    # Log fuel if odometer provided
    if odometer_reading and journey.vehicle:
        try:
            last_fuel = frappe.get_last_doc("Fuel Log", filters={"vehicle": journey.vehicle})
            if last_fuel:
                # Could calculate consumption here
                pass
        except:
            pass
    
    return {
        "success": True,
        "movement_log": movement.name,
        "message": _("Trip started successfully")
    }


@frappe.whitelist()
def complete_trip(journey_plan_name, odometer_reading=None, location_data=None, notes=None):
    """Mark journey as completed"""
    journey = frappe.get_doc("Journey Plan", journey_plan_name)
    journey.end_time = now_datetime()
    journey.save(ignore_permissions=True)
    
    # Create movement log for delivery confirmation
    movement = frappe.get_doc({
        "doctype": "Movement Log",
        "vehicle": journey.vehicle,
        "state": "Delivered",
        "event_time": now_datetime(),
        "location_lat": location_data.get("lat") if location_data else None,
        "location_lng": location_data.get("lng") if location_data else None,
        "notes": notes or f"Trip completed for Journey Plan {journey_plan_name}"
    })
    movement.insert(ignore_permissions=True)
    
    return {
        "success": True,
        "message": _("Trip completed successfully")
    }


@frappe.whitelist()
def submit_spot_check(vehicle, location=None, notes=None, photos=None):
    """Submit vehicle spot check"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    spot_check = frappe.get_doc({
        "doctype": "Spot Check",
        "date": getdate(),
        "vehicle": vehicle,
        "driver": employee,
        "location": location,
        "notes": notes
    })
    
    if photos:
        for photo in photos:
            spot_check.append("photos", {
                "image": photo.get("image"),
                "caption": photo.get("caption")
            })
    
    spot_check.insert(ignore_permissions=True)
    
    return {
        "success": True,
        "spot_check": spot_check.name,
        "message": _("Spot check submitted successfully")
    }


@frappe.whitelist()
def report_incident(data):
    """Create safety incident report"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    incident = frappe.get_doc({
        "doctype": "Safety Incident",
        "title": data.get("title"),
        "incident_date": data.get("incident_date") or now_datetime(),
        "severity": data.get("severity", "minor"),
        "status": "Open",
        "vehicle": data.get("vehicle"),
        "route": data.get("route"),
        "location": data.get("location"),
        "description": data.get("description")
    })
    
    # Add reporter as participant
    incident.append("participants", {
        "employee": employee,
        "role": "driver",
        "notes": "Incident reporter"
    })
    
    incident.insert(ignore_permissions=True)
    
    return {
        "success": True,
        "incident": incident.name,
        "message": _("Incident reported successfully")
    }


@frappe.whitelist()
def log_fuel(vehicle, liters, price_per_liter, odometer, station=None, location_data=None):
    """Log fuel entry"""
    fuel_log = frappe.get_doc({
        "doctype": "Fuel Log",
        "vehicle": vehicle,
        "odometer": odometer,
        "liters": liters,
        "price_per_liter": price_per_liter,
        "total_cost": liters * price_per_liter,
        "station": station,
        "geohash": location_data.get("geohash") if location_data else None,
        "date": getdate()
    })
    
    fuel_log.insert(ignore_permissions=True)
    
    return {
        "success": True,
        "fuel_log": fuel_log.name,
        "total_cost": fuel_log.total_cost,
        "message": _("Fuel logged successfully")
    }


def get_vehicle_info(vehicle_name):
    """Get vehicle details"""
    vehicle = frappe.get_doc("Vehicle", vehicle_name)
    
    # Get last fuel log
    last_fuel = None
    try:
        last_fuel = frappe.get_last_doc("Fuel Log", filters={"vehicle": vehicle_name})
    except:
        pass
    
    # Get pending maintenance
    pending_maintenance = frappe.get_all(
        "Maintenance Work Order",
        filters={
            "vehicle": vehicle_name,
            "status": ["in", ["Open", "In Progress"]]
        },
        fields=["name", "status", "planned_date", "cost"]
    )
    
    return {
        "vehicle": vehicle.as_dict(),
        "last_fuel": last_fuel.as_dict() if last_fuel else None,
        "pending_maintenance": pending_maintenance
    }


@frappe.whitelist()
def get_offline_sync_data(last_sync=None):
    """Get essential data for offline operation"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    # Get upcoming trips (next 7 days)
    upcoming_trips = frappe.get_all(
        "Journey Plan",
        filters={
            "driver": employee,
            "start_time": [">=", getdate()],
            "start_time": ["<=", frappe.utils.add_days(getdate(), 7)]
        },
        fields=["*"]
    )
    
    # Get routes for these trips
    route_names = [trip.get("route") for trip in upcoming_trips if trip.get("route")]
    routes = []
    if route_names:
        routes = frappe.get_all(
            "Route Planning",
            filters={"name": ["in", route_names]},
            fields=["*"]
        )
    
    # Get assigned vehicles
    vehicles = []
    vehicle_names = list(set([trip.get("vehicle") for trip in upcoming_trips if trip.get("vehicle")]))
    if vehicle_names:
        vehicles = frappe.get_all(
            "Vehicle",
            filters={"name": ["in", vehicle_names]},
            fields=["name", "license_plate", "make", "model"]
        )
    
    return {
        "trips": upcoming_trips,
        "routes": routes,
        "vehicles": vehicles,
        "sync_timestamp": now_datetime()
    }


@frappe.whitelist(allow_guest=False, methods=['POST'])
def send_sos_alert(location_data, notes=''):
    """Send SOS emergency alert"""
    # Parse location_data if it's a string
    if isinstance(location_data, str):
        import json
        location_data = json.loads(location_data)
    
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    # Get current journey if any
    current_journey = frappe.db.get_value(
        "Journey Plan",
        {
            "driver": employee,
            "start_time": ["<=", now_datetime()],
            "end_time": [">=", now_datetime()]
        },
        ["name", "vehicle", "route"]
    )
    
    # Create SOS Event
    sos = frappe.get_doc({
        "doctype": "SOS Event",
        "reporter_employee": employee,
        "vehicle": current_journey.get("vehicle") if current_journey else None,
        "route": current_journey.get("route") if current_journey else None,
        "lat": location_data.get("lat") if location_data else None,
        "lng": location_data.get("lng") if location_data else None,
        "status": "Open",
        "notes": notes,
        "created_at": now_datetime()
    })
    sos.insert(ignore_permissions=True)
    
    # TODO: Send push notification to operations team
    # TODO: Send SMS to emergency contacts
    
    return {
        "success": True,
        "sos_event": sos.name,
        "message": _("SOS alert sent successfully. Help is on the way.")
    }


@frappe.whitelist()
def get_messages():
    """Get driver messages/communications"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    # Get messages from Communication doctype
    messages = frappe.get_all(
        "Communication",
        filters={
            "reference_doctype": "Employee",
            "reference_name": employee,
            "communication_type": ["in", ["Communication", "Chat"]]
        },
        fields=["name", "subject", "content", "sender", "creation", "sent_or_received"],
        order_by="creation desc",
        limit=50
    )
    
    return messages


@frappe.whitelist()
def send_message(recipient_type, recipient_id, message, timestamp=None):
    """Send message to operations control"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    comm = frappe.get_doc({
        "doctype": "Communication",
        "communication_type": "Chat",
        "subject": f"Message from Driver - {employee}",
        "content": message,
        "sender": frappe.session.user,
        "sent_or_received": "Sent",
        "reference_doctype": "Employee",
        "reference_name": employee
    })
    comm.insert(ignore_permissions=True)
    
    return {
        "success": True,
        "message_id": comm.name,
        "timestamp": comm.creation
    }


@frappe.whitelist()
def get_notifications():
    """Get driver notifications"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    notifications = frappe.get_all(
        "Notification Log",
        filters={
            "for_user": frappe.session.user,
            "read": 0
        },
        fields=["name", "subject", "email_content", "document_type", "document_name", "creation"],
        order_by="creation desc",
        limit=20
    )
    
    return notifications


@frappe.whitelist()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    notification = frappe.get_doc("Notification Log", notification_id)
    notification.read = 1
    notification.save(ignore_permissions=True)
    
    return {"success": True}


@frappe.whitelist()
def get_driver_incidents():
    """Get incidents involving driver"""
    employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    
    incidents = frappe.get_all(
        "Safety Incident",
        filters={
            "participants": ["like", f"%{employee}%"]
        },
        fields=["name", "title", "incident_date", "severity", "status", "description"],
        order_by="incident_date desc"
    )
    
    return incidents


@frappe.whitelist()
def get_cargo_consignments(trip_id):
    """Get cargo consignments for a trip"""
    # Get consignments linked to this journey
    consignments = frappe.get_all(
        "Cargo Consignment",
        filters={
            "journey_plan": trip_id
        },
        fields=["name", "consignment_no", "sender", "receiver", "weight", "status", "tracking_no"],
        order_by="creation"
    )
    
    return consignments


@frappe.whitelist()
def scan_cargo_barcode(barcode, trip_id):
    """Scan and validate cargo barcode"""
    # Find consignment by barcode/tracking number
    consignment = frappe.db.get_value(
        "Cargo Consignment",
        {"tracking_no": barcode},
        ["name", "consignment_no", "sender", "receiver", "status"],
        as_dict=True
    )
    
    if not consignment:
        frappe.throw(_("Consignment not found with tracking number: {0}").format(barcode))
    
    return {
        "success": True,
        "consignment": consignment,
        "message": _("Consignment scanned successfully")
    }


@frappe.whitelist()
def update_delivery_status(consignment_id, status, location_data, signature=None, timestamp=None):
    """Update cargo delivery status"""
    consignment = frappe.get_doc("Cargo Consignment", consignment_id)
    consignment.status = status
    
    if location_data:
        consignment.delivery_lat = location_data.get("lat")
        consignment.delivery_lng = location_data.get("lng")
    
    if signature:
        # TODO: Save signature as attachment
        pass
    
    consignment.delivery_time = timestamp or now_datetime()
    consignment.save(ignore_permissions=True)
    
    return {
        "success": True,
        "message": _("Delivery status updated successfully")
    }


@frappe.whitelist()
def get_passenger_manifest(trip_id):
    """Get passenger manifest for a trip"""
    # Get passenger trip
    passenger_trip = frappe.db.get_value(
        "Passenger Trip",
        {"journey_plan": trip_id},
        ["name", "total_seats", "available_seats"],
        as_dict=True
    )
    
    if not passenger_trip:
        return {"manifest": None, "bookings": []}
    
    # Get bookings for this trip
    bookings = frappe.get_all(
        "Passenger Booking",
        filters={
            "trip": passenger_trip.name
        },
        fields=["name", "passenger_name", "seat_number", "ticket_code", "status", "booking_time"],
        order_by="seat_number"
    )
    
    return {
        "manifest": passenger_trip,
        "bookings": bookings
    }


@frappe.whitelist()
def scan_passenger_ticket(ticket_code, trip_id):
    """Scan and validate passenger ticket"""
    booking = frappe.db.get_value(
        "Passenger Booking",
        {"ticket_code": ticket_code},
        ["name", "passenger_name", "seat_number", "status"],
        as_dict=True
    )
    
    if not booking:
        frappe.throw(_("Invalid ticket code: {0}").format(ticket_code))
    
    if booking.status == "Boarded":
        return {
            "success": False,
            "message": _("Passenger already boarded"),
            "booking": booking
        }
    
    # Update status to boarded
    frappe.db.set_value("Passenger Booking", booking.name, "status", "Boarded")
    frappe.db.set_value("Passenger Booking", booking.name, "boarding_time", now_datetime())
    
    return {
        "success": True,
        "booking": booking,
        "message": _("Passenger checked in successfully")
    }


@frappe.whitelist()
def update_boarding_status(booking_id, status, timestamp=None):
    """Update passenger boarding status"""
    booking = frappe.get_doc("Passenger Booking", booking_id)
    booking.status = status
    
    if status == "Boarded":
        booking.boarding_time = timestamp or now_datetime()
    
    booking.save(ignore_permissions=True)
    
    return {
        "success": True,
        "message": _("Boarding status updated")
    }