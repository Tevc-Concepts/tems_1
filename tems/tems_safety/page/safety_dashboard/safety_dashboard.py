
import frappe
from tems.tems_ai.handlers.safety_ai import predict_driver_risk_score

@frappe.whitelist()
def get_driver_performance_widget():
    """
    Get driver performance data for dashboard widget.
    """
    # Get all active drivers
    drivers = frappe.get_all(
        "Employee",
        filters={
            "designation": ["like", "%Driver%"],
            "status": "Active"
        },
        fields=["name", "employee_name"],
        limit=20
    )
    
    driver_scores = []
    
    for driver in drivers:
        try:
            # Get AI risk score
            risk_data = predict_driver_risk_score(driver["name"])
            
            driver_scores.append({
                "driver_id": driver["name"],
                "driver_name": driver["employee_name"],
                "safety_score": risk_data.get("safety_score", 0),
                "risk_level": risk_data.get("risk_level", "unknown"),
                "recent_incidents": risk_data.get("breakdown", {}).get("recent_incidents", 0)
            })
        except Exception as e:
            frappe.log_error(f"Error getting score for {driver['name']}: {str(e)}")
    
    # Sort by safety score (lowest first - needs attention)
    driver_scores.sort(key=lambda x: x["safety_score"])
    
    return {
        "drivers": driver_scores[:10],  # Top 10 needing attention
        "total_drivers": len(drivers),
        "high_risk_count": sum(1 for d in driver_scores if d["risk_level"] in ["high", "critical"])
    }