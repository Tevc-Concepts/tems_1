import frappe

def execute(filters=None):
    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Link", "options": "Informal Operator Profile"},
        {"label": "Phone", "fieldname": "phone", "fieldtype": "Data"},
        {"label": "USSD ID", "fieldname": "ussd_id", "fieldtype": "Data"}
    ]
    data = frappe.get_all("Informal Operator Profile", fields=["name", "phone", "ussd_id"]) 
    return columns, data
