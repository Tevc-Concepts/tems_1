"""
Fleet AI Handler
================
AI-powered features for Fleet Management domain.
"""

import frappe
from typing import Dict, List, Optional
from tems.tems_ai.services.model_manager import ModelManager
from tems.tems_ai.services.insights_engine import generate_insight


def predict_maintenance_schedule(vehicle: str) -> Dict:
    """
    Predict when a vehicle will need maintenance.
    
    Args:
        vehicle: Vehicle ID
    
    Returns:
        Maintenance prediction with recommended date and components
    """
    # Get vehicle data
    vehicle_doc = frappe.get_doc("Vehicle", vehicle)
    odometer = vehicle_doc.get("odometer", 0)
    
    # Get maintenance history
    maintenance_history = frappe.get_all(
        "Maintenance Work Order",
        filters={"vehicle": vehicle},
        fields=["work_order_date", "maintenance_type", "cost", "odometer_reading"],
        order_by="work_order_date desc",
        limit=20
    )
    
    # Prepare input features
    input_data = {
        "vehicle": vehicle,
        "current_odometer": odometer,
        "maintenance_count": len(maintenance_history),
        "avg_maintenance_cost": sum(m.get("cost", 0) for m in maintenance_history) / len(maintenance_history) if maintenance_history else 0,
        "days_since_last_maintenance": _calculate_days_since_last(maintenance_history)
    }
    
    # Generate prediction
    result = generate_insight(domain="fleet", mode="forecast", context=input_data)
    
    return result


def detect_fuel_anomaly(vehicle: str, fuel_consumption: float) -> Dict:
    """
    Detect anomalies in fuel consumption for a vehicle.
    
    Args:
        vehicle: Vehicle ID
        fuel_consumption: Current fuel consumption rate
    
    Returns:
        Anomaly detection result
    """
    # Get historical fuel data
    fuel_logs = frappe.db.sql("""
        SELECT AVG(fuel_consumption) as avg_fuel, 
               STDDEV(fuel_consumption) as std_fuel
        FROM `tabVehicle Fuel Log`
        WHERE vehicle = %s
        AND creation >= DATE_SUB(NOW(), INTERVAL 90 DAY)
    """, (vehicle,), as_dict=True)
    
    if not fuel_logs or not fuel_logs[0].get("avg_fuel"):
        return {"anomaly": False, "reason": "Insufficient historical data"}
    
    avg_fuel = fuel_logs[0].get("avg_fuel", 0)
    std_fuel = fuel_logs[0].get("std_fuel", 0)
    
    # Calculate z-score
    z_score = abs((fuel_consumption - avg_fuel) / std_fuel) if std_fuel > 0 else 0
    
    is_anomaly = z_score > 2.5  # More than 2.5 standard deviations
    
    return {
        "anomaly": is_anomaly,
        "z_score": z_score,
        "current_consumption": fuel_consumption,
        "average_consumption": avg_fuel,
        "severity": "high" if z_score > 3 else "medium" if z_score > 2 else "low",
        "recommendation": "Inspect vehicle for fuel system issues" if is_anomaly else "Normal operation"
    }


def calculate_vehicle_health_score(vehicle: str) -> Dict:
    """
    Calculate overall health score for a vehicle using AI.
    
    Args:
        vehicle: Vehicle ID
    
    Returns:
        Health score (0-100) with breakdown
    """
    vehicle_doc = frappe.get_doc("Vehicle", vehicle)
    
    # Collect metrics
    odometer = vehicle_doc.get("odometer", 0)
    age_years = _calculate_vehicle_age(vehicle_doc.get("model_year"))
    
    # Recent maintenance
    recent_maintenance_count = frappe.db.count(
        "Maintenance Work Order",
        filters={
            "vehicle": vehicle,
            "work_order_date": [">=", frappe.utils.add_days(None, -90)]
        }
    )
    
    # Recent incidents
    recent_incident_count = frappe.db.count(
        "Incident Report",
        filters={
            "vehicle": vehicle,
            "creation": [">=", frappe.utils.add_days(None, -90)]
        }
    )
    
    # Calculate score components
    age_score = max(0, 100 - (age_years * 5))  # Lose 5 points per year
    maintenance_score = max(0, 100 - (recent_maintenance_count * 10))  # Lose 10 points per maintenance
    incident_score = max(0, 100 - (recent_incident_count * 15))  # Lose 15 points per incident
    
    # Weighted average
    health_score = (age_score * 0.3 + maintenance_score * 0.4 + incident_score * 0.3)
    
    return {
        "vehicle": vehicle,
        "health_score": round(health_score, 1),
        "grade": _score_to_grade(health_score),
        "breakdown": {
            "age_score": round(age_score, 1),
            "maintenance_score": round(maintenance_score, 1),
            "incident_score": round(incident_score, 1)
        },
        "recommendation": _get_health_recommendation(health_score)
    }


def optimize_maintenance_budget(fleet_size: int, budget: float) -> Dict:
    """
    AI-powered maintenance budget optimization.
    
    Args:
        fleet_size: Number of vehicles
        budget: Available budget
    
    Returns:
        Budget allocation recommendations
    """
    # Get all vehicles with maintenance needs
    vehicles = frappe.get_all(
        "Vehicle",
        fields=["name", "odometer", "model_year"],
        limit=fleet_size
    )
    
    vehicle_priorities = []
    
    for vehicle in vehicles:
        health_score = calculate_vehicle_health_score(vehicle["name"])
        priority_score = 100 - health_score["health_score"]  # Lower health = higher priority
        
        vehicle_priorities.append({
            "vehicle": vehicle["name"],
            "health_score": health_score["health_score"],
            "priority_score": priority_score
        })
    
    # Sort by priority
    vehicle_priorities.sort(key=lambda x: x["priority_score"], reverse=True)
    
    # Allocate budget
    budget_per_vehicle = budget / fleet_size if fleet_size > 0 else 0
    
    allocations = []
    for v in vehicle_priorities:
        # Higher priority vehicles get more budget
        multiplier = 1 + (v["priority_score"] / 100)
        allocation = budget_per_vehicle * multiplier
        
        allocations.append({
            "vehicle": v["vehicle"],
            "allocated_budget": round(allocation, 2),
            "priority": "high" if v["priority_score"] > 70 else "medium" if v["priority_score"] > 40 else "low"
        })
    
    return {
        "total_budget": budget,
        "fleet_size": fleet_size,
        "allocations": allocations
    }


def _calculate_days_since_last(maintenance_history: List[Dict]) -> int:
    """Calculate days since last maintenance."""
    if not maintenance_history:
        return 999
    
    last_date = maintenance_history[0].get("work_order_date")
    if not last_date:
        return 999
    
    from datetime import datetime
    delta = datetime.now().date() - last_date
    return delta.days


def _calculate_vehicle_age(model_year: Optional[int]) -> float:
    """Calculate vehicle age in years."""
    if not model_year:
        return 0.0
    
    from datetime import datetime
    current_year = datetime.now().year
    return current_year - model_year


def _score_to_grade(score: float) -> str:
    """Convert health score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def _get_health_recommendation(score: float) -> str:
    """Get recommendation based on health score."""
    if score >= 90:
        return "Vehicle in excellent condition. Continue regular maintenance."
    elif score >= 70:
        return "Vehicle in good condition. Schedule preventive maintenance."
    elif score >= 50:
        return "Vehicle requires attention. Increase inspection frequency."
    else:
        return "Vehicle in poor condition. Immediate maintenance recommended."
