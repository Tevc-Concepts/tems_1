"""
Tyre Management API Endpoints
REST APIs for tyre registration, updates, and sensor data ingestion
"""
from __future__ import annotations

import frappe
from frappe import _
from frappe.utils import now_datetime, cint, flt
from typing import Dict, Optional
import json


@frappe.whitelist(allow_guest=False)
def register_tyre(
    brand: str,
    model: str,
    size: str,
    tyre_type: str,
    cost: float,
    asset_link: str = None,
    vehicle: str = None,
    **kwargs
) -> Dict:
    """
    Register a new tyre in the system
    
    Args:
        brand: Tyre manufacturer
        model: Tyre model
        size: Tyre size (e.g., 315/80R22.5)
        tyre_type: Steer / Drive / Trailer / Spare
        cost: Purchase cost
        asset_link: Optional link to ERPNext Asset
        vehicle: Optional vehicle assignment
        
    Returns:
        Dict with tyre details
    """
    try:
        # Create tyre document
        tyre_doc = frappe.get_doc({
            "doctype": "Tyre",
            "brand": brand,
            "model": model,
            "size": size,
            "tyre_type": tyre_type,
            "cost": flt(cost),
            "asset_link": asset_link,
            "vehicle": vehicle,
            "status": "In Stock",
            "purchase_date": frappe.utils.today(),
            "current_mileage": 0,
            "initial_tread_depth": kwargs.get("initial_tread_depth", 16.0),
            "last_tread_depth_mm": kwargs.get("initial_tread_depth", 16.0)
        })
        
        tyre_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "tyre_id": tyre_doc.name,
            "message": f"Tyre {tyre_doc.name} registered successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Tyre registration failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def update_tyre_status(tyre: str, status: str, **kwargs) -> Dict:
    """
    Update tyre status
    
    Args:
        tyre: Tyre document name
        status: New status (In Stock / Installed / In Repair / Retread / Disposed)
        
    Returns:
        Dict with update confirmation
    """
    try:
        if not frappe.db.exists("Tyre", tyre):
            return {
                "success": False,
                "error": f"Tyre {tyre} not found"
            }
        
        tyre_doc = frappe.get_doc("Tyre", tyre)
        tyre_doc.status = status
        
        # Update additional fields if provided
        if kwargs.get("vehicle"):
            tyre_doc.vehicle = kwargs["vehicle"]
        
        if kwargs.get("mileage"):
            tyre_doc.current_mileage = flt(kwargs["mileage"])
        
        tyre_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "tyre": tyre,
            "status": status,
            "message": f"Tyre {tyre} status updated to {status}"
        }
        
    except Exception as e:
        frappe.log_error(f"Tyre status update failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def install_tyre(
    tyre: str,
    vehicle: str,
    position: str,
    installation_date: str = None,
    remarks: str = None
) -> Dict:
    """
    Record tyre installation on a vehicle
    
    Args:
        tyre: Tyre document name
        vehicle: Vehicle document name
        position: Tyre position (e.g., "Front Left", "Rear Right 1")
        installation_date: Optional installation date (defaults to now)
        remarks: Optional notes
        
    Returns:
        Dict with installation confirmation
    """
    try:
        # Validate tyre and vehicle exist
        if not frappe.db.exists("Tyre", tyre):
            return {"success": False, "error": f"Tyre {tyre} not found"}
        
        if not frappe.db.exists("Vehicle", vehicle):
            return {"success": False, "error": f"Vehicle {vehicle} not found"}
        
        # Create installation log
        install_doc = frappe.get_doc({
            "doctype": "Tyre Installation Log",
            "tyre": tyre,
            "vehicle": vehicle,
            "position": position,
            "installation_date": installation_date or now_datetime(),
            "remarks": remarks
        })
        
        install_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "installation_log": install_doc.name,
            "message": f"Tyre {tyre} installed on {vehicle} at position {position}"
        }
        
    except Exception as e:
        frappe.log_error(f"Tyre installation failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def remove_tyre(
    installation_log: str,
    removed_date: str = None,
    remarks: str = None
) -> Dict:
    """
    Record tyre removal from vehicle
    
    Args:
        installation_log: Tyre Installation Log document name
        removed_date: Optional removal date (defaults to now)
        remarks: Optional notes
        
    Returns:
        Dict with removal confirmation
    """
    try:
        if not frappe.db.exists("Tyre Installation Log", installation_log):
            return {"success": False, "error": f"Installation log {installation_log} not found"}
        
        install_doc = frappe.get_doc("Tyre Installation Log", installation_log)
        install_doc.removed_date = removed_date or now_datetime()
        if remarks:
            install_doc.remarks = (install_doc.remarks or "") + "\n" + remarks
        
        install_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "message": f"Tyre {install_doc.tyre} removed from {install_doc.vehicle}"
        }
        
    except Exception as e:
        frappe.log_error(f"Tyre removal failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def record_inspection(
    tyre: str,
    inspector: str,
    pressure_psi: float = None,
    tread_depth_mm: float = None,
    observations: str = None,
    inspection_date: str = None
) -> Dict:
    """
    Record tyre inspection
    
    Args:
        tyre: Tyre document name
        inspector: Employee conducting inspection
        pressure_psi: Tyre pressure in PSI
        tread_depth_mm: Tread depth in millimeters
        observations: Inspection notes
        inspection_date: Optional date (defaults to now)
        
    Returns:
        Dict with inspection details and AI classification
    """
    try:
        if not frappe.db.exists("Tyre", tyre):
            return {"success": False, "error": f"Tyre {tyre} not found"}
        
        # Create inspection log
        inspection_doc = frappe.get_doc({
            "doctype": "Tyre Inspection Log",
            "tyre": tyre,
            "inspector": inspector,
            "pressure_psi": flt(pressure_psi) if pressure_psi else None,
            "tread_depth_mm": flt(tread_depth_mm) if tread_depth_mm else None,
            "observations": observations,
            "inspection_date": inspection_date or now_datetime()
        })
        
        # Run AI classification if tread depth provided
        if tread_depth_mm:
            from tems.tems_tyre.utils.tyre_analyzer import calculate_health_index, classify_tyre_condition
            
            # Update tyre with tread depth first
            tyre_doc = frappe.get_doc("Tyre", tyre)
            tyre_doc.last_tread_depth_mm = flt(tread_depth_mm)
            tyre_doc.save(ignore_permissions=True)
            
            # Calculate health and classify
            health_index = calculate_health_index(tyre)
            condition = classify_tyre_condition(health_index)
            
            inspection_doc.ai_condition_classification = condition
            inspection_doc.ai_health_index = health_index
        
        inspection_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "inspection_log": inspection_doc.name,
            "ai_condition": getattr(inspection_doc, "ai_condition_classification", None),
            "ai_health_index": getattr(inspection_doc, "ai_health_index", None),
            "message": "Inspection recorded successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Tyre inspection recording failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=True, methods=["POST"])
def ingest_sensor_data(
    sensor_id: str,
    tyre: str = None,
    pressure_psi: float = None,
    temperature_c: float = None,
    speed_kmh: float = None,
    timestamp: str = None
) -> Dict:
    """
    Ingest IoT sensor data from tyre pressure monitoring systems (TPMS)
    Allows guest access for IoT devices with API key authentication
    
    Args:
        sensor_id: Unique sensor identifier
        tyre: Optional tyre document name (can be looked up from sensor_id)
        pressure_psi: Tyre pressure in PSI
        temperature_c: Temperature in Celsius
        speed_kmh: Vehicle speed in km/h
        timestamp: Optional timestamp (defaults to now)
        
    Returns:
        Dict with ingestion confirmation and any alerts
    """
    try:
        # Validate API key for guest access
        api_key = frappe.get_request_header("X-API-Key")
        if frappe.session.user == "Guest":
            if not api_key or not validate_sensor_api_key(api_key):
                return {
                    "success": False,
                    "error": "Unauthorized - Invalid API key"
                }
        
        # Look up tyre from sensor_id if not provided
        if not tyre:
            tyre = frappe.db.get_value("Tyre", {"pressure_sensor_id": sensor_id}, "name")
            
            if not tyre:
                # Log orphaned sensor data
                frappe.log_error(f"Sensor {sensor_id} not linked to any tyre")
                return {
                    "success": False,
                    "error": f"Sensor {sensor_id} not registered"
                }
        
        # Create sensor data record
        sensor_doc = frappe.get_doc({
            "doctype": "Tyre Sensor Data",
            "sensor_id": sensor_id,
            "tyre": tyre,
            "pressure_psi": flt(pressure_psi) if pressure_psi else None,
            "temperature_c": flt(temperature_c) if temperature_c else None,
            "speed_kmh": flt(speed_kmh) if speed_kmh else None,
            "timestamp": timestamp or now_datetime()
        })
        
        # Run anomaly detection
        from tems.tems_tyre.utils.tyre_analyzer import detect_pressure_anomaly
        
        anomaly_result = detect_pressure_anomaly({
            "tyre": tyre,
            "pressure_psi": pressure_psi,
            "temperature_c": temperature_c
        })
        
        if anomaly_result["severity"] in ["Critical", "Warning"]:
            sensor_doc.alert_generated = 1
            sensor_doc.ai_status_flag = anomaly_result["severity"]
            
            # Create alert notification
            create_sensor_alert(tyre, anomaly_result)
        else:
            sensor_doc.alert_generated = 0
            sensor_doc.ai_status_flag = "Normal"
        
        sensor_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "success": True,
            "sensor_data_id": sensor_doc.name,
            "anomaly_detected": anomaly_result["severity"] != "Normal",
            "severity": anomaly_result["severity"],
            "anomalies": anomaly_result.get("anomalies", []),
            "message": "Sensor data ingested successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Sensor data ingestion failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def get_tyre_health(tyre: str) -> Dict:
    """
    Get comprehensive health report for a tyre
    
    Args:
        tyre: Tyre document name
        
    Returns:
        Dict with health metrics and insights
    """
    try:
        if not frappe.db.exists("Tyre", tyre):
            return {"success": False, "error": f"Tyre {tyre} not found"}
        
        from tems.tems_tyre.utils.tyre_analyzer import generate_tyre_insights
        
        insights = generate_tyre_insights(tyre)
        
        return {
            "success": True,
            "insights": insights
        }
        
    except Exception as e:
        frappe.log_error(f"Tyre health retrieval failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def get_vehicle_tyre_status(vehicle: str) -> Dict:
    """
    Get status of all tyres on a vehicle
    
    Args:
        vehicle: Vehicle document name
        
    Returns:
        Dict with tyre positions and health status
    """
    try:
        if not frappe.db.exists("Vehicle", vehicle):
            return {"success": False, "error": f"Vehicle {vehicle} not found"}
        
        # Get all installed tyres for this vehicle
        installations = frappe.get_all(
            "Tyre Installation Log",
            filters={
                "vehicle": vehicle,
                "removed_date": ["is", "not set"]
            },
            fields=["tyre", "position", "installation_date"]
        )
        
        tyre_status = []
        
        for install in installations:
            tyre_doc = frappe.get_doc("Tyre", install["tyre"])
            
            from tems.tems_tyre.utils.tyre_analyzer import calculate_health_index, classify_tyre_condition
            
            health_index = calculate_health_index(install["tyre"])
            condition = classify_tyre_condition(health_index)
            
            tyre_status.append({
                "tyre": install["tyre"],
                "position": install["position"],
                "installation_date": install["installation_date"],
                "health_index": health_index,
                "condition": condition,
                "brand": getattr(tyre_doc, "brand", ""),
                "model": getattr(tyre_doc, "model", ""),
                "mileage": getattr(tyre_doc, "current_mileage", 0),
                "last_pressure_psi": getattr(tyre_doc, "last_pressure_psi", None),
                "last_tread_depth_mm": getattr(tyre_doc, "last_tread_depth_mm", None)
            })
        
        return {
            "success": True,
            "vehicle": vehicle,
            "tyre_count": len(tyre_status),
            "tyres": tyre_status
        }
        
    except Exception as e:
        frappe.log_error(f"Vehicle tyre status retrieval failed: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def validate_sensor_api_key(api_key: str) -> bool:
    """
    Validate API key for sensor data ingestion
    Checks against TEMS Settings or API Key doctype
    """
    # Check if API key exists and is valid
    key_doc = frappe.db.exists("API Key", {
        "api_key": api_key,
        "enabled": 1
    })
    
    return bool(key_doc)


def create_sensor_alert(tyre: str, anomaly_result: Dict):
    """
    Create alert notification for sensor anomaly
    """
    try:
        severity = anomaly_result.get("severity", "Warning")
        anomalies = ", ".join(anomaly_result.get("anomalies", []))
        
        # Get vehicle for context
        vehicle = frappe.db.get_value("Tyre", tyre, "vehicle")
        
        alert_doc = frappe.get_doc({
            "doctype": "Notification Log",
            "subject": f"Tyre Sensor Alert: {tyre} - {severity}",
            "email_content": f"""
                Tyre: {tyre}
                Vehicle: {vehicle or 'Not Installed'}
                Severity: {severity}
                Issues: {anomalies}
                Pressure: {anomaly_result.get('pressure_psi')} PSI
                Temperature: {anomaly_result.get('temperature_c')} °C
            """,
            "document_type": "Tyre",
            "document_name": tyre,
            "type": "Alert"
        })
        
        alert_doc.insert(ignore_permissions=True)
        
    except Exception as e:
        frappe.logger("tems_tyre").error(f"Failed to create sensor alert: {str(e)}")
