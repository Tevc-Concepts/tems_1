import frappe

def execute():
    # Add indexes for Safety Incident and Spot Check
    try:
        frappe.db.add_index("Safety Incident", ["incident_date"], index_name="idx_si_incident_date")
    except Exception:
        pass
    try:
        frappe.db.add_index("Safety Incident", ["status"], index_name="idx_si_status")
    except Exception:
        pass
    try:
        frappe.db.add_index("Spot Check", ["date", "vehicle"], index_name="idx_sc_date_vehicle")
    except Exception:
        pass