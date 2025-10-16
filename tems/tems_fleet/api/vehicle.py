import frappe
from tems.tems_ai.handlers.fleet_ai import predict_maintenance_schedule
from tems.tems_ai.services.alert_engine import trigger_alert

# Automatically alert fleet managers when a vehicle is due for maintenance
def on_vehicle_update(doc, method):
    """
    Hook that runs when a vehicle is updated.
    Checks if maintenance is needed.
    """
    # first get the list of all email of user with role - fleet managers
    fleet_manager_emails = frappe.get_all("User", filters={"roles": "Fleet Manager"}, fields=["email"])
    
    # check if empty assign default platform support "code@tevcng.com"
    if not fleet_manager_emails:
        fleet_manager_emails = ["code@tevcng.com"]

    # Only check vehicles that are active and have odometer data
    if doc.status == "Active" and doc.odometer:
        # Get AI prediction
        prediction = predict_maintenance_schedule(doc.name)
        
        # Store prediction on vehicle doc
        doc.db_set("ai_maintenance_score", prediction.get("confidence", 0))
        
        # If high confidence that maintenance is needed, trigger alert
        if prediction.get("confidence", 0) > 0.85:
            trigger_alert(
                domain="fleet",
                alert_type="predictive_maintenance",
                severity="high",
                message=f"Vehicle {doc.name} requires maintenance soon",
                details=prediction,
                recipients=fleet_manager_emails
            )
            