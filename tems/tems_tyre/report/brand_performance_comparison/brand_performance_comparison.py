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
        {"label": _("Brand"), "fieldname": "brand", "fieldtype": "Data", "width": 120},
        {"label": _("Total Tyres"), "fieldname": "total_tyres", "fieldtype": "Int", "width": 100},
        {"label": _("Active Tyres"), "fieldname": "active_tyres", "fieldtype": "Int", "width": 100},
        {"label": _("Avg Health Index"), "fieldname": "avg_health", "fieldtype": "Float", "width": 120},
        {"label": _("Avg Cost per km"), "fieldname": "avg_cost_per_km", "fieldtype": "Currency", "width": 120},
        {"label": _("Total Mileage"), "fieldname": "total_mileage", "fieldtype": "Float", "width": 120},
        {"label": _("Avg Lifespan (km)"), "fieldname": "avg_lifespan", "fieldtype": "Float", "width": 120},
        {"label": _("Total Investment"), "fieldname": "total_investment", "fieldtype": "Currency", "width": 120},
        {"label": _("Performance Score"), "fieldname": "performance_score", "fieldtype": "Float", "width": 120},
        {"label": _("Recommendation"), "fieldname": "recommendation", "fieldtype": "Data", "width": 150}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_calculator import compare_tyre_performance
    
    # Get all brands
    brands = frappe.db.sql("""
        SELECT DISTINCT brand 
        FROM `tabTyre` 
        WHERE brand IS NOT NULL AND brand != ''
        ORDER BY brand
    """, as_list=True)
    
    data = []
    for (brand,) in brands:
        # Get brand statistics
        brand_stats = frappe.db.sql("""
            SELECT 
                COUNT(*) as total_tyres,
                COUNT(CASE WHEN status IN ('Installed', 'In Stock') THEN 1 END) as active_tyres,
                AVG(CASE WHEN ai_health_index IS NOT NULL THEN ai_health_index END) as avg_health,
                SUM(current_mileage) as total_mileage,
                SUM(cost) as total_investment,
                AVG(CASE WHEN current_mileage > 0 THEN current_mileage END) as avg_lifespan
            FROM `tabTyre`
            WHERE brand = %s
        """, (brand,), as_dict=True)[0]
        
        # Calculate cost per km
        total_cost = flt(brand_stats.total_investment)
        total_km = flt(brand_stats.total_mileage)
        avg_cost_per_km = total_cost / total_km if total_km > 0 else 0
        
        # Calculate performance score (0-100)
        # Higher health + lower cost per km + higher lifespan = better score
        health_score = flt(brand_stats.avg_health, 2) or 50
        cost_score = min(100, (1 / (avg_cost_per_km + 0.01)) * 10) if avg_cost_per_km > 0 else 50
        lifespan_score = min(100, (flt(brand_stats.avg_lifespan) / 1000)) if brand_stats.avg_lifespan else 50
        
        performance_score = (health_score * 0.4) + (cost_score * 0.3) + (lifespan_score * 0.3)
        
        # Generate recommendation
        if performance_score >= 80:
            recommendation = "Excellent - Recommended"
        elif performance_score >= 60:
            recommendation = "Good - Consider"
        elif performance_score >= 40:
            recommendation = "Average - Monitor"
        else:
            recommendation = "Below Average - Review"
        
        data.append({
            "brand": brand,
            "total_tyres": int(brand_stats.total_tyres),
            "active_tyres": int(brand_stats.active_tyres),
            "avg_health": round(health_score, 2),
            "avg_cost_per_km": round(avg_cost_per_km, 2),
            "total_mileage": round(total_km, 2),
            "avg_lifespan": round(flt(brand_stats.avg_lifespan), 2),
            "total_investment": total_cost,
            "performance_score": round(performance_score, 2),
            "recommendation": recommendation
        })
    
    # Sort by performance score descending
    data = sorted(data, key=lambda x: x['performance_score'], reverse=True)
    
    return data

def get_chart_data(data):
    labels = [d["brand"] for d in data[:10]]
    health_values = [d["avg_health"] for d in data[:10]]
    cost_values = [d["avg_cost_per_km"] for d in data[:10]]
    
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Avg Health Index",
                    "values": health_values
                },
                {
                    "name": "Cost per km (scaled)",
                    "values": [v * 10 for v in cost_values]  # Scale for visibility
                }
            ]
        },
        "type": "bar",
        "colors": ["#1ABC9C", "#E74C3C"]
    }
