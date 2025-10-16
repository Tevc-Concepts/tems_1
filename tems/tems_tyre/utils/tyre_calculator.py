"""
Tyre Calculator
Cost and performance calculations for tyres
"""
from __future__ import annotations

import frappe
from frappe.utils import flt, cint
from typing import Dict, Optional, Tuple


def calculate_cost_per_km(tyre: str) -> float:
    """
    Calculate cost per kilometer for a tyre
    Includes purchase cost, maintenance, and pro-rata disposal
    
    Args:
        tyre: Tyre document name
        
    Returns:
        float: Cost per kilometer
    """
    tyre_doc = frappe.get_doc("Tyre", tyre)
    
    # Get total cost
    purchase_cost = flt(tyre_doc.cost) or 0
    
    # Get maintenance costs from ledger
    maintenance_costs = get_tyre_maintenance_costs(tyre)
    
    total_cost = purchase_cost + maintenance_costs
    
    # Calculate cost per km
    mileage = flt(tyre_doc.current_mileage) or 1  # Avoid division by zero
    
    if mileage > 0:
        return total_cost / mileage
    
    return 0


def get_tyre_maintenance_costs(tyre: str) -> float:
    """
    Get total maintenance and operational costs for a tyre
    """
    # Query Cost And Revenue Ledger
    costs = frappe.db.sql("""
        SELECT SUM(amount) as total
        FROM `tabCost And Revenue Ledger`
        WHERE type = 'Cost'
        AND (remarks LIKE %s OR asset = (SELECT asset_link FROM `tabTyre` WHERE name = %s))
    """, (f"%{tyre}%", tyre), as_dict=True)
    
    if costs and costs[0].get("total"):
        return flt(costs[0]["total"])
    
    return 0


def calculate_wear_rate(tyre: str) -> Tuple[float, str]:
    """
    Calculate tyre wear rate in mm per 1000 km
    
    Args:
        tyre: Tyre document name
        
    Returns:
        Tuple of (wear_rate, status_message)
    """
    tyre_doc = frappe.get_doc("Tyre", tyre)
    
    initial_tread = flt(getattr(tyre_doc, "initial_tread_depth", 16.0))
    current_tread = flt(getattr(tyre_doc, "last_tread_depth_mm", 16.0))
    mileage = flt(tyre_doc.current_mileage) or 0
    
    if mileage == 0:
        return 0, "Insufficient mileage data"
    
    tread_worn = initial_tread - current_tread
    
    if tread_worn <= 0:
        return 0, "No wear detected"
    
    # Calculate mm per 1000 km
    wear_rate = (tread_worn / mileage) * 1000
    
    # Classify wear rate
    if wear_rate < 0.5:
        status = "Excellent wear rate"
    elif wear_rate < 1.0:
        status = "Good wear rate"
    elif wear_rate < 1.5:
        status = "Average wear rate"
    elif wear_rate < 2.0:
        status = "High wear rate"
    else:
        status = "Excessive wear rate - investigate"
    
    return wear_rate, status


def predict_replacement_date(tyre: str) -> Optional[Dict]:
    """
    Predict when a tyre will need replacement based on wear rate
    
    Args:
        tyre: Tyre document name
        
    Returns:
        Dict with prediction data or None
    """
    tyre_doc = frappe.get_doc("Tyre", tyre)
    
    wear_rate, _ = calculate_wear_rate(tyre)
    
    if wear_rate == 0:
        return None
    
    current_tread = flt(getattr(tyre_doc, "last_tread_depth_mm", 16.0))
    min_tread = 1.6  # Legal minimum in mm
    
    remaining_tread = current_tread - min_tread
    
    if remaining_tread <= 0:
        return {
            "status": "Replace Immediately",
            "remaining_km": 0,
            "days_until_replacement": 0
        }
    
    # Calculate remaining km based on wear rate (mm per 1000 km)
    remaining_km = (remaining_tread / wear_rate) * 1000
    
    # Estimate days based on average usage
    # This should be improved with actual vehicle usage patterns
    avg_km_per_day = 150  # Default assumption
    
    if tyre_doc.vehicle:
        # Try to get actual usage from vehicle
        vehicle_doc = frappe.get_doc("Vehicle", tyre_doc.vehicle)
        # Calculate from last 30 days if data available
        avg_km_per_day = get_vehicle_avg_daily_km(tyre_doc.vehicle) or avg_km_per_day
    
    days_until_replacement = remaining_km / avg_km_per_day if avg_km_per_day > 0 else 0
    
    # Determine status
    if days_until_replacement < 7:
        status = "Replace Immediately"
    elif days_until_replacement < 30:
        status = "Replace Soon"
    elif days_until_replacement < 90:
        status = "Caution"
    else:
        status = "Good"
    
    return {
        "status": status,
        "remaining_km": remaining_km,
        "days_until_replacement": int(days_until_replacement),
        "wear_rate_mm_per_1000km": wear_rate,
        "current_tread_mm": current_tread
    }


def calculate_tyre_roi(tyre: str) -> Dict:
    """
    Calculate return on investment for a tyre
    Compares cost against expected vs actual lifespan
    
    Args:
        tyre: Tyre document name
        
    Returns:
        Dict with ROI analysis
    """
    tyre_doc = frappe.get_doc("Tyre", tyre)
    
    purchase_cost = flt(tyre_doc.cost) or 0
    mileage = flt(tyre_doc.current_mileage) or 0
    
    # Expected lifespan (should be configurable per brand/model)
    expected_km = 80000  # Default expectation
    
    # Calculate performance ratio
    if expected_km > 0:
        performance_ratio = (mileage / expected_km) * 100
    else:
        performance_ratio = 0
    
    # Cost efficiency
    cost_per_km = calculate_cost_per_km(tyre)
    
    # Industry benchmark (configurable)
    benchmark_cost_per_km = 0.50  # Currency per km
    
    efficiency_ratio = (benchmark_cost_per_km / cost_per_km * 100) if cost_per_km > 0 else 100
    
    return {
        "tyre": tyre,
        "purchase_cost": purchase_cost,
        "current_mileage": mileage,
        "expected_mileage": expected_km,
        "performance_ratio": performance_ratio,
        "cost_per_km": cost_per_km,
        "benchmark_cost_per_km": benchmark_cost_per_km,
        "efficiency_ratio": efficiency_ratio,
        "status": "Exceeding Expectations" if performance_ratio > 100 else 
                 "Meeting Expectations" if performance_ratio > 80 else
                 "Below Expectations"
    }


def get_vehicle_avg_daily_km(vehicle: str) -> Optional[float]:
    """
    Calculate average daily kilometers for a vehicle
    Based on recent journey data
    """
    try:
        # Get vehicle's journey data from last 30 days
        journeys = frappe.db.sql("""
            SELECT SUM(distance_km) as total_km, COUNT(*) as journey_count,
                   DATEDIFF(MAX(start_time), MIN(start_time)) as days
            FROM `tabJourney Plan`
            WHERE vehicle = %s
            AND start_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """, (vehicle,), as_dict=True)
        
        if journeys and journeys[0].get("total_km") and journeys[0].get("days"):
            days = max(1, journeys[0]["days"])
            return flt(journeys[0]["total_km"]) / days
            
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Error calculating avg daily km: {str(e)}")
    
    return None


def compare_tyre_performance(tyre_list: list) -> list:
    """
    Compare performance across multiple tyres
    Used for brand/model analysis
    
    Args:
        tyre_list: List of tyre document names
        
    Returns:
        List of dicts with comparative metrics
    """
    results = []
    
    for tyre in tyre_list:
        try:
            roi = calculate_tyre_roi(tyre)
            wear_rate, wear_status = calculate_wear_rate(tyre)
            cost_per_km = calculate_cost_per_km(tyre)
            
            tyre_doc = frappe.get_doc("Tyre", tyre)
            
            results.append({
                "tyre": tyre,
                "brand": getattr(tyre_doc, "brand", ""),
                "model": getattr(tyre_doc, "model", ""),
                "size": getattr(tyre_doc, "size", ""),
                "cost_per_km": cost_per_km,
                "wear_rate": wear_rate,
                "wear_status": wear_status,
                "performance_ratio": roi["performance_ratio"],
                "current_mileage": roi["current_mileage"],
                "status": roi["status"]
            })
            
        except Exception as e:
            frappe.logger("tems_tyre").error(f"Error analyzing tyre {tyre}: {str(e)}")
            continue
    
    # Sort by performance ratio descending
    results.sort(key=lambda x: x["performance_ratio"], reverse=True)
    
    return results


def calculate_fleet_tyre_metrics(vehicle: str = None) -> Dict:
    """
    Calculate aggregate tyre metrics for fleet or specific vehicle
    
    Args:
        vehicle: Optional vehicle filter
        
    Returns:
        Dict with aggregate metrics
    """
    filters = {}
    if vehicle:
        filters["vehicle"] = vehicle
    
    # Get all active tyres
    tyres = frappe.get_all(
        "Tyre",
        filters=filters,
        fields=["name", "cost", "current_mileage", "status", "brand", "model"]
    )
    
    total_cost = 0
    total_mileage = 0
    active_count = 0
    disposed_count = 0
    
    brand_performance = {}
    
    for tyre in tyres:
        total_cost += flt(tyre.get("cost", 0))
        total_mileage += flt(tyre.get("current_mileage", 0))
        
        if tyre.get("status") in ["Installed", "In Stock"]:
            active_count += 1
        elif tyre.get("status") == "Disposed":
            disposed_count += 1
        
        # Track by brand
        brand = tyre.get("brand", "Unknown")
        if brand not in brand_performance:
            brand_performance[brand] = {
                "count": 0,
                "total_mileage": 0,
                "total_cost": 0
            }
        
        brand_performance[brand]["count"] += 1
        brand_performance[brand]["total_mileage"] += flt(tyre.get("current_mileage", 0))
        brand_performance[brand]["total_cost"] += flt(tyre.get("cost", 0))
    
    # Calculate averages
    avg_cost_per_tyre = total_cost / len(tyres) if len(tyres) > 0 else 0
    avg_mileage_per_tyre = total_mileage / len(tyres) if len(tyres) > 0 else 0
    
    # Calculate brand metrics
    for brand in brand_performance:
        data = brand_performance[brand]
        data["avg_mileage"] = data["total_mileage"] / data["count"] if data["count"] > 0 else 0
        data["avg_cost"] = data["total_cost"] / data["count"] if data["count"] > 0 else 0
        data["cost_per_km"] = data["total_cost"] / data["total_mileage"] if data["total_mileage"] > 0 else 0
    
    return {
        "total_tyres": len(tyres),
        "active_tyres": active_count,
        "disposed_tyres": disposed_count,
        "total_investment": total_cost,
        "total_mileage": total_mileage,
        "avg_cost_per_tyre": avg_cost_per_tyre,
        "avg_mileage_per_tyre": avg_mileage_per_tyre,
        "brand_performance": brand_performance,
        "vehicle": vehicle or "Fleet-wide"
    }
