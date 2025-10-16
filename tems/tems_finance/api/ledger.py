#Detect and flag unusual costs automatically.

import frappe
from tems.tems_ai.handlers.finance_ai import detect_cost_anomaly
from tems.tems_ai.services.alert_engine import trigger_alert

def on_ledger_submit(doc, method):
    """
    Check for cost anomalies when cost/revenue is submitted.
    """
    # first the email address of user with role - Finance manager
    finance_manager_email = frappe.get_all("User", filters={"roles": "Finance Manager"}, fields=["email"])
    
    # check if empty assign default platform support "code@tevcng.com"
    if not finance_manager_email:
        finance_manager_email = ["code@tevcng.com"]

    if doc.cost_amount and doc.cost_amount > 0:
        # Run anomaly detection
        anomaly = detect_cost_anomaly(
            vehicle=doc.vehicle,
            cost_amount=doc.cost_amount,
            cost_type=doc.cost_type
        )
        
        # Flag if anomaly detected
        if anomaly.get("anomaly"):
            doc.db_set("anomaly_detected", 1)
            doc.db_set("anomaly_severity", anomaly.get("severity"))
            
            # Alert finance team on high severity
            if anomaly.get("severity") in ["high", "critical"]:
                trigger_alert(
                    domain="finance",
                    alert_type="cost_anomaly",
                    severity="high",
                    message=f"Unusual cost detected: {doc.cost_type} for {doc.vehicle}",
                    details=anomaly,
                    recipients=finance_manager_email
                )