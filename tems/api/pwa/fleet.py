"""
Fleet PWA API Endpoints
Handles asset tracking, maintenance management, fuel analytics, and lifecycle management
"""

import frappe
from frappe import _
from frappe.utils import nowdate, add_days, flt
import json


@frappe.whitelist()
def get_assets(filters=None):
    """
    Get fleet assets with optional filters
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        elif filters is None:
            filters = {}
        
        conditions = []
        values = {}
        
        if filters.get('status'):
            conditions.append("status = %(status)s")
            values['status'] = filters['status']
        
        if filters.get('category'):
            conditions.append("asset_category = %(category)s")
            values['category'] = filters['category']
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        assets = frappe.db.sql(f"""
            SELECT 
                name,
                asset_name,
                asset_category,
                status,
                purchase_date,
                gross_purchase_amount,
                current_value,
                location,
                custodian
            FROM `tabAsset`
            {where_clause}
            ORDER BY asset_name
            LIMIT 100
        """, values, as_dict=True)
        
        return {
            "success": True,
            "data": assets,
            "count": len(assets)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching assets: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_asset_details(asset_id):
    """
    Get detailed asset information
    """
    try:
        if not asset_id:
            frappe.throw(_("Asset ID is required"))
        
        if not frappe.has_permission("Asset", "read", asset_id):
            frappe.throw(_("Insufficient permissions"), frappe.PermissionError)
        
        asset = frappe.get_doc("Asset", asset_id)
        
        # Get maintenance history
        maintenance_history = frappe.get_all(
            "Maintenance Work Order",
            fields=["name", "maintenance_date", "maintenance_type", "status", "cost"],
            filters={"asset": asset_id},
            order_by="maintenance_date DESC",
            limit=20
        )
        
        # Get depreciation schedule
        depreciation = frappe.get_all(
            "Asset Depreciation Schedule",
            fields=["schedule_date", "depreciation_amount", "accumulated_depreciation_amount"],
            filters={"parent": asset_id},
            order_by="schedule_date DESC"
        )
        
        return {
            "success": True,
            "data": {
                "asset": asset.as_dict(),
                "maintenance_history": maintenance_history,
                "depreciation_schedule": depreciation
            }
        }
        
    except frappe.PermissionError:
        return {"success": False, "message": _("Insufficient permissions")}
    except Exception as e:
        frappe.log_error(f"Error fetching asset details: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_asset_status(asset_id, status, notes=''):
    """
    Update asset status
    """
    try:
        if not asset_id or not status:
            frappe.throw(_("Asset ID and status are required"))
        
        if not frappe.has_permission("Asset", "write", asset_id):
            frappe.throw(_("Insufficient permissions"), frappe.PermissionError)
        
        asset = frappe.get_doc("Asset", asset_id)
        old_status = asset.status
        asset.status = status
        
        if notes:
            asset.add_comment("Comment", f"Status changed from {old_status} to {status}: {notes}")
        
        asset.save()
        
        return {
            "success": True,
            "message": _("Asset status updated"),
            "data": {
                "asset": asset_id,
                "old_status": old_status,
                "new_status": status
            }
        }
        
    except frappe.PermissionError:
        return {"success": False, "message": _("Insufficient permissions")}
    except Exception as e:
        frappe.log_error(f"Error updating asset status: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_asset_categories():
    """
    Get asset categories
    """
    try:
        categories = frappe.get_all(
            "Asset Category",
            fields=["name", "enable_cwip_accounting"],
            order_by="name"
        )
        
        return {
            "success": True,
            "data": categories,
            "count": len(categories)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching asset categories: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_work_orders(filters=None):
    """
    Get maintenance work orders
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        
        work_orders = frappe.get_all(
            "Maintenance Work Order",
            fields=["name", "asset", "maintenance_date", "maintenance_type", "status", "cost", "is_overdue"],
            filters=filters or {},
            order_by="maintenance_date DESC",
            limit=100
        )
        
        return {
            "success": True,
            "data": work_orders,
            "count": len(work_orders)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching work orders: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_upcoming_maintenance(days=30):
    """
    Get upcoming maintenance schedule
    """
    try:
        end_date = add_days(nowdate(), days)
        
        upcoming = frappe.db.sql("""
            SELECT 
                name,
                asset,
                maintenance_date,
                maintenance_type,
                status,
                estimated_cost,
                DATEDIFF(maintenance_date, CURDATE()) as days_until
            FROM `tabMaintenance Work Order`
            WHERE maintenance_date BETWEEN CURDATE() AND %(end_date)s
            AND status IN ('Scheduled', 'Pending')
            ORDER BY maintenance_date ASC
        """, {"end_date": end_date}, as_dict=True)
        
        return {
            "success": True,
            "data": upcoming,
            "count": len(upcoming)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching upcoming maintenance: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def create_work_order(work_order_data):
    """
    Create new maintenance work order
    """
    try:
        if isinstance(work_order_data, str):
            work_order_data = json.loads(work_order_data)
        
        # Validate required fields
        required = ['asset', 'maintenance_date', 'maintenance_type']
        for field in required:
            if not work_order_data.get(field):
                frappe.throw(_(f"{field} is required"))
        
        # Create work order
        wo = frappe.get_doc({
            "doctype": "Maintenance Work Order",
            "asset": work_order_data['asset'],
            "maintenance_date": work_order_data['maintenance_date'],
            "maintenance_type": work_order_data['maintenance_type'],
            "description": work_order_data.get('description', ''),
            "estimated_cost": work_order_data.get('estimated_cost', 0),
            "status": "Scheduled"
        })
        
        wo.insert()
        
        return {
            "success": True,
            "message": _("Work order created successfully"),
            "data": wo.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating work order: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_work_order_status(work_order_id, status):
    """
    Update work order status
    """
    try:
        if not work_order_id or not status:
            frappe.throw(_("Work order ID and status are required"))
        
        wo = frappe.get_doc("Maintenance Work Order", work_order_id)
        wo.status = status
        
        if status == "Completed":
            wo.completion_date = nowdate()
        
        wo.save()
        
        return {
            "success": True,
            "message": _("Work order status updated"),
            "data": wo.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error updating work order status: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def schedule_preventive_maintenance(asset_id, scheduled_date, maintenance_type):
    """
    Schedule preventive maintenance
    """
    try:
        if not asset_id or not scheduled_date or not maintenance_type:
            frappe.throw(_("Asset ID, scheduled date, and maintenance type are required"))
        
        # Create preventive maintenance work order
        wo = frappe.get_doc({
            "doctype": "Maintenance Work Order",
            "asset": asset_id,
            "maintenance_date": scheduled_date,
            "maintenance_type": maintenance_type,
            "description": f"Scheduled preventive maintenance - {maintenance_type}",
            "status": "Scheduled",
            "is_preventive": 1
        })
        
        wo.insert()
        
        return {
            "success": True,
            "message": _("Preventive maintenance scheduled"),
            "data": wo.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error scheduling preventive maintenance: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_fuel_logs(filters=None):
    """
    Get fuel consumption logs
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        
        fuel_logs = frappe.get_all(
            "Fuel Log Entry",
            fields=["name", "vehicle", "date", "quantity", "cost", "odometer", "fuel_type"],
            filters=filters or {},
            order_by="date DESC",
            limit=100
        )
        
        return {
            "success": True,
            "data": fuel_logs,
            "count": len(fuel_logs)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching fuel logs: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_fuel_stats(period='month'):
    """
    Get fuel statistics by period
    """
    try:
        # Calculate date range based on period
        if period == 'week':
            from_date = add_days(nowdate(), -7)
        elif period == 'month':
            from_date = add_days(nowdate(), -30)
        else:
            from_date = add_days(nowdate(), -365)
        
        stats = frappe.db.sql("""
            SELECT 
                COUNT(*) as total_entries,
                SUM(quantity) as total_fuel,
                SUM(cost) as total_cost,
                AVG(quantity) as avg_quantity,
                AVG(cost) as avg_cost
            FROM `tabFuel Log Entry`
            WHERE date >= %(from_date)s
        """, {"from_date": from_date}, as_dict=True)
        
        # Calculate efficiency if odometer data available
        efficiency = frappe.db.sql("""
            SELECT 
                AVG((odometer_end - odometer_start) / NULLIF(quantity, 0)) as avg_efficiency
            FROM `tabFuel Log Entry`
            WHERE date >= %(from_date)s
            AND odometer_start IS NOT NULL
            AND odometer_end IS NOT NULL
            AND quantity > 0
        """, {"from_date": from_date}, as_dict=True)
        
        result = stats[0] if stats else {}
        result['average_efficiency'] = efficiency[0].get('avg_efficiency', 0) if efficiency else 0
        result['period'] = period
        
        return {
            "success": True,
            "data": result
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching fuel stats: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def log_fuel_entry(fuel_data):
    """
    Log new fuel entry
    """
    try:
        if isinstance(fuel_data, str):
            fuel_data = json.loads(fuel_data)
        
        # Validate required fields
        required = ['vehicle', 'date', 'quantity', 'cost']
        for field in required:
            if not fuel_data.get(field):
                frappe.throw(_(f"{field} is required"))
        
        # Create fuel log entry
        fuel_log = frappe.get_doc({
            "doctype": "Fuel Log Entry",
            "vehicle": fuel_data['vehicle'],
            "date": fuel_data['date'],
            "quantity": fuel_data['quantity'],
            "cost": fuel_data['cost'],
            "odometer": fuel_data.get('odometer'),
            "fuel_type": fuel_data.get('fuel_type', 'Diesel'),
            "station": fuel_data.get('station', '')
        })
        
        fuel_log.insert()
        
        return {
            "success": True,
            "message": _("Fuel entry logged successfully"),
            "data": fuel_log.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error logging fuel entry: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_fuel_trends(asset_id, period='month'):
    """
    Get fuel consumption trends for specific asset
    """
    try:
        if not asset_id:
            frappe.throw(_("Asset ID is required"))
        
        if period == 'week':
            from_date = add_days(nowdate(), -7)
        elif period == 'month':
            from_date = add_days(nowdate(), -30)
        else:
            from_date = add_days(nowdate(), -365)
        
        trends = frappe.db.sql("""
            SELECT 
                DATE(date) as log_date,
                SUM(quantity) as total_quantity,
                SUM(cost) as total_cost,
                AVG(quantity) as avg_quantity
            FROM `tabFuel Log Entry`
            WHERE vehicle = %(vehicle)s
            AND date >= %(from_date)s
            GROUP BY DATE(date)
            ORDER BY date ASC
        """, {"vehicle": asset_id, "from_date": from_date}, as_dict=True)
        
        return {
            "success": True,
            "data": trends,
            "count": len(trends),
            "period": period
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching fuel trends: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_lifecycle_data(filters=None):
    """
    Get asset lifecycle data
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        
        # Get assets with depreciation data
        assets = frappe.db.sql("""
            SELECT 
                a.name,
                a.asset_name,
                a.purchase_date,
                a.gross_purchase_amount,
                a.current_value,
                a.status,
                DATEDIFF(CURDATE(), a.purchase_date) as age_days,
                ((a.gross_purchase_amount - a.current_value) / NULLIF(a.gross_purchase_amount, 0) * 100) as depreciation_percent,
                CASE 
                    WHEN ((a.gross_purchase_amount - a.current_value) / NULLIF(a.gross_purchase_amount, 0) * 100) > 80 THEN 'Low'
                    ELSE 'Medium'
                END as remaining_life_percent
            FROM `tabAsset` a
            WHERE a.docstatus = 1
            ORDER BY a.purchase_date DESC
        """, as_dict=True)
        
        return {
            "success": True,
            "data": assets,
            "count": len(assets)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching lifecycle data: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_asset_lifecycle(asset_id):
    """
    Get specific asset lifecycle details
    """
    try:
        if not asset_id:
            frappe.throw(_("Asset ID is required"))
        
        asset = frappe.get_doc("Asset", asset_id)
        
        # Calculate lifecycle metrics
        age_days = (nowdate() - asset.purchase_date).days if asset.purchase_date else 0
        depreciation_amount = flt(asset.gross_purchase_amount) - flt(asset.current_value)
        depreciation_percent = (depreciation_amount / flt(asset.gross_purchase_amount) * 100) if flt(asset.gross_purchase_amount) > 0 else 0
        
        return {
            "success": True,
            "data": {
                "asset": asset_id,
                "asset_name": asset.asset_name,
                "purchase_date": asset.purchase_date,
                "age_days": age_days,
                "original_value": flt(asset.gross_purchase_amount),
                "current_value": flt(asset.current_value),
                "depreciation_amount": depreciation_amount,
                "depreciation_percent": depreciation_percent,
                "status": asset.status
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching asset lifecycle: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def calculate_depreciation(asset_id):
    """
    Calculate asset depreciation
    """
    try:
        if not asset_id:
            frappe.throw(_("Asset ID is required"))
        
        asset = frappe.get_doc("Asset", asset_id)
        
        # Trigger depreciation calculation
        # This would typically call Frappe's built-in depreciation methods
        depreciation_schedule = frappe.get_all(
            "Asset Depreciation Schedule",
            fields=["schedule_date", "depreciation_amount", "accumulated_depreciation_amount"],
            filters={"parent": asset_id},
            order_by="idx"
        )
        
        return {
            "success": True,
            "message": _("Depreciation calculated"),
            "data": {
                "asset": asset_id,
                "schedule": depreciation_schedule
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error calculating depreciation: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_lifecycle_milestone(asset_id, milestone, status):
    """
    Update asset lifecycle milestone
    """
    try:
        if not asset_id or not milestone or not status:
            frappe.throw(_("Asset ID, milestone, and status are required"))
        
        # Add milestone comment to asset
        asset = frappe.get_doc("Asset", asset_id)
        asset.add_comment("Comment", f"Lifecycle milestone '{milestone}' - Status: {status}")
        
        return {
            "success": True,
            "message": _("Lifecycle milestone updated"),
            "data": {
                "asset": asset_id,
                "milestone": milestone,
                "status": status
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error updating lifecycle milestone: {str(e)}", "Fleet API")
        return {"success": False, "message": str(e)}
