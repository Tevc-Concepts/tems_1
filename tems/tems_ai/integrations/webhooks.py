
import frappe
import requests

def send_insight_webhook(insight_doc):
    """
    Send AI insight to external webhook.
    Called after insight is created.
    """
    # Get webhook settings
    webhook_url = frappe.db.get_single_value("TEMS Settings", "ai_webhook_url")
    webhook_secret = frappe.db.get_single_value("TEMS Settings", "ai_webhook_secret")
    
    if not webhook_url:
        return
    
    # Prepare payload
    payload = {
        "event": "ai_insight_generated",
        "timestamp": insight_doc.creation.isoformat(),
        "data": {
            "domain": insight_doc.domain,
            "insight_type": insight_doc.insight_type,
            "prediction": insight_doc.prediction_value,
            "confidence": insight_doc.confidence_score,
            "model": insight_doc.model_used
        }
    }
    
    # Send webhook
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Secret": webhook_secret
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        response.raise_for_status()
        frappe.logger().info(f"Webhook sent successfully for {insight_doc.name}")
        
    except Exception as e:
        frappe.log_error(f"Webhook failed: {str(e)}", "AI Webhook")