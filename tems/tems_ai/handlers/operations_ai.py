"""
Operations AI Handler
=====================
AI-powered features for Operations Management domain.
"""

import frappe
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from tems.tems_ai.services.insights_engine import generate_insight


def predict_trip_eta(trip: str) -> Dict:
    """
    Predict ETA for a trip using AI.
    
    Args:
        trip: Trip Allocation ID
    
    Returns:
        ETA prediction with confidence
    """
    trip_doc = frappe.get_doc("Trip Allocation", trip)
    
    # Get historical data for this route
    route = trip_doc.get("route")
    historical_trips = frappe.get_all(
        "Trip Allocation",
        filters={"route": route, "status": "Completed"},
        fields=["estimated_duration", "actual_duration", "distance"],
        limit=50
    )
    
    # Calculate average duration for this route
    if historical_trips:
        avg_duration = sum(t.get("actual_duration", t.get("estimated_duration", 0)) 
                          for t in historical_trips) / len(historical_trips)
        
        variance = _calculate_variance([t.get("actual_duration", 0) for t in historical_trips])
    else:
        avg_duration = trip_doc.get("estimated_duration", 0)
        variance = 0.2  # 20% default variance
    
    # Adjust for time of day (traffic patterns)
    time_multiplier = _get_time_of_day_multiplier(datetime.now().hour)
    
    # Adjust for weather (stub - would integrate with weather API)
    weather_multiplier = 1.0  # Neutral
    
    # Calculate predicted ETA
    predicted_duration = avg_duration * time_multiplier * weather_multiplier
    confidence = max(0.5, 1.0 - variance)  # Lower variance = higher confidence
    
    return {
        "trip": trip,
        "predicted_duration_minutes": round(predicted_duration, 0),
        "estimated_arrival": (datetime.now() + timedelta(minutes=predicted_duration)).isoformat(),
        "confidence": round(confidence, 2),
        "factors": {
            "historical_avg": round(avg_duration, 0),
            "time_of_day_factor": time_multiplier,
            "weather_factor": weather_multiplier
        }
    }


def optimize_route(origin: str, destination: str, waypoints: Optional[List[str]] = None) -> Dict:
    """
    AI-powered route optimization.
    
    Args:
        origin: Starting location
        destination: End location
        waypoints: Optional intermediate stops
    
    Returns:
        Optimized route recommendations
    """
    # Stub implementation - would integrate with mapping API
    # For now, return simple recommendations
    
    waypoints = waypoints or []
    
    return {
        "origin": origin,
        "destination": destination,
        "waypoints": waypoints,
        "recommended_route": {
            "path": [origin] + waypoints + [destination],
            "estimated_distance_km": 100,  # Stub
            "estimated_duration_minutes": 120,  # Stub
            "fuel_efficiency_score": 85,
            "safety_score": 90
        },
        "alternative_routes": [],
        "optimization_factors": [
            "Shortest distance",
            "Fewer stops",
            "Better road conditions"
        ]
    }


def detect_route_deviation(trip: str, current_location: Dict) -> Dict:
    """
    Detect if a vehicle has deviated from planned route.
    
    Args:
        trip: Trip Allocation ID
        current_location: Current GPS coordinates
    
    Returns:
        Deviation detection result
    """
    trip_doc = frappe.get_doc("Trip Allocation", trip)
    planned_route = trip_doc.get("route")
    
    # Get route waypoints (stub - would use actual GPS data)
    # For now, return simple deviation check
    
    return {
        "trip": trip,
        "deviation_detected": False,  # Stub
        "deviation_distance_km": 0,
        "current_location": current_location,
        "planned_route": planned_route,
        "alert_level": "none",
        "recommendation": "Vehicle is on planned route"
    }


def predict_vehicle_demand(region: str, date_range: Optional[int] = 7) -> Dict:
    """
    Predict vehicle demand for a region.
    
    Args:
        region: Region/area name
        date_range: Number of days to forecast
    
    Returns:
        Demand forecast
    """
    # Get historical trip data for the region
    historical_trips = frappe.db.sql("""
        SELECT DATE(creation) as trip_date, COUNT(*) as trip_count
        FROM `tabTrip Allocation`
        WHERE route LIKE %s
        AND DATE(creation) >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
        GROUP BY DATE(creation)
    """, (f"%{region}%",), as_dict=True)
    
    if not historical_trips:
        return {
            "region": region,
            "forecast": [],
            "message": "Insufficient historical data"
        }
    
    # Calculate average daily demand
    avg_demand = sum(t.get("trip_count", 0) for t in historical_trips) / len(historical_trips)
    
    # Generate forecast (simple trend projection)
    forecast = []
    for day in range(date_range):
        forecast_date = datetime.now().date() + timedelta(days=day)
        # Add some variation (stub - real implementation would use time series models)
        predicted_demand = int(avg_demand * (0.9 + (day % 3) * 0.1))
        
        forecast.append({
            "date": forecast_date.isoformat(),
            "predicted_demand": predicted_demand,
            "confidence": 0.75
        })
    
    return {
        "region": region,
        "date_range_days": date_range,
        "historical_avg_daily_demand": round(avg_demand, 1),
        "forecast": forecast
    }


def calculate_operational_efficiency(date_from: str, date_to: str) -> Dict:
    """
    Calculate operational efficiency metrics using AI.
    
    Args:
        date_from: Start date
        date_to: End date
    
    Returns:
        Efficiency metrics and recommendations
    """
    # Get trip data for the period
    trips = frappe.get_all(
        "Trip Allocation",
        filters={
            "creation": ["between", [date_from, date_to]]
        },
        fields=["name", "status", "estimated_duration", "actual_duration", "distance"]
    )
    
    if not trips:
        return {
            "message": "No trips found for the specified period",
            "efficiency_score": 0
        }
    
    completed_trips = [t for t in trips if t.get("status") == "Completed"]
    
    # Calculate metrics
    on_time_trips = sum(1 for t in completed_trips 
                       if t.get("actual_duration", 0) <= t.get("estimated_duration", 0) * 1.1)
    
    on_time_percentage = (on_time_trips / len(completed_trips) * 100) if completed_trips else 0
    
    # Calculate utilization
    total_trips = len(trips)
    completion_rate = (len(completed_trips) / total_trips * 100) if total_trips else 0
    
    # Overall efficiency score
    efficiency_score = (on_time_percentage * 0.6 + completion_rate * 0.4)
    
    return {
        "period": {
            "from": date_from,
            "to": date_to
        },
        "metrics": {
            "total_trips": total_trips,
            "completed_trips": len(completed_trips),
            "completion_rate": round(completion_rate, 1),
            "on_time_percentage": round(on_time_percentage, 1),
            "efficiency_score": round(efficiency_score, 1)
        },
        "grade": _score_to_grade(efficiency_score),
        "recommendations": _get_efficiency_recommendations(efficiency_score)
    }


def _get_time_of_day_multiplier(hour: int) -> float:
    """Get traffic multiplier based on time of day."""
    # Morning rush (7-9 AM)
    if 7 <= hour < 9:
        return 1.3
    # Evening rush (5-7 PM)
    elif 17 <= hour < 19:
        return 1.4
    # Night (10 PM - 5 AM)
    elif hour >= 22 or hour < 5:
        return 0.8
    # Regular hours
    else:
        return 1.0


def _calculate_variance(values: List[float]) -> float:
    """Calculate variance of a list of values."""
    if not values or len(values) < 2:
        return 0.0
    
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance / (mean ** 2) if mean > 0 else 0.0  # Coefficient of variation


def _score_to_grade(score: float) -> str:
    """Convert efficiency score to letter grade."""
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


def _get_efficiency_recommendations(score: float) -> List[str]:
    """Get recommendations based on efficiency score."""
    recommendations = []
    
    if score < 70:
        recommendations.append("Review and optimize route planning")
        recommendations.append("Increase driver training on time management")
    
    if score < 80:
        recommendations.append("Implement real-time tracking for better coordination")
        recommendations.append("Analyze delay patterns and address root causes")
    
    if score >= 90:
        recommendations.append("Maintain current operational standards")
        recommendations.append("Share best practices across teams")
    
    return recommendations
