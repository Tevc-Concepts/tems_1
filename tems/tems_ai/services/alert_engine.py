"""
Alert Engine
============
Manages AI-generated alerts and notifications.
"""

import frappe
from typing import Dict, List, Optional
from datetime import datetime


def trigger_alert(
    domain: str,
    alert_type: str,
    severity: str,
    message: str,
    details: Optional[Dict] = None,
    recipients: Optional[List[str]] = None
) -> str:
    """
    Trigger an AI-generated alert.
    
    Args:
        domain: TEMS domain
        alert_type: Type of alert (maintenance, risk, anomaly, etc.)
        severity: high, medium, low
        message: Alert message
        details: Additional details
        recipients: List of users to notify
    
    Returns:
        Alert ID
    """
    # Create alert record in AI Insight Log with alert status
    alert_doc = frappe.get_doc({
        "doctype": "AI Insight Log",
        "domain": domain,
        "insight_type": alert_type,
        "prediction_value": severity,
        "details": frappe.as_json(details or {}),
        "status": "Alert",
        "alert_message": message,
        "timestamp": datetime.now()
    })
    
    alert_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    
    # Send notifications
    if recipients:
        _send_notifications(alert_doc.name, message, recipients)
    else:
        _send_notifications_by_role(domain, alert_type, message)
    
    return alert_doc.name


def _send_notifications(alert_id: str, message: str, recipients: List[str]):
    """Send notification to specific users."""
    for user in recipients:
        try:
            frappe.get_doc({
                "doctype": "Notification Log",
                "subject": "AI Alert",
                "email_content": message,
                "for_user": user,
                "type": "Alert",
                "document_type": "AI Insight Log",
                "document_name": alert_id
            }).insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Failed to send notification to {user}: {str(e)}", "Alert Engine")
    
    frappe.db.commit()


def _send_notifications_by_role(domain: str, alert_type: str, message: str):
    """Send notifications to users based on domain and alert type."""
    # Map domains and alert types to roles
    role_mapping = {
        "fleet": ["Fleet Manager", "Fleet Officer"],
        "operations": ["Operations Manager", "Operations Officer"],
        "safety": ["Safety Manager", "Safety Officer"],
        "finance": ["Finance Manager", "Finance Officer"]
    }
    
    roles = role_mapping.get(domain, ["TEMS Executive"])
    
    # Get users with these roles
    users = frappe.get_all(
        "Has Role",
        filters={"role": ["in", roles]},
        fields=["parent"],
        distinct=True
    )
    
    user_list = [u["parent"] for u in users]
    
    # Send email alerts
    for user in user_list:
        try:
            frappe.sendmail(
                recipients=[user],
                subject=f"TEMS AI Alert: {alert_type}",
                message=message,
                delayed=False
            )
        except Exception as e:
            frappe.log_error(f"Failed to send email to {user}: {str(e)}", "Alert Engine")


def check_threshold_breach(
    domain: str,
    metric: str,
    current_value: float,
    threshold: float,
    comparison: str = "greater"
) -> bool:
    """
    Check if a metric has breached its threshold.
    
    Args:
        domain: Domain name
        metric: Metric name
        current_value: Current metric value
        threshold: Threshold value
        comparison: 'greater' or 'less'
    
    Returns:
        True if threshold breached
    """
    if comparison == "greater":
        return current_value > threshold
    elif comparison == "less":
        return current_value < threshold
    else:
        return False


def evaluate_insights_for_alerts():
    """
    Scheduled task to evaluate recent insights and trigger alerts.
    Called from scheduler to check all recent insights.
    """
    # Get recent insights that haven't been evaluated
    insights = frappe.get_all(
        "AI Insight Log",
        filters={
            "status": "Generated",
            "creation": [">=", frappe.utils.add_days(None, -1)]
        },
        fields=["*"]
    )
    
    for insight in insights:
        _evaluate_single_insight(insight)


def _evaluate_single_insight(insight: Dict):
    """Evaluate a single insight and trigger alert if needed."""
    domain = insight.get("domain")
    insight_type = insight.get("insight_type")
    confidence = insight.get("confidence_score", 0.0)
    prediction = insight.get("prediction_value")
    
    # Get configuration for this insight type
    config = frappe.get_all(
        "AI Configuration",
        filters={
            "domain": domain,
            "insight_mode": insight_type,
            "enabled": 1
        },
        fields=["alert_threshold", "alert_on_high_confidence"],
        limit=1
    )
    
    if not config:
        return
    
    config = config[0]
    alert_threshold = config.get("alert_threshold", 0.8)
    alert_on_high = config.get("alert_on_high_confidence", 0)
    
    # Check if alert should be triggered
    should_alert = False
    alert_message = ""
    severity = "medium"
    
    if alert_on_high and confidence >= alert_threshold:
        should_alert = True
        alert_message = f"High confidence {insight_type} detected in {domain}: {prediction}"
        severity = "high" if confidence > 0.9 else "medium"
    
    # Domain-specific alert logic
    if domain == "fleet" and insight_type == "forecast":
        if "maintenance" in str(prediction).lower():
            should_alert = True
            alert_message = f"Predictive maintenance alert: {prediction}"
            severity = "high"
    
    elif domain == "safety" and insight_type == "risk":
        if str(prediction).lower() in ["high", "critical"]:
            should_alert = True
            alert_message = f"High safety risk detected: {prediction}"
            severity = "high"
    
    if should_alert:
        trigger_alert(
            domain=domain,
            alert_type=insight_type,
            severity=severity,
            message=alert_message,
            details={"insight_id": insight.get("name"), "confidence": confidence}
        )
        
        # Update insight status
        frappe.db.set_value("AI Insight Log", insight.get("name"), "status", "Alert Sent")
        frappe.db.commit()


def get_active_alerts(domain: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """
    Get active alerts, optionally filtered by domain.
    
    Args:
        domain: Optional domain filter
        limit: Number of alerts to retrieve
    
    Returns:
        List of alert records
    """
    filters = {"status": "Alert"}
    if domain:
        filters["domain"] = domain
    
    alerts = frappe.get_all(
        "AI Insight Log",
        filters=filters,
        fields=["*"],
        order_by="creation desc",
        limit=limit
    )
    
    return alerts
