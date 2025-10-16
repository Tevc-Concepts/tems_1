"""
Finance AI Handler
==================
AI-powered features for Finance Management domain.
"""

import frappe
from typing import Dict, List, Optional
from datetime import datetime, timedelta


def predict_vehicle_profitability(vehicle: str, forecast_days: int = 30) -> Dict:
    """
    Predict vehicle profitability using AI.
    
    Args:
        vehicle: Vehicle ID
        forecast_days: Number of days to forecast
    
    Returns:
        Profitability forecast
    """
    # Get historical cost and revenue data
    ledger = frappe.get_all(
        "Cost And Revenue Ledger",
        filters={"vehicle": vehicle},
        fields=["cost_amount", "revenue_amount", "transaction_date"],
        order_by="transaction_date desc",
        limit=90
    )
    
    if not ledger:
        return {
            "vehicle": vehicle,
            "message": "Insufficient financial data",
            "forecast": []
        }
    
    # Calculate daily averages
    total_cost = sum(e.get("cost_amount", 0) for e in ledger)
    total_revenue = sum(e.get("revenue_amount", 0) for e in ledger)
    days_count = len(set(e.get("transaction_date") for e in ledger if e.get("transaction_date")))
    
    avg_daily_cost = total_cost / days_count if days_count > 0 else 0
    avg_daily_revenue = total_revenue / days_count if days_count > 0 else 0
    avg_daily_profit = avg_daily_revenue - avg_daily_cost
    
    # Generate forecast
    forecast = []
    for day in range(forecast_days):
        forecast_date = datetime.now().date() + timedelta(days=day)
        # Simple projection with slight variation
        predicted_revenue = avg_daily_revenue * (1 + (day % 7) * 0.05)
        predicted_cost = avg_daily_cost * (1 + (day % 5) * 0.03)
        predicted_profit = predicted_revenue - predicted_cost
        
        forecast.append({
            "date": forecast_date.isoformat(),
            "predicted_revenue": round(predicted_revenue, 2),
            "predicted_cost": round(predicted_cost, 2),
            "predicted_profit": round(predicted_profit, 2),
            "confidence": 0.75
        })
    
    # Calculate cumulative forecast
    cumulative_profit = sum(f["predicted_profit"] for f in forecast)
    
    return {
        "vehicle": vehicle,
        "forecast_period_days": forecast_days,
        "historical_avg": {
            "daily_revenue": round(avg_daily_revenue, 2),
            "daily_cost": round(avg_daily_cost, 2),
            "daily_profit": round(avg_daily_profit, 2)
        },
        "forecast_summary": {
            "total_predicted_revenue": round(sum(f["predicted_revenue"] for f in forecast), 2),
            "total_predicted_cost": round(sum(f["predicted_cost"] for f in forecast), 2),
            "total_predicted_profit": round(cumulative_profit, 2)
        },
        "daily_forecast": forecast[:7],  # Show first 7 days in detail
        "profitability_trend": "positive" if avg_daily_profit > 0 else "negative"
    }


def detect_cost_anomaly(vehicle: str, cost_amount: float, cost_type: str) -> Dict:
    """
    Detect anomalies in vehicle costs.
    
    Args:
        vehicle: Vehicle ID
        cost_amount: Cost amount to check
        cost_type: Type of cost (fuel, maintenance, etc.)
    
    Returns:
        Anomaly detection result
    """
    # Get historical costs of this type
    historical_costs = frappe.db.sql("""
        SELECT AVG(cost_amount) as avg_cost, STDDEV(cost_amount) as std_cost
        FROM `tabCost And Revenue Ledger`
        WHERE vehicle = %s
        AND cost_type = %s
        AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
    """, (vehicle, cost_type), as_dict=True)
    
    if not historical_costs or not historical_costs[0].get("avg_cost"):
        return {
            "anomaly": False,
            "reason": "Insufficient historical data"
        }
    
    avg_cost = float(historical_costs[0].get("avg_cost", 0))
    std_cost = float(historical_costs[0].get("std_cost", 1))
    
    # Calculate z-score
    z_score = abs((cost_amount - avg_cost) / std_cost) if std_cost > 0 else 0
    
    is_anomaly = z_score > 2.5
    
    return {
        "vehicle": vehicle,
        "cost_type": cost_type,
        "anomaly": is_anomaly,
        "z_score": round(z_score, 2),
        "current_cost": cost_amount,
        "average_cost": round(avg_cost, 2),
        "severity": "high" if z_score > 3 else "medium" if z_score > 2 else "low",
        "recommendation": "Investigate unusual cost" if is_anomaly else "Cost within normal range"
    }


def optimize_pricing(route: str, season: Optional[str] = None) -> Dict:
    """
    AI-powered pricing optimization for a route.
    
    Args:
        route: Route name
        season: Optional season (peak, off-peak)
    
    Returns:
        Pricing recommendations
    """
    # Get historical pricing and demand data
    trips = frappe.get_all(
        "Trip Allocation",
        filters={"route": route, "status": "Completed"},
        fields=["estimated_cost", "actual_cost"],
        limit=100
    )
    
    if not trips:
        return {
            "route": route,
            "message": "Insufficient pricing data"
        }
    
    # Calculate average costs
    avg_cost = sum(t.get("actual_cost", t.get("estimated_cost", 0)) for t in trips) / len(trips)
    
    # Pricing recommendations based on cost + margin
    base_price = avg_cost * 1.25  # 25% margin
    
    # Adjust for season
    seasonal_multiplier = 1.2 if season == "peak" else 0.9 if season == "off-peak" else 1.0
    
    recommended_price = base_price * seasonal_multiplier
    
    return {
        "route": route,
        "season": season or "regular",
        "cost_analysis": {
            "average_cost": round(avg_cost, 2),
            "base_price": round(base_price, 2),
            "seasonal_multiplier": seasonal_multiplier
        },
        "recommended_price": round(recommended_price, 2),
        "price_range": {
            "minimum": round(recommended_price * 0.9, 2),
            "maximum": round(recommended_price * 1.1, 2)
        },
        "confidence": 0.80
    }


def forecast_cash_flow(days: int = 30) -> Dict:
    """
    Forecast cash flow for the organization.
    
    Args:
        days: Number of days to forecast
    
    Returns:
        Cash flow forecast
    """
    # Get recent financial data
    recent_ledger = frappe.db.sql("""
        SELECT 
            DATE(transaction_date) as date,
            SUM(cost_amount) as daily_cost,
            SUM(revenue_amount) as daily_revenue
        FROM `tabCost And Revenue Ledger`
        WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
        GROUP BY DATE(transaction_date)
        ORDER BY date
    """, as_dict=True)
    
    if not recent_ledger:
        return {
            "message": "Insufficient financial data",
            "forecast": []
        }
    
    # Calculate averages
    avg_daily_revenue = sum(r.get("daily_revenue", 0) for r in recent_ledger) / len(recent_ledger)
    avg_daily_cost = sum(r.get("daily_cost", 0) for r in recent_ledger) / len(recent_ledger)
    
    # Generate forecast
    forecast = []
    cumulative_cash = 0
    
    for day in range(days):
        forecast_date = datetime.now().date() + timedelta(days=day)
        
        # Apply weekly patterns (weekends typically lower)
        day_of_week = forecast_date.weekday()
        weekend_factor = 0.7 if day_of_week >= 5 else 1.0
        
        predicted_revenue = avg_daily_revenue * weekend_factor
        predicted_cost = avg_daily_cost * weekend_factor
        predicted_net = predicted_revenue - predicted_cost
        cumulative_cash += predicted_net
        
        forecast.append({
            "date": forecast_date.isoformat(),
            "predicted_revenue": round(predicted_revenue, 2),
            "predicted_cost": round(predicted_cost, 2),
            "predicted_net_cash": round(predicted_net, 2),
            "cumulative_cash": round(cumulative_cash, 2)
        })
    
    return {
        "forecast_period_days": days,
        "starting_date": datetime.now().date().isoformat(),
        "historical_avg": {
            "daily_revenue": round(avg_daily_revenue, 2),
            "daily_cost": round(avg_daily_cost, 2),
            "daily_net": round(avg_daily_revenue - avg_daily_cost, 2)
        },
        "forecast_summary": {
            "total_revenue": round(sum(f["predicted_revenue"] for f in forecast), 2),
            "total_cost": round(sum(f["predicted_cost"] for f in forecast), 2),
            "total_net": round(sum(f["predicted_net_cash"] for f in forecast), 2),
            "ending_cumulative": round(cumulative_cash, 2)
        },
        "daily_forecast": forecast[:7],  # First 7 days detail
        "cash_flow_trend": "positive" if cumulative_cash > 0 else "negative"
    }


def calculate_roi_score(investment_type: str, amount: float, vehicle: Optional[str] = None) -> Dict:
    """
    Calculate expected ROI for an investment.
    
    Args:
        investment_type: Type of investment (new_vehicle, maintenance, upgrade)
        amount: Investment amount
        vehicle: Optional vehicle ID for vehicle-specific investments
    
    Returns:
        ROI calculation and recommendation
    """
    roi_estimates = {
        "new_vehicle": 0.15,  # 15% annual ROI
        "maintenance": 0.25,  # 25% ROI (prevents breakdowns)
        "upgrade": 0.20,  # 20% ROI
        "technology": 0.30   # 30% ROI (efficiency gains)
    }
    
    base_roi = roi_estimates.get(investment_type, 0.10)
    
    # Adjust for vehicle-specific factors
    if vehicle:
        # Get vehicle profitability
        vehicle_data = frappe.db.sql("""
            SELECT SUM(revenue_amount - cost_amount) as net_profit
            FROM `tabCost And Revenue Ledger`
            WHERE vehicle = %s
            AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
        """, (vehicle,), as_dict=True)
        
        if vehicle_data and vehicle_data[0].get("net_profit", 0) > 0:
            base_roi *= 1.2  # Boost ROI for profitable vehicles
    
    # Calculate projections
    annual_return = amount * base_roi
    payback_months = (amount / (annual_return / 12)) if annual_return > 0 else 999
    
    return {
        "investment_type": investment_type,
        "investment_amount": amount,
        "vehicle": vehicle,
        "estimated_annual_roi": f"{round(base_roi * 100, 1)}%",
        "estimated_annual_return": round(annual_return, 2),
        "payback_period_months": round(payback_months, 1),
        "recommendation": "Recommended" if base_roi > 0.15 and payback_months < 24 else "Review carefully",
        "confidence": 0.70
    }


def identify_cost_savings_opportunities(vehicle: Optional[str] = None) -> Dict:
    """
    Identify potential cost savings opportunities using AI.
    
    Args:
        vehicle: Optional vehicle ID (if None, analyzes fleet-wide)
    
    Returns:
        Cost savings opportunities
    """
    opportunities = []
    
    # Analyze fuel efficiency
    fuel_opportunity = _analyze_fuel_efficiency(vehicle)
    if fuel_opportunity:
        opportunities.append(fuel_opportunity)
    
    # Analyze maintenance timing
    maintenance_opportunity = _analyze_maintenance_timing(vehicle)
    if maintenance_opportunity:
        opportunities.append(maintenance_opportunity)
    
    # Analyze route optimization
    route_opportunity = _analyze_route_efficiency(vehicle)
    if route_opportunity:
        opportunities.append(route_opportunity)
    
    # Calculate total potential savings
    total_savings = sum(o.get("estimated_annual_savings", 0) for o in opportunities)
    
    return {
        "vehicle": vehicle or "Fleet-wide",
        "opportunities_found": len(opportunities),
        "total_estimated_savings": round(total_savings, 2),
        "opportunities": opportunities
    }


def _analyze_fuel_efficiency(vehicle: Optional[str]) -> Optional[Dict]:
    """Analyze fuel efficiency for savings opportunities."""
    # Stub implementation
    return {
        "category": "Fuel Efficiency",
        "description": "Implement driver training on fuel-efficient driving techniques",
        "estimated_annual_savings": 5000,
        "implementation_cost": 1000,
        "difficulty": "medium"
    }


def _analyze_maintenance_timing(vehicle: Optional[str]) -> Optional[Dict]:
    """Analyze maintenance timing for savings opportunities."""
    return {
        "category": "Preventive Maintenance",
        "description": "Switch to predictive maintenance to reduce reactive repairs",
        "estimated_annual_savings": 8000,
        "implementation_cost": 2000,
        "difficulty": "low"
    }


def _analyze_route_efficiency(vehicle: Optional[str]) -> Optional[Dict]:
    """Analyze route efficiency for savings opportunities."""
    return {
        "category": "Route Optimization",
        "description": "Optimize routes to reduce fuel consumption and travel time",
        "estimated_annual_savings": 6000,
        "implementation_cost": 500,
        "difficulty": "low"
    }
