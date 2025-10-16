"""
AI Training API
===============
API endpoints for training and managing AI models.
"""

import frappe
from typing import Dict, Optional


@frappe.whitelist()
def run(model_name: str, training_data: Optional[Dict] = None) -> Dict:
    """
    Trigger model training or retraining.
    
    Args:
        model_name: Name of the model to train
        training_data: Optional training dataset
    
    Returns:
        Training job status
    
    Note:
        This is a stub for future implementation.
        In production, this would trigger background training jobs.
    """
    try:
        # Validate model exists
        model = frappe.get_doc("AI Model Registry", model_name)
        
        if not model:
            frappe.throw(f"Model '{model_name}' not found")
        
        # In production, trigger background training job
        # For now, return success stub
        
        return {
            "success": True,
            "model": model_name,
            "status": "training_queued",
            "message": "Training job has been queued. This is a stub implementation."
        }
    
    except Exception as e:
        frappe.log_error(f"Training API error: {str(e)}", "AI Train API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def schedule_training(model_name: str, frequency: str = "weekly") -> Dict:
    """
    Schedule automatic model retraining.
    
    Args:
        model_name: Name of the model
        frequency: Training frequency (daily, weekly, monthly)
    
    Returns:
        Schedule configuration
    """
    try:
        # Update model configuration
        model = frappe.get_doc("AI Model Registry", model_name)
        model.auto_retrain = 1
        model.retrain_frequency = frequency
        model.save()
        
        frappe.db.commit()
        
        return {
            "success": True,
            "model": model_name,
            "frequency": frequency,
            "message": f"Model will be retrained {frequency}"
        }
    
    except Exception as e:
        frappe.log_error(f"Schedule training error: {str(e)}", "AI Train API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_training_status(model_name: str) -> Dict:
    """
    Get training status for a model.
    
    Args:
        model_name: Name of the model
    
    Returns:
        Training status
    """
    try:
        model = frappe.get_doc("AI Model Registry", model_name)
        
        return {
            "success": True,
            "model": model_name,
            "status": {
                "auto_retrain": model.get("auto_retrain", 0),
                "retrain_frequency": model.get("retrain_frequency"),
                "last_trained": model.get("last_trained_date"),
                "training_status": "idle"  # Stub
            }
        }
    
    except Exception as e:
        frappe.log_error(f"Get training status error: {str(e)}", "AI Train API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def validate_training_data(domain: str, record_count: Optional[int] = None) -> Dict:
    """
    Validate if sufficient training data exists for a domain.
    
    Args:
        domain: Domain name
        record_count: Optional expected record count
    
    Returns:
        Validation results
    """
    try:
        validation_results = {}
        
        if domain == "fleet":
            vehicle_count = frappe.db.count("Vehicle")
            maintenance_count = frappe.db.count("Maintenance Work Order")
            validation_results = {
                "vehicles": vehicle_count,
                "maintenance_records": maintenance_count,
                "sufficient": vehicle_count >= 10 and maintenance_count >= 50
            }
        
        elif domain == "operations":
            trip_count = frappe.db.count("Trip Allocation")
            validation_results = {
                "trips": trip_count,
                "sufficient": trip_count >= 100
            }
        
        elif domain == "safety":
            incident_count = frappe.db.count("Incident Report")
            validation_results = {
                "incidents": incident_count,
                "sufficient": incident_count >= 30
            }
        
        elif domain == "finance":
            ledger_count = frappe.db.count("Cost And Revenue Ledger")
            validation_results = {
                "ledger_entries": ledger_count,
                "sufficient": ledger_count >= 100
            }
        
        return {
            "success": True,
            "domain": domain,
            "validation": validation_results
        }
    
    except Exception as e:
        frappe.log_error(f"Validate training data error: {str(e)}", "AI Train API")
        return {
            "success": False,
            "error": str(e)
        }
