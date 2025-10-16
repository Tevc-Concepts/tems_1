"""
Model Registry Service
======================
Manages the catalog of available AI models and their configurations.
"""

import frappe
from typing import Dict, List, Optional


def get_enabled_models(domain: Optional[str] = None) -> List[Dict]:
    """
    Retrieve all enabled AI models, optionally filtered by domain.
    
    Args:
        domain: Optional domain filter (fleet, operations, safety, finance, etc.)
    
    Returns:
        List of model configurations
    """
    filters = {"enabled": 1}
    if domain:
        filters["domain"] = domain
    
    models = frappe.get_all(
        "AI Model Registry",
        filters=filters,
        fields=["name", "model_name", "model_type", "domain", "source", 
                "endpoint_url", "model_path", "api_key", "confidence_threshold"]
    )
    
    return models


def get_model_by_name(model_name: str) -> Optional[Dict]:
    """
    Get a specific model configuration by name.
    
    Args:
        model_name: Name of the model
    
    Returns:
        Model configuration dict or None
    """
    try:
        model = frappe.get_doc("AI Model Registry", model_name)
        return model.as_dict()
    except frappe.DoesNotExistError:
        return None


def register_model(model_data: Dict) -> str:
    """
    Register a new AI model in the registry.
    
    Args:
        model_data: Dict containing model configuration
    
    Returns:
        Name of the created model
    """
    doc = frappe.get_doc({
        "doctype": "AI Model Registry",
        **model_data
    })
    doc.insert()
    frappe.db.commit()
    
    return doc.name


def validate_model_availability(model_name: str) -> bool:
    """
    Check if a model is available and properly configured.
    
    Args:
        model_name: Name of the model to validate
    
    Returns:
        True if model is available and enabled
    """
    model = get_model_by_name(model_name)
    
    if not model:
        return False
    
    if not model.get("enabled"):
        return False
    
    # Check if model source is configured
    source = model.get("source")
    if source == "Local" and not model.get("model_path"):
        return False
    
    if source == "API" and not model.get("endpoint_url"):
        return False
    
    return True


def get_models_by_task(task_type: str) -> List[Dict]:
    """
    Get all models suitable for a specific task type.
    
    Args:
        task_type: Type of task (e.g., "maintenance_prediction", "eta_forecast")
    
    Returns:
        List of suitable models
    """
    # Get AI configurations that map tasks to models
    configs = frappe.get_all(
        "AI Configuration",
        filters={"enabled": 1, "task_type": task_type},
        fields=["model", "domain", "confidence_threshold"]
    )
    
    model_names = [c["model"] for c in configs]
    
    if not model_names:
        return []
    
    models = frappe.get_all(
        "AI Model Registry",
        filters={"name": ["in", model_names], "enabled": 1},
        fields=["*"]
    )
    
    return models
