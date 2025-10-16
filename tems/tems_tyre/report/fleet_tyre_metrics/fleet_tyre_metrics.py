# Copyright (c) 2025, Tevc Concepts Limited and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    summary = get_summary_data(data)
    chart = get_chart_data(data)
    
    return columns, data, None, chart, summary

def get_columns():
    return [
        {"label": _("Metric"), "fieldname": "metric", "fieldtype": "Data", "width": 250},
        {"label": _("Value"), "fieldname": "value", "fieldtype": "Data", "width": 150},
        {"label": _("Unit"), "fieldname": "unit", "fieldtype": "Data", "width": 100},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": _("Trend"), "fieldname": "trend", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    from tems.tems_tyre.utils.tyre_calculator import calculate_fleet_tyre_metrics
    
    vehicle = filters.get("vehicle") if filters else None
    metrics = calculate_fleet_tyre_metrics(vehicle)
    
    data = []
    
    # Fleet Overview
    data.append({
        "metric": "Total Active Tyres",
        "value": str(metrics.get("total_tyres", 0)),
        "unit": "tyres",
        "status": "Active",
        "trend": "→"
    })
    
    data.append({
        "metric": "Tyres on Vehicles",
        "value": str(metrics.get("installed_tyres", 0)),
        "unit": "tyres",
        "status": "Installed",
        "trend": "→"
    })
    
    data.append({
        "metric": "Tyres in Stock",
        "value": str(metrics.get("stock_tyres", 0)),
        "unit": "tyres",
        "status": "Available",
        "trend": "→"
    })
    
    # Health Metrics
    avg_health = metrics.get("avg_health_index", 0)
    health_status = "Good" if avg_health >= 70 else "Caution" if avg_health >= 50 else "Critical"
    
    data.append({
        "metric": "Average Health Index",
        "value": f"{avg_health:.1f}",
        "unit": "score",
        "status": health_status,
        "trend": get_health_trend(avg_health)
    })
    
    # Alert Metrics
    critical_tyres = metrics.get("critical_tyres", 0)
    alert_status = "Critical" if critical_tyres > 5 else "Warning" if critical_tyres > 0 else "OK"
    
    data.append({
        "metric": "Tyres Needing Immediate Attention",
        "value": str(critical_tyres),
        "unit": "tyres",
        "status": alert_status,
        "trend": "⚠️" if critical_tyres > 0 else "✓"
    })
    
    data.append({
        "metric": "Replacement Due (14 days)",
        "value": str(metrics.get("replacement_due_soon", 0)),
        "unit": "tyres",
        "status": "Scheduled",
        "trend": "→"
    })
    
    # Financial Metrics
    data.append({
        "metric": "Total Tyre Investment",
        "value": f"{metrics.get('total_investment', 0):,.2f}",
        "unit": "currency",
        "status": "Invested",
        "trend": "↑"
    })
    
    avg_cost_per_km = metrics.get("avg_cost_per_km", 0)
    cost_status = "Excellent" if avg_cost_per_km < 3 else "Good" if avg_cost_per_km < 5 else "Review"
    
    data.append({
        "metric": "Average Cost per km",
        "value": f"{avg_cost_per_km:.2f}",
        "unit": "currency/km",
        "status": cost_status,
        "trend": get_cost_trend(avg_cost_per_km)
    })
    
    data.append({
        "metric": "Monthly Tyre Spend (Current)",
        "value": f"{metrics.get('monthly_spend', 0):,.2f}",
        "unit": "currency",
        "status": "Current Month",
        "trend": "→"
    })
    
    # Performance Metrics
    data.append({
        "metric": "Total Fleet Mileage on Tyres",
        "value": f"{metrics.get('total_mileage', 0):,.0f}",
        "unit": "km",
        "status": "Cumulative",
        "trend": "↑"
    })
    
    avg_lifespan = metrics.get("avg_tyre_lifespan", 0)
    lifespan_status = "Excellent" if avg_lifespan > 80000 else "Good" if avg_lifespan > 50000 else "Review"
    
    data.append({
        "metric": "Average Tyre Lifespan",
        "value": f"{avg_lifespan:,.0f}",
        "unit": "km",
        "status": lifespan_status,
        "trend": get_lifespan_trend(avg_lifespan)
    })
    
    # Maintenance Metrics
    data.append({
        "metric": "Inspections This Month",
        "value": str(metrics.get("inspections_this_month", 0)),
        "unit": "inspections",
        "status": "Completed",
        "trend": "→"
    })
    
    data.append({
        "metric": "Rotations This Month",
        "value": str(metrics.get("rotations_this_month", 0)),
        "unit": "rotations",
        "status": "Completed",
        "trend": "→"
    })
    
    data.append({
        "metric": "Tyres Disposed This Month",
        "value": str(metrics.get("disposals_this_month", 0)),
        "unit": "tyres",
        "status": "End of Life",
        "trend": "→"
    })
    
    # Sensor Metrics
    sensor_active = metrics.get("sensors_active", 0)
    sensor_total = metrics.get("sensors_total", 0)
    sensor_status = "OK" if sensor_active == sensor_total else "Check Required"
    
    data.append({
        "metric": "Active Sensor Coverage",
        "value": f"{sensor_active}/{sensor_total}",
        "unit": "sensors",
        "status": sensor_status,
        "trend": "→"
    })
    
    return data

def get_summary_data(data):
    """Generate summary cards for the report"""
    summary = []
    
    # Extract key metrics
    for row in data:
        if row["metric"] == "Average Health Index":
            summary.append({
                "value": row["value"],
                "label": "Fleet Health",
                "datatype": "Data",
                "indicator": "Green" if float(row["value"]) >= 70 else "Orange" if float(row["value"]) >= 50 else "Red"
            })
        elif row["metric"] == "Tyres Needing Immediate Attention":
            summary.append({
                "value": row["value"],
                "label": "Action Required",
                "datatype": "Int",
                "indicator": "Red" if int(row["value"]) > 0 else "Green"
            })
        elif row["metric"] == "Average Cost per km":
            summary.append({
                "value": row["value"],
                "label": "Avg Cost/km",
                "datatype": "Currency",
                "indicator": "Green" if float(row["value"]) < 5 else "Orange"
            })
    
    return summary

def get_chart_data(data):
    """Generate chart for key metrics"""
    labels = []
    values = []
    
    # Select key metrics for chart
    chart_metrics = [
        "Average Health Index",
        "Total Active Tyres",
        "Tyres Needing Immediate Attention",
        "Average Cost per km"
    ]
    
    for row in data:
        if row["metric"] in chart_metrics:
            labels.append(row["metric"])
            try:
                values.append(float(row["value"].replace(",", "")))
            except:
                values.append(0)
    
    return {
        "data": {
            "labels": labels,
            "datasets": [{"values": values}]
        },
        "type": "bar",
        "colors": ["#3498DB"]
    }

def get_health_trend(health):
    """Determine health trend indicator"""
    if health >= 80:
        return "↑"
    elif health >= 60:
        return "→"
    else:
        return "↓"

def get_cost_trend(cost):
    """Determine cost trend indicator"""
    if cost < 3:
        return "↓"  # Low cost is good
    elif cost < 5:
        return "→"
    else:
        return "↑"  # High cost is bad

def get_lifespan_trend(lifespan):
    """Determine lifespan trend indicator"""
    if lifespan > 80000:
        return "↑"
    elif lifespan > 50000:
        return "→"
    else:
        return "↓"