"""
Data Preprocessor
=================
Utilities for preparing data for AI model input.
"""

import frappe
from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta


def preprocess_fleet_data(vehicles: List[Dict]) -> Dict[str, Any]:
    """
    Preprocess fleet data for AI models.
    
    Args:
        vehicles: List of vehicle records
    
    Returns:
        Preprocessed feature dict
    """
    if not vehicles:
        return {}
    
    features = {
        "total_vehicles": len(vehicles),
        "avg_odometer": _safe_average([v.get("odometer", 0) for v in vehicles]),
        "vehicles_needing_maintenance": 0,
        "vehicle_features": []
    }
    
    for vehicle in vehicles:
        vehicle_features = {
            "name": vehicle.get("name"),
            "odometer": vehicle.get("odometer", 0),
            "days_since_maintenance": _days_since(vehicle.get("last_maintenance_date")),
            "age_years": _calculate_vehicle_age(vehicle.get("purchase_date"))
        }
        features["vehicle_features"].append(vehicle_features)
    
    return features


def preprocess_operations_data(trips: List[Dict]) -> Dict[str, Any]:
    """
    Preprocess operations/trip data for AI models.
    
    Args:
        trips: List of trip records
    
    Returns:
        Preprocessed feature dict
    """
    if not trips:
        return {}
    
    features = {
        "total_trips": len(trips),
        "avg_distance": _safe_average([t.get("distance", 0) for t in trips]),
        "avg_duration": _safe_average([t.get("estimated_duration", 0) for t in trips]),
        "trip_features": []
    }
    
    for trip in trips:
        trip_features = {
            "route": trip.get("route"),
            "distance": trip.get("distance", 0),
            "duration": trip.get("estimated_duration", 0)
        }
        features["trip_features"].append(trip_features)
    
    return features


def preprocess_safety_data(incidents: List[Dict]) -> Dict[str, Any]:
    """
    Preprocess safety/incident data for AI models.
    
    Args:
        incidents: List of incident records
    
    Returns:
        Preprocessed feature dict
    """
    if not incidents:
        return {}
    
    severity_counts = {}
    incident_type_counts = {}
    
    for incident in incidents:
        severity = incident.get("severity", "unknown")
        inc_type = incident.get("incident_type", "unknown")
        
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        incident_type_counts[inc_type] = incident_type_counts.get(inc_type, 0) + 1
    
    features = {
        "total_incidents": len(incidents),
        "severity_distribution": severity_counts,
        "incident_type_distribution": incident_type_counts,
        "high_severity_ratio": severity_counts.get("High", 0) / len(incidents) if incidents else 0
    }
    
    return features


def preprocess_finance_data(ledger: List[Dict]) -> Dict[str, Any]:
    """
    Preprocess financial data for AI models.
    
    Args:
        ledger: List of cost and revenue ledger entries
    
    Returns:
        Preprocessed feature dict
    """
    if not ledger:
        return {}
    
    total_cost = sum(e.get("cost_amount", 0) for e in ledger)
    total_revenue = sum(e.get("revenue_amount", 0) for e in ledger)
    
    features = {
        "total_entries": len(ledger),
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "profit_margin": (total_revenue - total_cost) / total_revenue if total_revenue > 0 else 0,
        "avg_cost_per_entry": total_cost / len(ledger),
        "avg_revenue_per_entry": total_revenue / len(ledger)
    }
    
    return features


def normalize_numeric_features(data: Dict, keys: List[str]) -> Dict:
    """
    Normalize numeric features to 0-1 range.
    
    Args:
        data: Data dict
        keys: Keys to normalize
    
    Returns:
        Data with normalized values
    """
    normalized = data.copy()
    
    for key in keys:
        if key in data and isinstance(data[key], (int, float)):
            value = data[key]
            # Simple min-max normalization (would use proper scaler in production)
            normalized[key] = max(0, min(1, value / 100))
    
    return normalized


def encode_categorical(value: str, categories: List[str]) -> List[int]:
    """
    One-hot encode a categorical value.
    
    Args:
        value: Categorical value
        categories: List of all possible categories
    
    Returns:
        One-hot encoded list
    """
    return [1 if cat == value else 0 for cat in categories]


def extract_time_features(date_field: Optional[str]) -> Dict:
    """
    Extract time-based features from a date field.
    
    Args:
        date_field: Date string or datetime
    
    Returns:
        Dict with time features (day_of_week, month, quarter, etc.)
    """
    if not date_field:
        return {}
    
    try:
        if isinstance(date_field, str):
            dt = datetime.fromisoformat(date_field)
        else:
            dt = date_field
        
        return {
            "day_of_week": dt.weekday(),
            "month": dt.month,
            "quarter": (dt.month - 1) // 3 + 1,
            "day_of_month": dt.day,
            "is_weekend": dt.weekday() >= 5
        }
    except (ValueError, AttributeError):
        return {}


def _safe_average(values: List[float]) -> float:
    """Calculate average safely handling empty lists."""
    return sum(values) / len(values) if values else 0.0


def _days_since(date_field: Optional[str]) -> int:
    """Calculate days since a date."""
    if not date_field:
        return 999
    
    try:
        if isinstance(date_field, str):
            date = datetime.fromisoformat(date_field)
        else:
            date = date_field
        
        delta = datetime.now() - date
        return delta.days
    except (ValueError, AttributeError):
        return 999


def _calculate_vehicle_age(purchase_date: Optional[str]) -> float:
    """Calculate vehicle age in years."""
    if not purchase_date:
        return 0.0
    
    days = _days_since(purchase_date)
    return days / 365.25
