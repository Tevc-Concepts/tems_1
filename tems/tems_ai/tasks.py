"""
TEMS AI Scheduled Tasks
========================
Background tasks for AI operations, model updates, and alert generation.
"""

import frappe
from tems.tems_ai.services.alert_engine import evaluate_insights_for_alerts
from tems.tems_ai.services.insights_engine import generate_insight
from frappe.utils import today, add_days
from tems.tems_ai.services.insights_engine import get_recent_insights
from tems.tems_ai.services.alert_engine import get_active_alerts


def generate_daily_insights():
    """
    Scheduled task to generate AI insights daily for all domains.
    Run at 02:00 AM daily.
    """
    frappe.logger().info("Starting daily AI insights generation")
    
    domains = ["fleet", "operations", "safety", "finance"]
    
    for domain in domains:
        try:
            # Check if AI is enabled for this domain
            configs = frappe.get_all(
                "AI Configuration",
                filters={"domain": domain, "enabled": 1},
                fields=["insight_mode"]
            )
            
            for config in configs:
                insight_mode = config.get("insight_mode")
                try:
                    frappe.logger().info(f"Generating {insight_mode} insight for {domain}")
                    generate_insight(domain=domain, mode=insight_mode)
                except Exception as e:
                    frappe.log_error(f"Failed to generate {insight_mode} for {domain}: {str(e)}", 
                                   "AI Daily Insights")
        
        except Exception as e:
            frappe.log_error(f"Failed to process domain {domain}: {str(e)}", 
                           "AI Daily Insights")
    
    frappe.db.commit()
    frappe.logger().info("Completed daily AI insights generation")


def evaluate_alerts_hourly():
    """
    Scheduled task to evaluate recent insights and trigger alerts.
    Run hourly.
    """
    frappe.logger().info("Starting hourly alert evaluation")
    
    try:
        evaluate_insights_for_alerts()
        frappe.db.commit()
        frappe.logger().info("Completed hourly alert evaluation")
    except Exception as e:
        frappe.log_error(f"Alert evaluation failed: {str(e)}", "AI Alert Evaluation")


def cleanup_old_insights():
    """
    Scheduled task to clean up old AI insights.
    Run weekly on Sunday at 03:00 AM.
    """
    frappe.logger().info("Starting AI insights cleanup")
    
    try:
        # Delete insights older than 90 days
        frappe.db.sql("""
            DELETE FROM `tabAI Insight Log`
            WHERE DATE(creation) < DATE_SUB(CURDATE(), INTERVAL 90 DAY)
        """)
        
        frappe.db.commit()
        frappe.logger().info("Completed AI insights cleanup")
    except Exception as e:
        frappe.log_error(f"Insights cleanup failed: {str(e)}", "AI Cleanup")


def update_model_performance_metrics():
    """
    Scheduled task to update model performance metrics.
    Run daily at 04:00 AM.
    """
    frappe.logger().info("Starting model performance metrics update")
    
    try:
        from tems.tems_ai.utils.metrics import evaluate_model_performance
        
        # Get all enabled models
        models = frappe.get_all(
            "AI Model Registry",
            filters={"enabled": 1},
            fields=["name"]
        )
        
        for model in models:
            try:
                model_name = model.get("name")
                metrics = evaluate_model_performance(model_name)
                
                # Update model doc with latest metrics
                model_doc = frappe.get_doc("AI Model Registry", model_name)
                model_doc.last_performance_check = frappe.utils.now()
                model_doc.avg_confidence = metrics.get("avg_confidence", 0)
                model_doc.total_predictions = metrics.get("total_predictions", 0)
                model_doc.save(ignore_permissions=True)
                
            except Exception as e:
                frappe.log_error(f"Failed to update metrics for {model_name}: {str(e)}", 
                               "AI Model Metrics")
        
        frappe.db.commit()
        frappe.logger().info("Completed model performance metrics update")
    except Exception as e:
        frappe.log_error(f"Model metrics update failed: {str(e)}", "AI Model Metrics")


def retrain_models_weekly():
    """
    Scheduled task to retrain AI models that have auto-retrain enabled.
    Run weekly on Monday at 01:00 AM.
    """
    frappe.logger().info("Starting weekly model retraining")
    
    try:
        # Get models with auto-retrain enabled
        models = frappe.get_all(
            "AI Model Registry",
            filters={
                "enabled": 1,
                "auto_retrain": 1,
                "retrain_frequency": "weekly"
            },
            fields=["name"]
        )
        
        for model in models:
            model_name = model.get("name")
            frappe.logger().info(f"Queuing retraining for {model_name}")
            
            # In production, this would trigger actual model training
            # For now, just log
            frappe.log_error(f"Retrain queued for {model_name}", "AI Model Training")
        
        frappe.db.commit()
        frappe.logger().info("Completed weekly model retraining queue")
    except Exception as e:
        frappe.log_error(f"Model retraining failed: {str(e)}", "AI Model Training")


def generate_fleet_maintenance_predictions():
    """
    Generate predictive maintenance insights for fleet.
    Run daily at 06:00 AM.
    """
    frappe.logger().info("Starting fleet maintenance predictions")
    
    try:
        from tems.tems_ai.handlers.fleet_ai import predict_maintenance_schedule
        
        # Get all active vehicles
        vehicles = frappe.get_all(
            "Vehicle",
            filters={"status": "Active"},
            fields=["name"],
            limit=50  # Process in batches
        )
        
        predictions_generated = 0
        
        for vehicle in vehicles:
            try:
                vehicle_name = vehicle.get("name")
                result = predict_maintenance_schedule(vehicle_name)
                
                if result.get("prediction"):
                    predictions_generated += 1
                    
                    # Check if immediate maintenance needed
                    confidence = result.get("confidence", 0)
                    if confidence > 0.8:
                        # Trigger alert
                        from tems.tems_ai.services.alert_engine import trigger_alert
                        trigger_alert(
                            domain="fleet",
                            alert_type="maintenance_prediction",
                            severity="medium",
                            message=f"Predictive maintenance recommended for {vehicle_name}",
                            details=result
                        )
                        
            except Exception as e:
                frappe.log_error(f"Failed to predict maintenance for {vehicle_name}: {str(e)}", 
                               "Fleet AI Predictions")
        
        frappe.db.commit()
        frappe.logger().info(f"Completed fleet maintenance predictions: {predictions_generated} vehicles processed")
    except Exception as e:
        frappe.log_error(f"Fleet predictions failed: {str(e)}", "Fleet AI Predictions")


def calculate_driver_risk_scores():
    """
    Calculate risk scores for all active drivers.
    Run daily at 05:00 AM.
    """
    frappe.logger().info("Starting driver risk score calculations")
    
    try:
        from tems.tems_ai.handlers.safety_ai import predict_driver_risk_score
        
        # Get all active drivers
        drivers = frappe.get_all(
            "Employee",
            filters={"designation": ["like", "%Driver%"], "status": "Active"},
            fields=["name"],
            limit=100
        )
        
        high_risk_count = 0
        
        for driver in drivers:
            try:
                driver_name = driver.get("name")
                result = predict_driver_risk_score(driver_name)
                
                risk_level = result.get("risk_level")
                
                # Alert on high risk drivers
                if risk_level in ["high", "critical"]:
                    high_risk_count += 1
                    
                    from tems.tems_ai.services.alert_engine import trigger_alert
                    trigger_alert(
                        domain="safety",
                        alert_type="driver_risk",
                        severity="high" if risk_level == "critical" else "medium",
                        message=f"High risk driver detected: {driver_name}",
                        details=result
                    )
                    
            except Exception as e:
                frappe.log_error(f"Failed to calculate risk for {driver_name}: {str(e)}", 
                               "Safety AI Predictions")
        
        frappe.db.commit()
        frappe.logger().info(f"Completed driver risk calculations: {high_risk_count} high-risk drivers identified")
    except Exception as e:
        frappe.log_error(f"Driver risk calculation failed: {str(e)}", "Safety AI Predictions")


def forecast_financial_metrics():
    """
    Generate financial forecasts for vehicles and operations.
    Run daily at 07:00 AM.
    """
    frappe.logger().info("Starting financial forecasting")
    
    try:
        from tems.tems_ai.handlers.finance_ai import predict_vehicle_profitability
        
        # Get top revenue vehicles
        vehicles = frappe.db.sql("""
            SELECT vehicle, SUM(revenue_amount) as total_revenue
            FROM `tabCost And Revenue Ledger`
            WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY vehicle
            ORDER BY total_revenue DESC
            LIMIT 20
        """, as_dict=True)
        
        forecasts_generated = 0
        
        for vehicle_data in vehicles:
            try:
                vehicle = vehicle_data.get("vehicle")
                if vehicle:
                    result = predict_vehicle_profitability(vehicle, forecast_days=7)
                    forecasts_generated += 1
                    
                    # Alert on negative profitability trend
                    if result.get("profitability_trend") == "negative":
                        from tems.tems_ai.services.alert_engine import trigger_alert
                        trigger_alert(
                            domain="finance",
                            alert_type="profitability_warning",
                            severity="medium",
                            message=f"Negative profitability trend for {vehicle}",
                            details=result
                        )
                        
            except Exception as e:
                frappe.log_error(f"Failed to forecast for {vehicle}: {str(e)}", 
                               "Finance AI Predictions")
        
        frappe.db.commit()
        frappe.logger().info(f"Completed financial forecasting: {forecasts_generated} vehicles processed")
    except Exception as e:
        frappe.log_error(f"Financial forecasting failed: {str(e)}", "Finance AI Predictions")


def send_daily_ai_summary():
    """
    Send daily AI summary email to executives.
    Scheduled to run daily at 08:00 AM.
    """
    # Get yesterday's insights
    insights = get_recent_insights(domain=None, limit=50)
    yesterday_insights = [
        i for i in insights 
        if frappe.utils.getdate(i.get("creation")) >= frappe.utils.add_days(today(), -1)
    ]
    
    # Get active alerts
    alerts = get_active_alerts(domain=None, limit=20)
    
    # Group by domain
    insights_by_domain = {}
    for insight in yesterday_insights:
        domain = insight.get("domain")
        if domain not in insights_by_domain:
            insights_by_domain[domain] = []
        insights_by_domain[domain].append(insight)
    
    # Build email content
    html_content = f"""
    <h2>TEMS AI Daily Summary - {today()}</h2>
    
    <h3>Summary</h3>
    <ul>
        <li>Total Insights Generated: {len(yesterday_insights)}</li>
        <li>Active Alerts: {len(alerts)}</li>
    </ul>
    
    <h3>Insights by Domain</h3>
    """
    
    for domain, domain_insights in insights_by_domain.items():
        html_content += f"""
        <h4>{domain.title()}</h4>
        <ul>
        """
        for insight in domain_insights[:5]:  # Top 5 per domain
            html_content += f"""
            <li>
                {insight.get("insight_type")}: {insight.get("prediction_value")} 
                (Confidence: {insight.get("confidence_score", 0):.2f})
            </li>
            """
        html_content += "</ul>"
    
    html_content += """
    <h3>Active Alerts</h3>
    <ul>
    """
    
    for alert in alerts[:10]:  # Top 10 alerts
        html_content += f"""
        <li>
            <strong>{alert.get("domain").upper()}</strong>: {alert.get("alert_message")}
        </li>
        """
    
    html_content += """
    </ul>
    
    <p>View full details in the AI Center workspace.</p>
    """
    
    # Send email
    # First get email of recipients - uses with roles TEMS Executive, Executive, Operation Manager
    recipient_emails = frappe.frappe.get_all("User", filters={"roles": ["TEMS Executive", "Executive", "Operation Manager"]}, fields=["email"])
    
    # check if empty assign default platform support "code@tevcng.com"
    if not recipient_emails:
        recipient_emails = ["code@tevcng.com"]

    frappe.sendmail(
        recipients=recipient_emails,
        subject=f"TEMS AI Daily Summary - {today()}",
        message=html_content,
        delayed=False
    )
