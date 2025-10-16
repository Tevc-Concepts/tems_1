# Adjust route pricing based on AI demand forecasts.

import frappe
from frappe.utils import getdate
from tems.tems_ai.handlers.finance_ai import optimize_pricing
from tems.tems_ai.handlers.operations_ai import predict_vehicle_demand

@frappe.whitelist()
def get_recommended_price(route, date):
    #Get AI-recommended pricing for a route.
    # Determine season based on date
    date_obj = getdate(date)
    if not date_obj:
        frappe.throw("Invalid date provided.")
    month = date_obj.month

    season = "peak" if month in [12, 1, 7, 8] else "regular"
    
    # Get pricing recommendation
    pricing = optimize_pricing(route, season)
    
    # Get demand forecast to adjust further
    region = route.split("-")[0]  # Extract origin
    demand = predict_vehicle_demand(region, date_range=7)
    
    # Adjust price based on demand
    base_price = pricing.get("recommended_price", 0)
    demand_forecast = demand.get("forecast", [{}])[0]
    demand_level = demand_forecast.get("predicted_demand", 0)
    
    # Higher demand = higher price
    if demand_level > 20:
        final_price = base_price * 1.1
        demand_note = "High demand period"
    elif demand_level < 10:
        final_price = base_price * 0.9
        demand_note = "Low demand period"
    else:
        final_price = base_price
        demand_note = "Normal demand"
    
    return {
        "route": route,
        "date": date,
        "season": season,
        "base_price": base_price,
        "recommended_price": final_price,
        "demand_note": demand_note,
        "confidence": pricing.get("confidence", 0)
    }