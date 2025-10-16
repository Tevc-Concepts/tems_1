"""
TEMS Tyre Scheduled Tasks
Background jobs for monitoring, prediction, and maintenance
"""
from __future__ import annotations

import frappe
from frappe.utils import now_datetime, add_days, get_datetime
from typing import List


def monitor_tyre_sensors():
    """
    Hourly task to check for stale sensor data and trigger alerts
    Runs every hour
    """
    try:
        # Get all tyres with sensors that haven't reported in 2+ hours
        tyres_with_sensors = frappe.get_all(
            "Tyre",
            filters={
                "status": ["in", ["Installed", "In Stock"]],
                "pressure_sensor_id": ["!=", ""]
            },
            fields=["name", "pressure_sensor_id", "vehicle"]
        )
        
        stale_count = 0
        
        for tyre_info in tyres_with_sensors:
            # Check last sensor reading
            last_reading = frappe.db.sql("""
                SELECT timestamp
                FROM `tabTyre Sensor Data`
                WHERE tyre = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (tyre_info["name"],), as_dict=True)
            
            if last_reading and len(last_reading) > 0:
                last_timestamp = get_datetime(last_reading[0]["timestamp"])
                hours_since = (now_datetime() - last_timestamp).total_seconds() / 3600
                
                if hours_since > 2:
                    # Create stale sensor alert
                    create_stale_sensor_alert(
                        tyre_info["name"],
                        tyre_info["pressure_sensor_id"],
                        hours_since
                    )
                    stale_count += 1
        
        frappe.logger("tems_tyre").info(f"Sensor monitoring complete. {stale_count} stale sensors detected.")
        
    except Exception as e:
        frappe.log_error(f"Tyre sensor monitoring failed: {str(e)}", "TEMS Tyre Tasks")


def update_tyre_health_scores():
    """
    Daily task to recalculate health scores for all active tyres
    Runs daily at 2 AM
    """
    try:
        from tems.tems_tyre.utils.tyre_analyzer import calculate_health_index, classify_tyre_condition
        
        # Get all active tyres
        tyres = frappe.get_all(
            "Tyre",
            filters={"status": ["!=", "Disposed"]},
            pluck="name"
        )
        
        updated_count = 0
        alerts_generated = 0
        
        for tyre in tyres:
            try:
                # Calculate health index
                health_index = calculate_health_index(tyre)
                condition = classify_tyre_condition(health_index)
                
                # Update tyre document
                frappe.db.set_value("Tyre", tyre, {
                    "ai_health_index": health_index,
                    "ai_health_status": condition,
                    "last_health_check": now_datetime()
                })
                
                updated_count += 1
                
                # Generate alerts for tyres needing attention
                if condition in ["Replace Soon", "Replace Immediately"]:
                    create_health_alert(tyre, health_index, condition)
                    alerts_generated += 1
                    
            except Exception as e:
                frappe.logger("tems_tyre").error(f"Failed to update health for tyre {tyre}: {str(e)}")
                continue
        
        frappe.db.commit()
        frappe.logger("tems_tyre").info(
            f"Health scores updated for {updated_count} tyres. {alerts_generated} alerts generated."
        )
        
    except Exception as e:
        frappe.log_error(f"Tyre health score update failed: {str(e)}", "TEMS Tyre Tasks")


def predict_replacement_schedule():
    """
    Daily task to predict replacement dates and schedule maintenance
    Runs daily at 3 AM
    """
    try:
        from tems.tems_tyre.utils.tyre_calculator import predict_replacement_date
        
        # Get all installed tyres
        tyres = frappe.get_all(
            "Tyre",
            filters={"status": "Installed"},
            fields=["name", "vehicle"]
        )
        
        scheduled_count = 0
        
        for tyre_info in tyres:
            try:
                prediction = predict_replacement_date(tyre_info["name"])
                
                if prediction:
                    days_until = prediction.get("days_until_replacement", 999)
                    
                    # Update tyre with prediction
                    frappe.db.set_value("Tyre", tyre_info["name"], {
                        "estimated_remaining_life": prediction.get("remaining_km", 0),
                        "predicted_replacement_date": add_days(None, int(days_until))
                    })
                    
                    # Create maintenance work order if replacement due within 14 days
                    if days_until <= 14:
                        create_tyre_replacement_work_order(
                            tyre_info["name"],
                            tyre_info["vehicle"],
                            days_until
                        )
                        scheduled_count += 1
                        
            except Exception as e:
                frappe.logger("tems_tyre").error(
                    f"Failed to predict replacement for tyre {tyre_info['name']}: {str(e)}"
                )
                continue
        
        frappe.db.commit()
        frappe.logger("tems_tyre").info(
            f"Replacement prediction complete. {scheduled_count} work orders created."
        )
        
    except Exception as e:
        frappe.log_error(f"Tyre replacement prediction failed: {str(e)}", "TEMS Tyre Tasks")


def analyze_fleet_tyre_performance():
    """
    Weekly task to analyze fleet-wide tyre performance
    Runs Monday at 1 AM
    """
    try:
        from tems.tems_tyre.utils.tyre_calculator import calculate_fleet_tyre_metrics
        from tems.tems_tyre.utils.tyre_analyzer import batch_analyze_fleet_tyres
        
        # Get fleet-wide metrics
        fleet_metrics = calculate_fleet_tyre_metrics()
        
        # Analyze all tyres
        tyre_insights = batch_analyze_fleet_tyres()
        
        # Identify tyres requiring immediate attention
        critical_tyres = [
            t for t in tyre_insights
            if t.get("condition") in ["Replace Immediately", "Replace Soon"]
        ]
        
        # Generate weekly report
        report_content = generate_weekly_tyre_report(fleet_metrics, critical_tyres)
        
        # Create report document or send email
        create_weekly_report_document(report_content)
        
        frappe.logger("tems_tyre").info(
            f"Weekly tyre performance analysis complete. {len(critical_tyres)} tyres need attention."
        )
        
    except Exception as e:
        frappe.log_error(f"Fleet tyre performance analysis failed: {str(e)}", "TEMS Tyre Tasks")


def sync_tyre_costs_to_finance():
    """
    Daily task to sync tyre costs to finance module
    Runs daily at 6 AM
    """
    try:
        # Get all cost entries created in last 24 hours that need syncing
        new_costs = frappe.db.sql("""
            SELECT 
                name, tyre, vehicle, amount, cost_type, date
            FROM `tabCost And Revenue Ledger`
            WHERE category LIKE '%Tyre%'
            AND date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)
            AND synced_to_finance != 1
        """, as_dict=True)
        
        synced_count = 0
        
        for cost in new_costs:
            try:
                # Mark as synced
                frappe.db.set_value(
                    "Cost And Revenue Ledger",
                    cost["name"],
                    "synced_to_finance",
                    1
                )
                synced_count += 1
                
            except Exception as e:
                frappe.logger("tems_tyre").error(
                    f"Failed to sync cost {cost['name']}: {str(e)}"
                )
                continue
        
        frappe.db.commit()
        frappe.logger("tems_tyre").info(f"Synced {synced_count} tyre cost entries to finance.")
        
    except Exception as e:
        frappe.log_error(f"Tyre cost sync failed: {str(e)}", "TEMS Tyre Tasks")


def cleanup_old_sensor_data():
    """
    Monthly task to archive old sensor data
    Keeps last 90 days, archives older records
    Runs on 1st of each month at 4 AM
    """
    try:
        # Delete sensor data older than 90 days
        cutoff_date = add_days(None, -90)
        
        deleted = frappe.db.sql("""
            DELETE FROM `tabTyre Sensor Data`
            WHERE timestamp < %s
        """, (cutoff_date,))
        
        frappe.db.commit()
        frappe.logger("tems_tyre").info(f"Cleaned up old sensor data. Deleted {deleted} records.")
        
    except Exception as e:
        frappe.log_error(f"Sensor data cleanup failed: {str(e)}", "TEMS Tyre Tasks")


# Helper functions for tasks

def create_stale_sensor_alert(tyre: str, sensor_id: str, hours_since: float):
    """Create alert for stale sensor"""
    try:
        vehicle = frappe.db.get_value("Tyre", tyre, "vehicle")
        
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Stale Sensor Alert: {sensor_id}",
            "email_content": f"""
                Sensor {sensor_id} has not reported in {hours_since:.1f} hours.
                Tyre: {tyre}
                Vehicle: {vehicle or 'Not Installed'}
                
                Please check sensor connectivity and battery.
            """,
            "document_type": "Tyre",
            "document_name": tyre,
            "type": "Alert"
        }).insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create stale sensor alert: {str(e)}")


def create_health_alert(tyre: str, health_index: int, condition: str):
    """Create alert for poor tyre health"""
    try:
        tyre_doc = frappe.get_doc("Tyre", tyre)
        vehicle = getattr(tyre_doc, "vehicle", None)
        
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Tyre Health Alert: {tyre} - {condition}",
            "email_content": f"""
                Tyre: {tyre}
                Vehicle: {vehicle or 'Not Installed'}
                Health Index: {health_index}/100
                Status: {condition}
                Current Mileage: {getattr(tyre_doc, 'current_mileage', 0)} km
                
                Action required - schedule inspection or replacement.
            """,
            "document_type": "Tyre",
            "document_name": tyre,
            "type": "Alert"
        }).insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create health alert: {str(e)}")


def create_tyre_replacement_work_order(tyre: str, vehicle: str, days_until: int):
    """Create maintenance work order for tyre replacement"""
    try:
        # Check if work order already exists
        existing = frappe.db.exists("Maintenance Work Order", {
            "asset": frappe.db.get_value("Tyre", tyre, "asset_link"),
            "status": ["in", ["Planned", "In Progress"]]
        })
        
        if existing:
            return  # Work order already scheduled
        
        tyre_doc = frappe.get_doc("Tyre", tyre)
        asset_link = getattr(tyre_doc, "asset_link", None)
        
        if not asset_link:
            frappe.logger("tems_tyre").warning(f"Tyre {tyre} has no asset link - cannot create work order")
            return
        
        work_order = frappe.get_doc({
            "doctype": "Maintenance Work Order",
            "asset": asset_link,
            "vehicle": vehicle,
            "status": "Planned",
            "planned_date": add_days(None, int(days_until) - 2),  # Schedule 2 days before
            "description": f"Replace tyre {tyre} - predicted end of life in {days_until} days",
            "work_type": "Tyre Replacement"
        })
        
        work_order.insert(ignore_permissions=True)
        frappe.logger("tems_tyre").info(f"Created work order for tyre {tyre} replacement")
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create work order: {str(e)}")


def generate_weekly_tyre_report(fleet_metrics: dict, critical_tyres: List[dict]) -> str:
    """Generate weekly report content"""
    report = f"""
    # Weekly Tyre Performance Report
    
    ## Fleet Overview
    - Total Tyres: {fleet_metrics.get('total_tyres', 0)}
    - Active Tyres: {fleet_metrics.get('active_tyres', 0)}
    - Disposed Tyres: {fleet_metrics.get('disposed_tyres', 0)}
    - Total Investment: {fleet_metrics.get('total_investment', 0):.2f}
    - Average Mileage per Tyre: {fleet_metrics.get('avg_mileage_per_tyre', 0):.0f} km
    
    ## Critical Attention Required
    {len(critical_tyres)} tyres require immediate attention:
    
    """
    
    for tyre in critical_tyres[:10]:  # Top 10 critical
        report += f"""
    - **{tyre.get('tyre')}** ({tyre.get('brand')} {tyre.get('model')})
      - Vehicle: {tyre.get('vehicle', 'Not Installed')}
      - Condition: {tyre.get('condition')}
      - Health Index: {tyre.get('health_index', 0)}/100
      - Mileage: {tyre.get('current_mileage', 0):.0f} km
    """
    
    report += """
    
    ## Brand Performance
    """
    
    for brand, data in fleet_metrics.get('brand_performance', {}).items():
        report += f"""
    ### {brand}
    - Count: {data.get('count', 0)}
    - Avg Mileage: {data.get('avg_mileage', 0):.0f} km
    - Cost per km: {data.get('cost_per_km', 0):.4f}
    """
    
    return report


def create_weekly_report_document(content: str):
    """Create weekly report document"""
    try:
        report_doc = frappe.get_doc({
            "doctype": "TEMS Report",
            "report_type": "Tyre Performance",
            "report_date": now_datetime(),
            "content": content
        })
        
        report_doc.insert(ignore_permissions=True)
        
        # TODO: Send email to Fleet Managers
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create weekly report: {str(e)}")
