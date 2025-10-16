# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

# import frappe
# Shows predicted replacement dates for all active tyres.

import frappe
from frappe import _
from frappe.utils import getdate, add_days

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _("Tyre"), "fieldname": "tyre", "fieldtype": "Link", "options": "Tyre", "width": 120},
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": _("Position"), "fieldname": "position", "fieldtype": "Data", "width": 100},
        {"label": _("Health Index"), "fieldname": "health_index", "fieldtype": "Int", "width": 90},
        {"label": _("Current Mileage"), "fieldname": "mileage", "fieldtype": "Float", "width": 100},
        {"label": _("Remaining km"), "fieldname": "remaining_km", "fieldtype": "Float", "width": 100},
        {"label": _("Days Until Replacement"), "fieldname": "days_until", "fieldtype": "Int", "width": 150},
        {"label": _("Predicted Date"), "fieldname": "predicted_date", "fieldtype": "Date", "width": 120},
        {"label": _("Priority"), "fieldname": "priority", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_calculator import predict_replacement_date
    
    # Get installed tyres
    tyres = frappe.db.sql("""
        SELECT 
            t.name as tyre,
            t.vehicle,
            t.current_mileage,
            t.ai_health_index,
            til.position
        FROM `tabTyre` t
        LEFT JOIN `tabTyre Installation Log` til ON til.tyre = t.name
        WHERE t.status = 'Installed'
        AND til.removed_date IS NULL
        ORDER BY t.ai_health_index ASC
    """, as_dict=True)
    
    data = []
    for tyre_info in tyres:
        prediction = predict_replacement_date(tyre_info.tyre)
        
        if prediction:
            days = prediction.get("days_until_replacement", 999)
            
            if days < 7:
                priority = "Critical"
            elif days < 30:
                priority = "High"
            elif days < 90:
                priority = "Medium"
            else:
                priority = "Low"
            
            data.append({
                "tyre": tyre_info.tyre,
                "vehicle": tyre_info.vehicle,
                "position": tyre_info.position,
                "health_index": tyre_info.ai_health_index,
                "mileage": tyre_info.current_mileage,
                "remaining_km": prediction.get("remaining_km", 0),
                "days_until": days,
                "predicted_date": add_days(None, days),
                "priority": priority
            })
    
    return data