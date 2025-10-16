"""
Safety AI Handler
=================
AI-powered features for Safety Management domain.
"""

import frappe
from typing import Dict, List, Optional
from datetime import datetime, timedelta


def predict_driver_risk_score(driver: str) -> Dict:
    """
    Calculate AI-powered risk score for a driver.
    
    Args:
        driver: Employee/Driver ID
    
    Returns:
        Risk score (0-100) with breakdown
    """
    # Get driver's incident history
    incidents = frappe.get_all(
        "Incident Report",
        filters={"driver": driver},
        fields=["severity", "incident_type", "creation"],
        order_by="creation desc",
        limit=50
    )
    
    # Count incidents by severity
    high_severity = sum(1 for i in incidents if i.get("severity") == "High")
    medium_severity = sum(1 for i in incidents if i.get("severity") == "Medium")
    low_severity = sum(1 for i in incidents if i.get("severity") == "Low")
    
    # Recent incidents (last 90 days) carry more weight
    recent_incidents = [i for i in incidents 
                       if (datetime.now() - i.get("creation")).days <= 90]
    
    # Calculate risk components
    incident_risk = min(100, len(incidents) * 5)  # 5 points per incident
    severity_risk = (high_severity * 20 + medium_severity * 10 + low_severity * 5)
    recency_risk = len(recent_incidents) * 10  # Recent incidents are more concerning
    
    # Overall risk score (0-100, higher is worse)
    total_risk = min(100, incident_risk * 0.4 + severity_risk * 0.4 + recency_risk * 0.2)
    
    # Convert to safety score (higher is better)
    safety_score = 100 - total_risk
    
    return {
        "driver": driver,
        "risk_score": round(total_risk, 1),
        "safety_score": round(safety_score, 1),
        "risk_level": _risk_level(total_risk),
        "breakdown": {
            "total_incidents": len(incidents),
            "recent_incidents": len(recent_incidents),
            "high_severity": high_severity,
            "medium_severity": medium_severity,
            "low_severity": low_severity
        },
        "recommendation": _get_driver_recommendation(total_risk)
    }


def predict_journey_risk(journey_plan: str) -> Dict:
    """
    Predict risk level for a planned journey.
    
    Args:
        journey_plan: Journey Plan ID
    
    Returns:
        Journey risk assessment
    """
    journey = frappe.get_doc("Journey Plan", journey_plan)
    
    driver = journey.get("driver")
    route = journey.get("route")
    vehicle = journey.get("vehicle")
    
    # Get driver risk score
    driver_risk = 0
    if driver:
        driver_score = predict_driver_risk_score(driver)
        driver_risk = driver_score.get("risk_score", 0)
    
    # Get vehicle risk (based on maintenance status)
    vehicle_risk = 0
    if vehicle:
        recent_maintenance = frappe.db.count(
            "Maintenance Work Order",
            filters={
                "vehicle": vehicle,
                "status": ["in", ["Pending", "In Progress"]]
            }
        )
        vehicle_risk = min(50, recent_maintenance * 15)
    
    # Route risk (based on historical incidents on this route)
    route_risk = 0
    if route:
        route_incidents = frappe.db.count(
            "Incident Report",
            filters={"route": route}
        )
        route_risk = min(40, route_incidents * 10)
    
    # Weather risk (stub - would integrate with weather API)
    weather_risk = 10  # Default low risk
    
    # Calculate overall journey risk
    total_risk = (driver_risk * 0.4 + vehicle_risk * 0.3 + 
                  route_risk * 0.2 + weather_risk * 0.1)
    
    return {
        "journey_plan": journey_plan,
        "overall_risk_score": round(total_risk, 1),
        "risk_level": _risk_level(total_risk),
        "risk_components": {
            "driver_risk": round(driver_risk, 1),
            "vehicle_risk": round(vehicle_risk, 1),
            "route_risk": round(route_risk, 1),
            "weather_risk": round(weather_risk, 1)
        },
        "recommendation": _get_journey_recommendation(total_risk),
        "approval_recommended": total_risk < 50
    }


def detect_fatigue_patterns(driver: str, period_days: int = 30) -> Dict:
    """
    Detect driver fatigue patterns using AI.
    
    Args:
        driver: Driver ID
        period_days: Analysis period in days
    
    Returns:
        Fatigue analysis
    """
    # Get driver's trip history
    trips = frappe.db.sql("""
        SELECT 
            DATE(creation) as trip_date,
            COUNT(*) as trip_count,
            SUM(estimated_duration) as total_duration
        FROM `tabTrip Allocation`
        WHERE driver = %s
        AND DATE(creation) >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY DATE(creation)
        ORDER BY trip_date
    """, (driver, period_days), as_dict=True)
    
    if not trips:
        return {
            "driver": driver,
            "fatigue_detected": False,
            "message": "Insufficient trip data"
        }
    
    # Analyze patterns
    high_volume_days = sum(1 for t in trips if t.get("trip_count", 0) > 5)
    long_duration_days = sum(1 for t in trips if t.get("total_duration", 0) > 480)  # > 8 hours
    
    # Calculate fatigue risk
    fatigue_risk = (high_volume_days * 5 + long_duration_days * 10)
    fatigue_detected = fatigue_risk > 30
    
    return {
        "driver": driver,
        "period_days": period_days,
        "fatigue_risk_score": min(100, fatigue_risk),
        "fatigue_detected": fatigue_detected,
        "patterns": {
            "high_volume_days": high_volume_days,
            "long_duration_days": long_duration_days,
            "total_trips": len(trips)
        },
        "recommendation": "Mandatory rest period recommended" if fatigue_detected else "Normal work pattern"
    }


def predict_incident_hotspots(region: Optional[str] = None) -> Dict:
    """
    Predict incident hotspots using historical data.
    
    Args:
        region: Optional region filter
    
    Returns:
        Hotspot analysis
    """
    filters = {}
    if region:
        filters["region"] = region
    
    # Get incident locations
    incidents = frappe.get_all(
        "Incident Report",
        filters=filters,
        fields=["route", "location", "severity"],
        limit=200
    )
    
    # Count incidents by route
    route_incidents = {}
    for incident in incidents:
        route = incident.get("route", "Unknown")
        if route not in route_incidents:
            route_incidents[route] = {
                "count": 0,
                "high_severity": 0
            }
        
        route_incidents[route]["count"] += 1
        if incident.get("severity") == "High":
            route_incidents[route]["high_severity"] += 1
    
    # Identify hotspots (routes with > average incidents)
    avg_incidents = sum(r["count"] for r in route_incidents.values()) / len(route_incidents) if route_incidents else 0
    
    hotspots = []
    for route, data in route_incidents.items():
        if data["count"] > avg_incidents:
            risk_score = (data["count"] * 10 + data["high_severity"] * 20)
            hotspots.append({
                "route": route,
                "incident_count": data["count"],
                "high_severity_count": data["high_severity"],
                "risk_score": min(100, risk_score),
                "risk_level": _risk_level(risk_score)
            })
    
    # Sort by risk score
    hotspots.sort(key=lambda x: x["risk_score"], reverse=True)
    
    return {
        "region": region or "All Regions",
        "total_incidents": len(incidents),
        "total_routes_analyzed": len(route_incidents),
        "hotspot_count": len(hotspots),
        "hotspots": hotspots[:10],  # Top 10 hotspots
        "recommendations": [
            "Increase monitoring on high-risk routes",
            "Implement additional safety measures",
            "Provide route-specific safety training"
        ]
    }


def calculate_safety_compliance_score(entity: str, entity_type: str = "driver") -> Dict:
    """
    Calculate safety compliance score for a driver or vehicle.
    
    Args:
        entity: Driver or Vehicle ID
        entity_type: "driver" or "vehicle"
    
    Returns:
        Compliance score
    """
    if entity_type == "driver":
        return _calculate_driver_compliance(entity)
    elif entity_type == "vehicle":
        return _calculate_vehicle_compliance(entity)
    else:
        return {"error": "Invalid entity type"}


def _calculate_driver_compliance(driver: str) -> Dict:
    """Calculate driver safety compliance score."""
    # Check license validity
    emp = frappe.get_doc("Employee", driver)
    license_valid = 1  # Stub - would check actual license expiry
    
    # Check training completion
    training_count = frappe.db.count(
        "Training Event",
        filters={"employee": driver, "status": "Completed"}
    )
    training_score = min(100, training_count * 20)
    
    # Check incident-free record
    recent_incidents = frappe.db.count(
        "Incident Report",
        filters={
            "driver": driver,
            "creation": [">=", datetime.now() - timedelta(days=90)]
        }
    )
    incident_score = max(0, 100 - (recent_incidents * 20))
    
    # Overall compliance
    compliance_score = (training_score * 0.4 + incident_score * 0.6)
    
    return {
        "entity": driver,
        "entity_type": "driver",
        "compliance_score": round(compliance_score, 1),
        "grade": _score_to_grade(compliance_score),
        "components": {
            "license_valid": license_valid,
            "training_score": training_score,
            "incident_score": incident_score
        }
    }


def _calculate_vehicle_compliance(vehicle: str) -> Dict:
    """Calculate vehicle safety compliance score."""
    # Check inspection status
    recent_inspections = frappe.db.count(
        "Spot Check",
        filters={
            "vehicle": vehicle,
            "status": "Passed",
            "creation": [">=", datetime.now() - timedelta(days=90)]
        }
    )
    inspection_score = min(100, recent_inspections * 50)
    
    # Check maintenance status
    pending_maintenance = frappe.db.count(
        "Maintenance Work Order",
        filters={
            "vehicle": vehicle,
            "status": "Pending"
        }
    )
    maintenance_score = max(0, 100 - (pending_maintenance * 25))
    
    # Overall compliance
    compliance_score = (inspection_score * 0.5 + maintenance_score * 0.5)
    
    return {
        "entity": vehicle,
        "entity_type": "vehicle",
        "compliance_score": round(compliance_score, 1),
        "grade": _score_to_grade(compliance_score),
        "components": {
            "inspection_score": inspection_score,
            "maintenance_score": maintenance_score,
            "pending_maintenance_count": pending_maintenance
        }
    }


def _risk_level(risk_score: float) -> str:
    """Convert risk score to level."""
    if risk_score >= 70:
        return "critical"
    elif risk_score >= 50:
        return "high"
    elif risk_score >= 30:
        return "medium"
    else:
        return "low"


def _score_to_grade(score: float) -> str:
    """Convert score to letter grade."""
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


def _get_driver_recommendation(risk_score: float) -> str:
    """Get recommendation based on driver risk score."""
    if risk_score >= 70:
        return "High risk: Suspend from operations pending review and additional training"
    elif risk_score >= 50:
        return "Elevated risk: Require additional supervision and immediate safety training"
    elif risk_score >= 30:
        return "Moderate risk: Schedule safety refresher training"
    else:
        return "Low risk: Continue regular operations with standard monitoring"


def _get_journey_recommendation(risk_score: float) -> str:
    """Get recommendation based on journey risk score."""
    if risk_score >= 70:
        return "Do not approve: Risk too high. Address identified issues first."
    elif risk_score >= 50:
        return "Approve with caution: Implement additional safety measures."
    elif risk_score >= 30:
        return "Approve: Monitor closely during journey."
    else:
        return "Approve: Normal safety protocols apply."
