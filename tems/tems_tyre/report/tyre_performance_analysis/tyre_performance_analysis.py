# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Tyre"), "fieldname": "tyre", "fieldtype": "Link", "options": "Tyre", "width": 120},
        {"label": _("Brand"), "fieldname": "brand", "fieldtype": "Data", "width": 100},
        {"label": _("Model"), "fieldname": "model", "fieldtype": "Data", "width": 100},
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": _("Health Index"), "fieldname": "health_index", "fieldtype": "Int", "width": 90},
        {"label": _("Condition"), "fieldname": "condition", "fieldtype": "Data", "width": 120},
        {"label": _("Mileage (km)"), "fieldname": "mileage", "fieldtype": "Float", "width": 100},
        {"label": _("Cost/km"), "fieldname": "cost_per_km", "fieldtype": "Currency", "width": 100},
        {"label": _("Tread (mm)"), "fieldname": "tread_depth", "fieldtype": "Float", "width": 90},
        {"label": _("Pressure (PSI)"), "fieldname": "pressure", "fieldtype": "Float", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

def get_conditions(filters):
	conditions = {}

	if filters.brand:
		conditions["brand"] = filters.brand

	if filters.vehicle:
		conditions["vehicle"] = filters.vehicle

	if filters.status:
		conditions["status"] = filters.status

	return conditions

def get_data(filters):
    from tems.tems_tyre.utils.tyre_analyzer import batch_analyze_fleet_tyres
    
    vehicle = filters.get("vehicle") if filters else None
    insights = batch_analyze_fleet_tyres(vehicle)
    
    data = []
    for insight in insights:
        data.append({
            "tyre": insight.get("tyre"),
            "brand": insight.get("brand"),
            "model": insight.get("model"),
            "vehicle": insight.get("vehicle"),
            "health_index": insight.get("health_index"),
            "condition": insight.get("condition"),
            "mileage": insight.get("current_mileage"),
            "cost_per_km": insight.get("cost_per_km"),
            "tread_depth": 0,  # Get from tyre doc
            "pressure": 0,  # Get from tyre doc
            "status": insight.get("status")
        })
    
    return data

