"""
Tyre Analyzer - AI-powered insights
Integrates with tems_ai module for predictive analytics
"""
from __future__ import annotations

import frappe
from frappe.utils import flt
from typing import Dict, Optional
import json


def calculate_health_index(tyre: str) -> int:
    """
    Calculate AI Health Index (0-100) for a tyre
    Combines multiple factors: tread depth, pressure, age, mileage, incidents
    
    Args:
        tyre: Tyre document name
        
    Returns:
        int: Health score 0-100
    """
    tyre_doc = frappe.get_doc("Tyre", tyre)
    
    scores = []
    weights = []
    
    # 1. Tread Depth Score (40% weight)
    tread_score = calculate_tread_score(tyre_doc)
    scores.append(tread_score)
    weights.append(0.40)
    
    # 2. Pressure Score (25% weight)
    pressure_score = calculate_pressure_score(tyre_doc)
    scores.append(pressure_score)
    weights.append(0.25)
    
    # 3. Age/Mileage Score (20% weight)
    usage_score = calculate_usage_score(tyre_doc)
    scores.append(usage_score)
    weights.append(0.20)
    
    # 4. Incident History Score (15% weight)
    incident_score = calculate_incident_score(tyre_doc)
    scores.append(incident_score)
    weights.append(0.15)
    
    # Weighted average
    health_index = sum(s * w for s, w in zip(scores, weights))
    
    return int(health_index)


def calculate_tread_score(tyre_doc) -> float:
    """
    Score based on tread depth
    New tyre (16mm) = 100, Legal minimum (1.6mm) = 0
    """
    current_tread = flt(getattr(tyre_doc, "last_tread_depth_mm", 16.0))
    
    NEW_TREAD = 16.0
    MIN_TREAD = 1.6
    USABLE_RANGE = NEW_TREAD - MIN_TREAD
    
    remaining_tread = max(0, current_tread - MIN_TREAD)
    score = (remaining_tread / USABLE_RANGE) * 100
    
    return max(0, min(100, score))


def calculate_pressure_score(tyre_doc) -> float:
    """
    Score based on last recorded pressure
    Optimal range varies by tyre type, assume 100-120 psi for commercial
    """
    last_pressure = flt(getattr(tyre_doc, "last_pressure_psi", 0))
    
    if last_pressure == 0:
        # No data, assume OK
        return 75.0
    
    # Optimal range for commercial vehicle tyres
    OPTIMAL_MIN = 100
    OPTIMAL_MAX = 120
    
    if OPTIMAL_MIN <= last_pressure <= OPTIMAL_MAX:
        return 100.0
    elif last_pressure < OPTIMAL_MIN:
        # Under-inflation penalty
        deficit = OPTIMAL_MIN - last_pressure
        score = 100 - (deficit * 2)  # -2 points per psi under
    else:
        # Over-inflation penalty
        excess = last_pressure - OPTIMAL_MAX
        score = 100 - (excess * 1.5)  # -1.5 points per psi over
    
    return max(0, min(100, score))


def calculate_usage_score(tyre_doc) -> float:
    """
    Score based on age and mileage relative to expected lifespan
    """
    current_mileage = flt(getattr(tyre_doc, "current_mileage", 0))
    
    # Expected lifespan (should be configurable per brand/model)
    expected_km = 80000
    
    if current_mileage == 0:
        return 100.0
    
    usage_ratio = current_mileage / expected_km
    
    if usage_ratio < 0.5:
        score = 100
    elif usage_ratio < 0.75:
        score = 90
    elif usage_ratio < 1.0:
        score = 75
    elif usage_ratio < 1.25:
        score = 50
    else:
        score = 25
    
    return score


def calculate_incident_score(tyre_doc) -> float:
    """
    Score based on incident/damage history
    Perfect record = 100, multiple incidents = lower score
    """
    tyre_name = tyre_doc.name
    
    # Check for recorded incidents in inspection logs
    inspections = frappe.get_all(
        "Tyre Inspection Log",
        filters={"tyre": tyre_name},
        fields=["ai_condition_classification", "observations"]
    )
    
    critical_count = 0
    warning_count = 0
    
    for insp in inspections:
        condition = insp.get("ai_condition_classification", "")
        if condition in ["Replace Immediately", "Replace Soon"]:
            critical_count += 1
        elif condition == "Caution":
            warning_count += 1
    
    # Scoring
    if critical_count == 0 and warning_count == 0:
        return 100.0
    
    score = 100 - (critical_count * 20) - (warning_count * 5)
    
    return max(0, score)


def classify_tyre_condition(health_index: int) -> str:
    """
    Classify tyre condition based on health index
    
    Args:
        health_index: 0-100 health score
        
    Returns:
        str: Classification (Good, Caution, Replace Soon, Replace Immediately)
    """
    if health_index >= 85:
        return "Good"
    elif health_index >= 70:
        return "Caution"
    elif health_index >= 50:
        return "Replace Soon"
    else:
        return "Replace Immediately"


def detect_pressure_anomaly(sensor_data: Dict) -> Dict:
    """
    Detect anomalies in tyre pressure/temperature sensor data
    
    Args:
        sensor_data: Dict with pressure_psi, temperature_c, tyre
        
    Returns:
        Dict with anomaly detection results
    """
    pressure = flt(sensor_data.get("pressure_psi", 0))
    temperature = flt(sensor_data.get("temperature_c", 0))
    tyre = sensor_data.get("tyre")
    
    anomalies = []
    severity = "Normal"
    
    # Pressure checks
    if pressure < 80:
        anomalies.append("Critical low pressure")
        severity = "Critical"
    elif pressure < 95:
        anomalies.append("Low pressure warning")
        severity = "Warning" if severity == "Normal" else severity
    elif pressure > 140:
        anomalies.append("Critical over-pressure")
        severity = "Critical"
    elif pressure > 125:
        anomalies.append("High pressure warning")
        severity = "Warning" if severity == "Normal" else severity
    
    # Temperature checks
    if temperature > 90:
        anomalies.append("Critical temperature - possible bearing failure")
        severity = "Critical"
    elif temperature > 75:
        anomalies.append("High temperature warning")
        severity = "Warning" if severity == "Normal" else severity
    
    # Check for rapid changes if historical data exists
    if tyre:
        rapid_change = detect_rapid_pressure_change(tyre, pressure)
        if rapid_change:
            anomalies.append("Rapid pressure loss detected")
            severity = "Critical"
    
    return {
        "tyre": tyre,
        "severity": severity,
        "anomalies": anomalies,
        "requires_action": severity in ["Critical", "Warning"],
        "pressure_psi": pressure,
        "temperature_c": temperature
    }


def detect_rapid_pressure_change(tyre: str, current_pressure: float) -> bool:
    """
    Detect rapid pressure loss (>10 psi in last hour)
    """
    try:
        # Get last pressure reading within 1 hour
        last_reading = frappe.db.sql("""
            SELECT pressure_psi
            FROM `tabTyre Sensor Data`
            WHERE tyre = %s
            AND timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
            ORDER BY timestamp DESC
            LIMIT 1, 1
        """, (tyre,), as_dict=True)
        
        if last_reading and len(last_reading) > 0:
            last_pressure = flt(last_reading[0].get("pressure_psi", 0))
            pressure_drop = last_pressure - current_pressure
            
            if pressure_drop > 10:
                return True
                
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Error checking pressure change: {str(e)}")
    
    return False


def analyze_wear_pattern(tyre: str) -> Dict:
    """
    Analyze tyre wear pattern from inspection history
    Detects uneven wear which may indicate alignment/suspension issues
    
    Args:
        tyre: Tyre document name
        
    Returns:
        Dict with wear pattern analysis
    """
    # Get inspection history
    inspections = frappe.get_all(
        "Tyre Inspection Log",
        filters={"tyre": tyre},
        fields=["tread_depth_mm", "inspection_date", "observations"],
        order_by="inspection_date asc"
    )
    
    if len(inspections) < 2:
        return {
            "status": "Insufficient data",
            "recommendation": "Require at least 2 inspections for pattern analysis"
        }
    
    # Calculate wear rate between inspections
    wear_rates = []
    
    for i in range(1, len(inspections)):
        prev = inspections[i-1]
        curr = inspections[i]
        
        tread_loss = flt(prev.get("tread_depth_mm", 0)) - flt(curr.get("tread_depth_mm", 0))
        
        # Calculate days between inspections
        if prev.get("inspection_date") and curr.get("inspection_date"):
            days_between = (curr["inspection_date"] - prev["inspection_date"]).days
            
            if days_between > 0:
                wear_rate = tread_loss / days_between
                wear_rates.append(wear_rate)
    
    if not wear_rates:
        return {
            "status": "Insufficient data",
            "recommendation": "Cannot calculate wear patterns"
        }
    
    # Analyze consistency
    avg_wear = sum(wear_rates) / len(wear_rates)
    max_wear = max(wear_rates)
    min_wear = min(wear_rates)
    variance = max_wear - min_wear
    
    # Classification
    if variance < 0.01:
        pattern = "Even wear"
        recommendation = "Tyre wear is consistent and normal"
    elif variance < 0.03:
        pattern = "Slightly uneven wear"
        recommendation = "Monitor tyre - consider rotation"
    else:
        pattern = "Uneven wear detected"
        recommendation = "Check vehicle alignment, suspension, and tyre pressure. Immediate inspection recommended."
    
    return {
        "status": pattern,
        "recommendation": recommendation,
        "avg_wear_mm_per_day": round(avg_wear, 4),
        "variance": round(variance, 4),
        "inspections_analyzed": len(inspections)
    }


def generate_tyre_insights(tyre: str) -> Dict:
    """
    Generate comprehensive AI insights for a tyre
    Main function called by dashboard/reports
    
    Args:
        tyre: Tyre document name
        
    Returns:
        Dict with comprehensive insights
    """
    tyre_doc = frappe.get_doc("Tyre", tyre)
    
    # Calculate health index
    health_index = calculate_health_index(tyre)
    condition = classify_tyre_condition(health_index)
    
    # Wear pattern analysis
    wear_analysis = analyze_wear_pattern(tyre)
    
    # Import calculator functions
    from tems.tems_tyre.utils.tyre_calculator import (
        calculate_cost_per_km,
        calculate_wear_rate,
        predict_replacement_date
    )
    
    cost_per_km = calculate_cost_per_km(tyre)
    wear_rate, wear_status = calculate_wear_rate(tyre)
    replacement_prediction = predict_replacement_date(tyre)
    
    # Compile insights
    insights = {
        "tyre": tyre,
        "health_index": health_index,
        "condition": condition,
        "cost_per_km": cost_per_km,
        "wear_rate_mm_per_1000km": wear_rate,
        "wear_status": wear_status,
        "wear_pattern": wear_analysis,
        "replacement_prediction": replacement_prediction,
        "vehicle": getattr(tyre_doc, "vehicle", None),
        "brand": getattr(tyre_doc, "brand", ""),
        "model": getattr(tyre_doc, "model", ""),
        "current_mileage": getattr(tyre_doc, "current_mileage", 0),
        "status": getattr(tyre_doc, "status", "")
    }
    
    # Generate recommendations
    recommendations = []
    
    if condition in ["Replace Soon", "Replace Immediately"]:
        recommendations.append(f"Action Required: {condition}")
    
    if wear_analysis.get("status") == "Uneven wear detected":
        recommendations.append("Vehicle inspection required - uneven wear detected")
    
    if replacement_prediction and replacement_prediction.get("days_until_replacement", 999) < 30:
        recommendations.append(f"Schedule replacement within {replacement_prediction['days_until_replacement']} days")
    
    if cost_per_km > 1.0:  # Threshold
        recommendations.append("Cost per km exceeds benchmark - review tyre selection")
    
    insights["recommendations"] = recommendations
    insights["requires_attention"] = len(recommendations) > 0
    
    return insights


def batch_analyze_fleet_tyres(vehicle: str = None) -> list:
    """
    Analyze all tyres in fleet or for specific vehicle
    Returns prioritized list for action
    
    Args:
        vehicle: Optional vehicle filter
        
    Returns:
        List of dicts with tyre insights, sorted by priority
    """
    filters = {"status": ["!=", "Disposed"]}
    if vehicle:
        filters["vehicle"] = vehicle
    
    tyres = frappe.get_all("Tyre", filters=filters, pluck="name")
    
    results = []
    
    for tyre in tyres:
        try:
            insights = generate_tyre_insights(tyre)
            results.append(insights)
        except Exception as e:
            frappe.logger("tems_tyre").error(f"Error analyzing tyre {tyre}: {str(e)}")
            continue
    
    # Sort by health index (lowest first = highest priority)
    results.sort(key=lambda x: x["health_index"])
    
    return results
