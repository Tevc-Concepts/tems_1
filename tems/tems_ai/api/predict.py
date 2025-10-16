"""
AI Prediction API
=================
Whitelisted API endpoints for running AI predictions.
"""

import frappe
from typing import Dict, Any, Optional
from tems.tems_ai.services.model_manager import ModelManager, get_prediction
from tems.tems_ai.services.insights_engine import generate_insight


@frappe.whitelist()
def run(domain: str, dataset: Optional[Dict] = None, model: Optional[str] = None) -> Dict:
    """
    Run AI prediction for a specific domain.
    
    Args:
        domain: TEMS domain (fleet, operations, safety, finance)
        dataset: Optional input dataset (will fetch if not provided)
        model: Optional specific model name (will use domain default if not provided)
    
    Returns:
        Prediction result with insights
    
    Example:
        POST /api/method/tems_ai.api.predict.run
        {
            "domain": "fleet",
            "dataset": {"odometer": 50000, "days_since_maintenance": 180},
            "model": "Fleet Maintenance Predictor"
        }
    """
    try:
        # Validate domain
        valid_domains = ["fleet", "operations", "safety", "finance", "cargo", "passenger"]
        if domain not in valid_domains:
            frappe.throw(f"Invalid domain. Must be one of: {', '.join(valid_domains)}")
        
        # Parse dataset if it's a JSON string
        if isinstance(dataset, str):
            import json
            dataset = json.loads(dataset)
        
        if model:
            # Use specific model
            manager = ModelManager(model)
            result = manager.predict(dataset or {})
        else:
            # Use domain default configuration
            result = generate_insight(domain=domain, mode="forecast", context=dataset)
        
        return {
            "success": True,
            "domain": domain,
            "result": result
        }
    
    except Exception as e:
        frappe.log_error(f"Prediction API error: {str(e)}", "AI Predict API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def predict_maintenance(vehicle: str) -> Dict:
    """
    Predict maintenance needs for a specific vehicle.
    
    Args:
        vehicle: Vehicle name/ID
    
    Returns:
        Maintenance prediction with confidence score
    """
    try:
        # Get vehicle data
        vehicle_doc = frappe.get_doc("Vehicle", vehicle)
        
        # Prepare input features
        input_data = {
            "odometer": vehicle_doc.get("odometer", 0),
            "last_maintenance_date": vehicle_doc.get("last_maintenance_date"),
            "vehicle_age": vehicle_doc.get("model_year"),
            "recent_issues": _count_recent_issues(vehicle)
        }
        
        # Get prediction
        result = generate_insight(domain="fleet", mode="forecast", context=input_data)
        
        return {
            "success": True,
            "vehicle": vehicle,
            "prediction": result
        }
    
    except Exception as e:
        frappe.log_error(f"Maintenance prediction error: {str(e)}", "AI Predict API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def predict_eta(trip: str) -> Dict:
    """
    Predict ETA for a trip.
    
    Args:
        trip: Trip Allocation name/ID
    
    Returns:
        ETA prediction with confidence
    """
    try:
        trip_doc = frappe.get_doc("Trip Allocation", trip)
        
        input_data = {
            "route": trip_doc.get("route"),
            "distance": trip_doc.get("distance", 0),
            "vehicle": trip_doc.get("vehicle"),
            "driver": trip_doc.get("driver"),
            "time_of_day": frappe.utils.now_datetime().hour
        }
        
        result = generate_insight(domain="operations", mode="forecast", context=input_data)
        
        return {
            "success": True,
            "trip": trip,
            "prediction": result
        }
    
    except Exception as e:
        frappe.log_error(f"ETA prediction error: {str(e)}", "AI Predict API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def predict_risk(driver: str, route: str) -> Dict:
    """
    Predict safety risk for a driver on a specific route.
    
    Args:
        driver: Driver/Employee ID
        route: Route name
    
    Returns:
        Risk assessment with score
    """
    try:
        # Get driver incident history
        incidents = frappe.get_all(
            "Incident Report",
            filters={"driver": driver},
            fields=["severity", "incident_type"],
            limit=10
        )
        
        input_data = {
            "driver": driver,
            "route": route,
            "incident_count": len(incidents),
            "high_severity_incidents": sum(1 for i in incidents if i.get("severity") == "High")
        }
        
        result = generate_insight(domain="safety", mode="risk", context=input_data)
        
        return {
            "success": True,
            "driver": driver,
            "route": route,
            "prediction": result
        }
    
    except Exception as e:
        frappe.log_error(f"Risk prediction error: {str(e)}", "AI Predict API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def batch_predict(domain: str, records: list) -> Dict:
    """
    Run batch predictions for multiple records.
    
    Args:
        domain: Domain name
        records: List of record IDs
    
    Returns:
        Batch prediction results
    """
    try:
        if isinstance(records, str):
            import json
            records = json.loads(records)
        
        results = []
        
        for record in records:
            try:
                result = run(domain=domain, dataset={"record": record})
                results.append({
                    "record": record,
                    "prediction": result
                })
            except Exception as e:
                results.append({
                    "record": record,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "domain": domain,
            "total": len(records),
            "results": results
        }
    
    except Exception as e:
        frappe.log_error(f"Batch prediction error: {str(e)}", "AI Predict API")
        return {
            "success": False,
            "error": str(e)
        }


def _count_recent_issues(vehicle: str) -> int:
    """Count recent maintenance issues for a vehicle."""
    try:
        count = frappe.db.count(
            "Maintenance Work Order",
            filters={
                "vehicle": vehicle,
                "creation": [">=", frappe.utils.add_days(None, -90)]
            }
        )
        return count
    except:
        return 0
