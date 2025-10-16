"""
AI Analysis API
===============
Whitelisted API endpoints for analyzing data and generating insights.
"""

import frappe
from typing import Dict, Optional, List
from tems.tems_ai.services.insights_engine import get_recent_insights, get_insight_summary
from tems.tems_ai.services.alert_engine import get_active_alerts
from tems.tems_ai.utils.metrics import evaluate_model_performance, track_model_drift


@frappe.whitelist()
def run(domain: str, analysis_type: str = "summary", days: int = 7) -> Dict:
    """
    Run analysis on AI insights for a domain.
    
    Args:
        domain: TEMS domain
        analysis_type: Type of analysis (summary, trends, alerts)
        days: Time period for analysis
    
    Returns:
        Analysis results
    
    Example:
        POST /api/method/tems_ai.api.analyze.run
        {
            "domain": "fleet",
            "analysis_type": "summary",
            "days": 30
        }
    """
    try:
        if analysis_type == "summary":
            result = get_insight_summary(domain, days)
        
        elif analysis_type == "trends":
            result = _analyze_trends(domain, days)
        
        elif analysis_type == "alerts":
            result = get_active_alerts(domain)
        
        else:
            frappe.throw(f"Unknown analysis type: {analysis_type}")
        
        return {
            "success": True,
            "domain": domain,
            "analysis_type": analysis_type,
            "result": result
        }
    
    except Exception as e:
        frappe.log_error(f"Analysis API error: {str(e)}", "AI Analyze API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_insights(domain: Optional[str] = None, limit: int = 20) -> Dict:
    """
    Get recent AI insights.
    
    Args:
        domain: Optional domain filter
        limit: Number of insights to retrieve
    
    Returns:
        List of insights
    """
    try:
        insights = get_recent_insights(domain, limit)
        
        return {
            "success": True,
            "domain": domain,
            "total": len(insights),
            "insights": insights
        }
    
    except Exception as e:
        frappe.log_error(f"Get insights error: {str(e)}", "AI Analyze API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_alerts(domain: Optional[str] = None, limit: int = 20) -> Dict:
    """
    Get active AI alerts.
    
    Args:
        domain: Optional domain filter
        limit: Number of alerts to retrieve
    
    Returns:
        List of alerts
    """
    try:
        alerts = get_active_alerts(domain, limit)
        
        return {
            "success": True,
            "domain": domain,
            "total": len(alerts),
            "alerts": alerts
        }
    
    except Exception as e:
        frappe.log_error(f"Get alerts error: {str(e)}", "AI Analyze API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def model_performance(model_name: str, limit: int = 100) -> Dict:
    """
    Get performance metrics for a specific AI model.
    
    Args:
        model_name: Name of the model
        limit: Number of predictions to analyze
    
    Returns:
        Performance metrics
    """
    try:
        metrics = evaluate_model_performance(model_name, limit)
        
        return {
            "success": True,
            "metrics": metrics
        }
    
    except Exception as e:
        frappe.log_error(f"Model performance error: {str(e)}", "AI Analyze API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def model_drift(model_name: str, window_days: int = 30) -> Dict:
    """
    Analyze model performance drift over time.
    
    Args:
        model_name: Name of the model
        window_days: Time window for analysis
    
    Returns:
        Drift analysis
    """
    try:
        drift_analysis = track_model_drift(model_name, window_days)
        
        return {
            "success": True,
            "analysis": drift_analysis
        }
    
    except Exception as e:
        frappe.log_error(f"Model drift error: {str(e)}", "AI Analyze API")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def domain_dashboard(domain: str) -> Dict:
    """
    Get complete AI dashboard data for a domain.
    
    Args:
        domain: Domain name
    
    Returns:
        Dashboard data including insights, alerts, and metrics
    """
    try:
        # Get recent insights
        insights = get_recent_insights(domain, 10)
        
        # Get active alerts
        alerts = get_active_alerts(domain, 10)
        
        # Get summary
        summary = get_insight_summary(domain, 7)
        
        # Get AI configurations for this domain
        configs = frappe.get_all(
            "AI Configuration",
            filters={"domain": domain},
            fields=["name", "insight_mode", "model", "enabled"]
        )
        
        return {
            "success": True,
            "domain": domain,
            "dashboard": {
                "recent_insights": insights,
                "active_alerts": alerts,
                "summary": summary,
                "configurations": configs,
                "stats": {
                    "total_insights": len(insights),
                    "total_alerts": len(alerts),
                    "enabled_models": sum(1 for c in configs if c.get("enabled"))
                }
            }
        }
    
    except Exception as e:
        frappe.log_error(f"Domain dashboard error: {str(e)}", "AI Analyze API")
        return {
            "success": False,
            "error": str(e)
        }


def _analyze_trends(domain: str, days: int) -> Dict:
    """Analyze insight trends for a domain."""
    insights = frappe.db.sql("""
        SELECT 
            DATE(creation) as date,
            insight_type,
            AVG(confidence_score) as avg_confidence,
            COUNT(*) as count
        FROM `tabAI Insight Log`
        WHERE domain = %s
        AND DATE(creation) >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY DATE(creation), insight_type
        ORDER BY date
    """, (domain, days), as_dict=True)
    
    return {
        "domain": domain,
        "period_days": days,
        "trends": insights
    }
