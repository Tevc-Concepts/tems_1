"""
Landing page controller for TEMS
Provides context for the main landing page
"""

import frappe
from frappe import _

def get_context(context):
    """Prepare context for landing page"""
    
    context.no_cache = 1  # Don't cache for now to see changes
    context.show_sidebar = False
    
    # Set page metadata
    context.title = _("TEMS - Transport Excellence Management System")
    context.description = _("Comprehensive fleet, operations, safety, and finance management for African transport enterprises")
    
    # Allow guest access
    frappe.flags.ignore_permissions = True
    
    # Get live metrics (will be fetched via AJAX for real-time updates)
    try:
        context.metrics = get_platform_metrics()
    except Exception as e:
        frappe.log_error(f"Error in landing page metrics: {str(e)}")
        context.metrics = {}
    
    # Get modules data
    context.modules = get_modules_data()
    
    return context


def get_platform_metrics():
    """Get real-time platform metrics"""
    
    try:
        # Active vehicles count
        active_vehicles = frappe.db.count("Vehicle", {
            "docstatus": ["!=", 2],
            "vehicle_state": ["in", ["Active", "In Transit", "On Route","Arrival"]]
        })
        
        # Ongoing trips
        ongoing_trips = frappe.db.count("Operation Plan", {
            "docstatus": 1,
            "status": ["in", ["In Progress", "Active"]]
        })
        
        # Active consignments
        active_consignments = frappe.db.count("Cargo Consignment", {
            "docstatus": ["!=", 2],
            "status": ["in", ["In Transit", "Processing", "At Terminal"]]
        })
        
        # Passengers today
        from frappe.utils import today
        passengers_today = frappe.db.sql("""
            SELECT COALESCE(SUM(passenger_count), 0)
            FROM `tabPassenger Trip`
            WHERE DATE(trip_date) = %s
            AND docstatus != 2
        """, today())[0][0] or 0
        
        # Safety incidents (Month to Date)
        from frappe.utils import get_first_day
        first_day = get_first_day(today())
        safety_incidents = frappe.db.count("Incident Report", {
            "incident_date": [">=", first_day],
            "docstatus": ["!=", 2]
        })
        
        # Fleet utilization
        total_vehicles = frappe.db.count("Vehicle", {"docstatus": ["!=", 2]})
        fleet_utilization = round((active_vehicles / total_vehicles * 100), 1) if total_vehicles > 0 else 0
        
        # On-time performance
        on_time_trips = frappe.db.sql("""
            SELECT COUNT(*) 
            FROM `tabOperation Plan`
            WHERE docstatus = 1
            AND DATE(actual_end_time) = %s
            AND actual_end_time <= planned_end_time
        """, today())[0][0] or 0
        
        total_completed_today = frappe.db.sql("""
            SELECT COUNT(*) 
            FROM `tabOperation Plan`
            WHERE docstatus = 1
            AND DATE(actual_end_time) = %s
        """, today())[0][0] or 0
        
        on_time_rate = round((on_time_trips / total_completed_today * 100), 1) if total_completed_today > 0 else 0
        
        # Average response time (in minutes) for SOS events
        avg_response = frappe.db.sql("""
            SELECT AVG(TIMESTAMPDIFF(MINUTE, creation, resolution_time))
            FROM `tabSOS Event`
            WHERE resolution_time IS NOT NULL
            AND DATE(creation) = %s
        """, today())[0][0] or 0
        
        return {
            "active_vehicles": int(active_vehicles),
            "ongoing_trips": int(ongoing_trips),
            "active_consignments": int(active_consignments),
            "passengers_today": int(passengers_today),
            "safety_incidents": int(safety_incidents),
            "fleet_utilization": fleet_utilization,
            "on_time_rate": on_time_rate,
            "avg_response_time": round(avg_response, 1)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching platform metrics: {str(e)}")
        return {
            "active_vehicles": 0,
            "ongoing_trips": 0,
            "active_consignments": 0,
            "passengers_today": 0,
            "safety_incidents": 0,
            "fleet_utilization": 0,
            "on_time_rate": 0,
            "avg_response_time": 0
        }


def get_modules_data():
    """Get modules configuration for landing page"""
    
    return [
        {
            "id": "governance",
            "title": "Leadership & Governance",
            "description": "Strategic planning, KPIs, policy management, and executive dashboards",
            "icon": "🛡️",
            "color": "purple",
            "route": "/modules/governance",
            "features": [
                "Vision & Mission Tracking",
                "Strategic Goals & KPIs",
                "Policy Management",
                "Compliance Audits"
            ]
        },
        {
            "id": "operations",
            "title": "Operations Management",
            "description": "Real-time dispatch, route optimization, and operational excellence",
            "icon": "🚚",
            "color": "blue",
            "route": "/modules/operations",
            "features": [
                "Trip Management",
                "Route Optimization",
                "Real-time Tracking",
                "Dispatch Control"
            ]
        },
        {
            "id": "fleet",
            "title": "Fleet Management",
            "description": "Asset lifecycle, maintenance scheduling, and utilization tracking",
            "icon": "🔧",
            "color": "green",
            "route": "/modules/fleet",
            "features": [
                "Asset Management",
                "Maintenance Scheduling",
                "Utilization Tracking",
                "Work Order Management"
            ]
        },
        {
            "id": "safety",
            "title": "Safety & Risk",
            "description": "Incident management, risk assessments, and compliance monitoring",
            "icon": "⚠️",
            "color": "red",
            "route": "/modules/safety",
            "features": [
                "Incident Reporting",
                "Risk Assessments",
                "Safety Audits",
                "Driver Competence"
            ]
        },
        {
            "id": "finance",
            "title": "Finance & Profitability",
            "description": "Cost tracking, revenue management, and profitability analysis",
            "icon": "💰",
            "color": "yellow",
            "route": "/modules/finance",
            "features": [
                "Cost & Revenue Ledger",
                "Profitability Analysis",
                "Journey Costing",
                "Financial Reports"
            ]
        },
        {
            "id": "cargo",
            "title": "Cargo Logistics",
            "description": "Freight management, consignment tracking, and load optimization",
            "icon": "📦",
            "color": "orange",
            "route": "/modules/cargo",
            "features": [
                "Consignment Tracking",
                "Load Optimization",
                "Freight Management",
                "Documentation"
            ]
        },
        {
            "id": "passenger",
            "title": "Passenger Transport",
            "description": "Booking systems, seat management, and passenger services",
            "icon": "👥",
            "color": "indigo",
            "route": "/modules/passenger",
            "features": [
                "Booking Management",
                "Seat Allocation",
                "Ticketing",
                "Passenger Manifest"
            ]
        },
        {
            "id": "tyre",
            "title": "Tyre Management",
            "description": "Tyre lifecycle tracking, predictive maintenance, and cost analysis",
            "icon": "⚙️",
            "color": "gray",
            "route": "/modules/tyre",
            "features": [
                "Lifecycle Tracking",
                "Pressure Monitoring",
                "Cost Analysis",
                "Rotation Scheduling"
            ]
        },
        {
            "id": "ai",
            "title": "AI & Insights",
            "description": "Machine learning predictions, anomaly detection, and analytics",
            "icon": "🤖",
            "color": "pink",
            "route": "/modules/ai",
            "features": [
                "Predictive Maintenance",
                "Demand Forecasting",
                "Anomaly Detection",
                "Smart Alerts"
            ]
        },
        {
            "id": "people",
            "title": "People & HR",
            "description": "Recruitment, training, competency management, and performance tracking",
            "icon": "👔",
            "color": "teal",
            "route": "/modules/people",
            "features": [
                "Recruitment",
                "Training Records",
                "Competency Matrix",
                "Performance Reviews"
            ]
        },
        {
            "id": "trade",
            "title": "Cross-Border Trade",
            "description": "Border crossing management, customs clearance, and compliance",
            "icon": "🌍",
            "color": "blue",
            "route": "/modules/trade",
            "features": [
                "Border Crossings",
                "Customs Clearance",
                "Trade Lanes",
                "Documentation"
            ]
        },
        {
            "id": "climate",
            "title": "Climate & Sustainability",
            "description": "Emissions tracking, carbon footprint analysis, and eco-routing",
            "icon": "🌱",
            "color": "green",
            "route": "/modules/climate",
            "features": [
                "Emissions Tracking",
                "Carbon Footprint",
                "Eco-routing",
                "Climate Alerts"
            ]
        },
        {
            "id": "supply-chain",
            "title": "Supply Chain",
            "description": "Procurement, inventory management, and supplier performance",
            "icon": "📊",
            "color": "purple",
            "route": "/modules/supply-chain",
            "features": [
                "Procurement",
                "Inventory Management",
                "Supplier Ratings",
                "Logistics"
            ]
        }
    ]


@frappe.whitelist(allow_guest=True)
def get_live_metrics():
    """API endpoint for fetching live metrics via AJAX"""
    return get_platform_metrics()
