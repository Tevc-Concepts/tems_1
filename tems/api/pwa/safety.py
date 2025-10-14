"""
Safety PWA API Endpoints
Handles incident management, safety audits, compliance tracking, and risk assessment
"""

import frappe
from frappe import _
from frappe.utils import nowdate, add_days, get_datetime
import json


@frappe.whitelist()
def get_incidents(filters=None):
    """
    Get safety incidents with optional filters
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
        
        if filters.get('severity'):
            conditions.append("severity = %(severity)s")
            values['severity'] = filters['severity']
        
        if filters.get('from_date'):
            conditions.append("incident_date >= %(from_date)s")
            values['from_date'] = filters['from_date']
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        incidents = frappe.db.sql(f"""
            SELECT 
                name,
                incident_date,
                incident_type,
                severity,
                status,
                location,
                vehicle,
                driver,
                description,
                investigation_status,
                created_by,
                creation
            FROM `tabIncident Report`
            {where_clause}
            ORDER BY incident_date DESC, creation DESC
            LIMIT 100
        """, values, as_dict=True)
        
        return {
            "success": True,
            "data": incidents,
            "count": len(incidents)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching incidents: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def report_incident(incident_data):
    """
    Report new safety incident
    """
    try:
        if isinstance(incident_data, str):
            incident_data = json.loads(incident_data)
        
        # Validate required fields
        required = ['incident_date', 'incident_type', 'severity', 'description']
        for field in required:
            if not incident_data.get(field):
                frappe.throw(_(f"{field} is required"))
        
        # Create incident report
        incident = frappe.get_doc({
            "doctype": "Incident Report",
            "incident_date": incident_data['incident_date'],
            "incident_type": incident_data['incident_type'],
            "severity": incident_data['severity'],
            "description": incident_data['description'],
            "location": incident_data.get('location'),
            "vehicle": incident_data.get('vehicle'),
            "driver": incident_data.get('driver'),
            "status": "Open",
            "investigation_status": "Pending"
        })
        
        incident.insert()
        
        # Notify safety team for critical incidents
        if incident.severity in ["Critical", "High"]:
            frappe.publish_realtime(
                "safety_incident_alert",
                {"incident": incident.name, "severity": incident.severity},
                user="safety_team"
            )
        
        return {
            "success": True,
            "message": _("Incident reported successfully"),
            "data": incident.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error reporting incident: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_incident_status(incident_id, status):
    """
    Update incident status
    """
    try:
        if not incident_id or not status:
            frappe.throw(_("Incident ID and status are required"))
        
        if not frappe.has_permission("Incident Report", "write", incident_id):
            frappe.throw(_("Insufficient permissions"), frappe.PermissionError)
        
        incident = frappe.get_doc("Incident Report", incident_id)
        incident.status = status
        
        if status == "Closed":
            incident.closure_date = nowdate()
        
        incident.save()
        
        return {
            "success": True,
            "message": _("Incident status updated"),
            "data": incident.as_dict()
        }
        
    except frappe.PermissionError:
        return {"success": False, "message": _("Insufficient permissions")}
    except Exception as e:
        frappe.log_error(f"Error updating incident status: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def assign_investigator(incident_id, investigator_id):
    """
    Assign investigator to incident
    """
    try:
        if not incident_id or not investigator_id:
            frappe.throw(_("Incident ID and Investigator ID are required"))
        
        incident = frappe.get_doc("Incident Report", incident_id)
        incident.investigator = investigator_id
        incident.investigation_status = "In Progress"
        incident.save()
        
        return {
            "success": True,
            "message": _("Investigator assigned successfully"),
            "data": {
                "incident": incident_id,
                "investigator": investigator_id
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error assigning investigator: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_audits(filters=None):
    """
    Get safety audits
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        
        audits = frappe.get_all(
            "Safety Audit",
            fields=["name", "audit_date", "audit_type", "status", "auditor", "vehicle", "location", "score"],
            filters=filters or {},
            order_by="audit_date DESC",
            limit=100
        )
        
        return {
            "success": True,
            "data": audits,
            "count": len(audits)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching audits: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def schedule_audit(audit_data):
    """
    Schedule new safety audit
    """
    try:
        if isinstance(audit_data, str):
            audit_data = json.loads(audit_data)
        
        # Validate required fields
        required = ['audit_date', 'audit_type', 'auditor']
        for field in required:
            if not audit_data.get(field):
                frappe.throw(_(f"{field} is required"))
        
        # Create audit
        audit = frappe.get_doc({
            "doctype": "Safety Audit",
            "audit_date": audit_data['audit_date'],
            "audit_type": audit_data['audit_type'],
            "auditor": audit_data['auditor'],
            "vehicle": audit_data.get('vehicle'),
            "location": audit_data.get('location'),
            "status": "Scheduled"
        })
        
        audit.insert()
        
        return {
            "success": True,
            "message": _("Audit scheduled successfully"),
            "data": audit.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error scheduling audit: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def submit_audit_findings(audit_id, findings):
    """
    Submit audit findings
    """
    try:
        if not audit_id:
            frappe.throw(_("Audit ID is required"))
        
        if isinstance(findings, str):
            findings = json.loads(findings)
        
        audit = frappe.get_doc("Safety Audit", audit_id)
        audit.findings = findings.get('findings', '')
        audit.score = findings.get('score', 0)
        audit.recommendations = findings.get('recommendations', '')
        audit.status = "Completed"
        audit.completion_date = nowdate()
        
        audit.save()
        
        return {
            "success": True,
            "message": _("Audit findings submitted"),
            "data": audit.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error submitting audit findings: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_compliance_items(filters=None):
    """
    Get compliance tracking items
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        
        compliance_items = frappe.get_all(
            "Compliance Document",
            fields=["name", "document_type", "vehicle", "driver", "issue_date", "expiry_date", "status"],
            filters=filters or {},
            order_by="expiry_date ASC"
        )
        
        return {
            "success": True,
            "data": compliance_items,
            "count": len(compliance_items)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching compliance items: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_compliance_status(compliance_id, status):
    """
    Update compliance item status
    """
    try:
        if not compliance_id or not status:
            frappe.throw(_("Compliance ID and status are required"))
        
        compliance = frappe.get_doc("Compliance Document", compliance_id)
        compliance.status = status
        compliance.save()
        
        return {
            "success": True,
            "message": _("Compliance status updated"),
            "data": compliance.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error updating compliance status: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def renew_compliance(compliance_id, renewal_data):
    """
    Renew compliance certification
    """
    try:
        if not compliance_id:
            frappe.throw(_("Compliance ID is required"))
        
        if isinstance(renewal_data, str):
            renewal_data = json.loads(renewal_data)
        
        compliance = frappe.get_doc("Compliance Document", compliance_id)
        compliance.issue_date = renewal_data.get('issue_date', nowdate())
        compliance.expiry_date = renewal_data.get('expiry_date')
        compliance.status = "Active"
        compliance.save()
        
        return {
            "success": True,
            "message": _("Compliance renewed successfully"),
            "data": compliance.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error renewing compliance: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_risk_assessments(filters=None):
    """
    Get risk assessments
    """
    try:
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}
        
        assessments = frappe.get_all(
            "Risk Assessment",
            fields=["name", "assessment_date", "risk_type", "risk_level", "status", "vehicle", "route"],
            filters=filters or {},
            order_by="assessment_date DESC"
        )
        
        return {
            "success": True,
            "data": assessments,
            "count": len(assessments)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching risk assessments: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def create_risk_assessment(assessment_data):
    """
    Create new risk assessment
    """
    try:
        if isinstance(assessment_data, str):
            assessment_data = json.loads(assessment_data)
        
        # Validate required fields
        required = ['risk_type', 'risk_level', 'description']
        for field in required:
            if not assessment_data.get(field):
                frappe.throw(_(f"{field} is required"))
        
        # Create assessment
        assessment = frappe.get_doc({
            "doctype": "Risk Assessment",
            "assessment_date": nowdate(),
            "risk_type": assessment_data['risk_type'],
            "risk_level": assessment_data['risk_level'],
            "description": assessment_data['description'],
            "vehicle": assessment_data.get('vehicle'),
            "route": assessment_data.get('route'),
            "status": "Open"
        })
        
        assessment.insert()
        
        return {
            "success": True,
            "message": _("Risk assessment created"),
            "data": assessment.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating risk assessment: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def update_mitigation_plan(assessment_id, plan_data):
    """
    Update risk mitigation plan
    """
    try:
        if not assessment_id:
            frappe.throw(_("Assessment ID is required"))
        
        if isinstance(plan_data, str):
            plan_data = json.loads(plan_data)
        
        assessment = frappe.get_doc("Risk Assessment", assessment_id)
        assessment.mitigation_plan = plan_data.get('mitigation_plan', '')
        assessment.mitigation_status = plan_data.get('status', 'Planned')
        assessment.save()
        
        return {
            "success": True,
            "message": _("Mitigation plan updated"),
            "data": assessment.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error updating mitigation plan: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_safety_statistics():
    """
    Get safety statistics for dashboard
    """
    try:
        stats = frappe._dict()
        
        # Total incidents
        stats.total_incidents = frappe.db.count("Incident Report")
        
        # Open incidents
        stats.open_incidents = frappe.db.count("Incident Report", {"status": "Open"})
        
        # Critical incidents
        stats.critical_incidents = frappe.db.count("Incident Report", {"severity": "Critical"})
        
        # Compliance rate
        total_compliance = frappe.db.count("Compliance Document")
        active_compliance = frappe.db.count("Compliance Document", {"status": "Active"})
        stats.compliance_rate = round((active_compliance / total_compliance * 100), 1) if total_compliance > 0 else 100
        
        # Pending audits
        stats.pending_audits = frappe.db.count("Safety Audit", {"status": ["in", ["Scheduled", "In Progress"]]})
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching safety statistics: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_expiring_compliance(days=30):
    """
    Get compliance items expiring soon
    """
    try:
        expiry_date = add_days(nowdate(), days)
        
        expiring = frappe.db.sql("""
            SELECT 
                name,
                document_type,
                vehicle,
                driver,
                expiry_date,
                DATEDIFF(expiry_date, CURDATE()) as days_to_expiry
            FROM `tabCompliance Document`
            WHERE status = 'Active'
            AND expiry_date <= %(expiry_date)s
            AND expiry_date >= CURDATE()
            ORDER BY expiry_date ASC
        """, {"expiry_date": expiry_date}, as_dict=True)
        
        return {
            "success": True,
            "data": expiring,
            "count": len(expiring)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching expiring compliance: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def get_critical_incidents():
    """
    Get critical/high-severity incidents
    """
    try:
        critical = frappe.db.sql("""
            SELECT 
                name,
                incident_date,
                incident_type,
                severity,
                status,
                description,
                vehicle,
                driver
            FROM `tabIncident Report`
            WHERE severity IN ('Critical', 'High')
            AND status != 'Closed'
            ORDER BY incident_date DESC
            LIMIT 20
        """, as_dict=True)
        
        return {
            "success": True,
            "data": critical,
            "count": len(critical)
        }
        
    except Exception as e:
        frappe.log_error(f"Error fetching critical incidents: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}


@frappe.whitelist()
def calculate_compliance_rate():
    """
    Calculate overall compliance rate
    """
    try:
        total = frappe.db.count("Compliance Document")
        active = frappe.db.count("Compliance Document", {"status": "Active"})
        
        rate = round((active / total * 100), 2) if total > 0 else 100
        
        return {
            "success": True,
            "data": {
                "total": total,
                "active": active,
                "rate": rate
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error calculating compliance rate: {str(e)}", "Safety API")
        return {"success": False, "message": str(e)}
