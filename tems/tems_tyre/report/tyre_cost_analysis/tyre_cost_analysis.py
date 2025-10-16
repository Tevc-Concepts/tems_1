# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Tyre"), "fieldname": "tyre", "fieldtype": "Link", "options": "Tyre", "width": 120},
        {"label": _("Vehicle"), "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": _("Purchase Cost"), "fieldname": "purchase_cost", "fieldtype": "Currency", "width": 120},
        {"label": _("Maintenance Cost"), "fieldname": "maintenance_cost", "fieldtype": "Currency", "width": 120},
        {"label": _("Total Cost"), "fieldname": "total_cost", "fieldtype": "Currency", "width": 120},
        {"label": _("Mileage"), "fieldname": "mileage", "fieldtype": "Float", "width": 100},
        {"label": _("Cost per km"), "fieldname": "cost_per_km", "fieldtype": "Currency", "width": 100},
        {"label": _("ROI Status"), "fieldname": "roi_status", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_calculator import calculate_tyre_roi
    
    conditions = []
    if filters.get("vehicle"):
        conditions.append(f"vehicle = '{filters.get('vehicle')}'")
    if filters.get("brand"):
        conditions.append(f"brand = '{filters.get('brand')}'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    tyres = frappe.db.sql(f"""
        SELECT name, vehicle, brand, cost, current_mileage
        FROM `tabTyre`
        WHERE {where_clause}
        AND status != 'Disposed'
    """, as_dict=True)
    
    data = []
    for tyre in tyres:
        roi = calculate_tyre_roi(tyre.name)
        
        data.append({
            "tyre": tyre.name,
            "vehicle": tyre.vehicle,
            "purchase_cost": tyre.cost,
            "maintenance_cost": roi["purchase_cost"] - flt(tyre.cost),
            "total_cost": roi["purchase_cost"],
            "mileage": tyre.current_mileage,
            "cost_per_km": roi["cost_per_km"],
            "roi_status": roi["status"]
        })
    
    return data

def get_chart_data(data):
    labels = [d["tyre"] for d in data[:10]]
    values = [d["cost_per_km"] for d in data[:10]]
    
    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}]
        },
        "type": "bar",
        "colors": ["#FF5733"]
    }