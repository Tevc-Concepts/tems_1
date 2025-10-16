"""
Insights Engine
===============
Generates AI-powered insights and recommendations across TEMS domains.
"""

import frappe
from typing import Dict, List, Optional, Any
from datetime import datetime
from tems.tems_ai.services.model_manager import ModelManager
from tems.tems_ai.services.model_registry import get_models_by_task


def generate_insight(domain: str, mode: str, context: Optional[Dict] = None) -> Dict:
    """
    Generate AI insight for a specific domain and mode.
    
    Args:
        domain: TEMS domain (fleet, operations, safety, finance, etc.)
        mode: Type of insight (forecast, anomaly, recommendation, risk)
        context: Optional context data for the insight
    
    Returns:
        Insight result with predictions and recommendations
    """
    # Get AI configuration for this domain and mode
    config = _get_ai_config(domain, mode)
    
    if not config:
        return {
            "error": f"No AI configuration found for {domain}/{mode}",
            "enabled": False
        }
    
    if not config.get("enabled"):
        return {
            "error": f"AI is disabled for {domain}/{mode}",
            "enabled": False
        }
    
    # Get the model to use
    model_name = config.get("model")
    
    if not model_name:
        return {
            "error": "No model assigned to this configuration",
            "enabled": True
        }
    
    # Fetch data for the domain
    input_data = _fetch_domain_data(domain, mode, context)
    
    # Run prediction
    manager = ModelManager(model_name)
    prediction_result = manager.predict(input_data)
    
    # Generate insight record
    insight = _create_insight_record(
        domain=domain,
        mode=mode,
        config=config,
        prediction=prediction_result,
        context=context
    )
    
    return insight


def _get_ai_config(domain: str, mode: str) -> Optional[Dict]:
    """Retrieve AI configuration for domain and mode."""
    configs = frappe.get_all(
        "AI Configuration",
        filters={
            "domain": domain,
            "insight_mode": mode
        },
        fields=["*"],
        limit=1
    )
    
    return configs[0] if configs else None


def _fetch_domain_data(domain: str, mode: str, context: Optional[Dict]) -> Dict:
    """
    Fetch relevant data from the domain for AI processing.
    
    Args:
        domain: Domain name
        mode: Insight mode
        context: Additional context
    
    Returns:
        Preprocessed data dict ready for model input
    """
    if context:
        return context
    
    # Default data fetching logic per domain
    if domain == "fleet":
        return _fetch_fleet_data(mode)
    elif domain == "operations":
        return _fetch_operations_data(mode)
    elif domain == "safety":
        return _fetch_safety_data(mode)
    elif domain == "finance":
        return _fetch_finance_data(mode)
    else:
        return {}


def _fetch_fleet_data(mode: str) -> Dict:
    """Fetch fleet-specific data for AI processing."""
    if mode == "forecast":
        # Get maintenance history
        vehicles = frappe.get_all(
            "Vehicle",
            fields=["name", "odometer", "last_maintenance_date"],
            limit=10
        )
        return {"vehicles": vehicles, "mode": mode}
    
    return {"mode": mode}


def _fetch_operations_data(mode: str) -> Dict:
    """Fetch operations-specific data for AI processing."""
    if mode == "forecast":
        # Get recent trips for ETA prediction
        trips = frappe.get_all(
            "Trip Allocation",
            fields=["name", "route", "distance", "estimated_duration"],
            limit=20,
            order_by="creation desc"
        )
        return {"trips": trips, "mode": mode}
    
    return {"mode": mode}


def _fetch_safety_data(mode: str) -> Dict:
    """Fetch safety-specific data for AI processing."""
    if mode == "risk":
        # Get incident history
        incidents = frappe.get_all(
            "Incident Report",
            fields=["name", "severity", "incident_type", "driver"],
            limit=50,
            order_by="creation desc"
        )
        return {"incidents": incidents, "mode": mode}
    
    return {"mode": mode}


def _fetch_finance_data(mode: str) -> Dict:
    """Fetch finance-specific data for AI processing."""
    if mode == "forecast":
        # Get cost and revenue data
        ledger = frappe.get_all(
            "Cost And Revenue Ledger",
            fields=["vehicle", "cost_amount", "revenue_amount", "transaction_date"],
            limit=100,
            order_by="transaction_date desc"
        )
        return {"ledger": ledger, "mode": mode}
    
    return {"mode": mode}


def _create_insight_record(
    domain: str,
    mode: str,
    config: Dict,
    prediction: Dict,
    context: Optional[Dict]
) -> Dict:
    """
    Create and save an AI Insight Log record.
    
    Args:
        domain: Domain name
        mode: Insight mode
        config: AI configuration used
        prediction: Prediction result from model
        context: Additional context
    
    Returns:
        Created insight record
    """
    try:
        insight_doc = frappe.get_doc({
            "doctype": "AI Insight Log",
            "domain": domain,
            "insight_type": mode,
            "model_used": config.get("model"),
            "prediction_value": str(prediction.get("prediction")),
            "confidence_score": prediction.get("confidence", 0.0),
            "details": frappe.as_json(prediction.get("details", {})),
            "context_data": frappe.as_json(context or {}),
            "timestamp": datetime.now(),
            "status": "Generated"
        })
        
        insight_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return insight_doc.as_dict()
    
    except Exception as e:
        frappe.log_error(f"Failed to create insight record: {str(e)}", "Insights Engine")
        return {
            "error": str(e),
            "prediction": prediction
        }


def get_recent_insights(domain: Optional[str] = None, limit: int = 10) -> List[Dict]:
    """
    Get recent AI insights, optionally filtered by domain.
    
    Args:
        domain: Optional domain filter
        limit: Number of insights to retrieve
    
    Returns:
        List of insight records
    """
    filters = {}
    if domain:
        filters["domain"] = domain
    
    insights = frappe.get_all(
        "AI Insight Log",
        filters=filters,
        fields=["*"],
        order_by="creation desc",
        limit=limit
    )
    
    return insights


def get_insight_summary(domain: str, days: int = 7) -> Dict:
    """
    Get summary of AI insights for a domain over a period.
    
    Args:
        domain: Domain name
        days: Number of days to look back
    
    Returns:
        Summary statistics
    """
    insights = frappe.db.sql("""
        SELECT 
            COUNT(*) as total_insights,
            AVG(confidence_score) as avg_confidence,
            insight_type,
            COUNT(*) as count_by_type
        FROM `tabAI Insight Log`
        WHERE domain = %s
        AND DATE(creation) >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY insight_type
    """, (domain, days), as_dict=True)
    
    return {
        "domain": domain,
        "period_days": days,
        "insights": insights
    }
