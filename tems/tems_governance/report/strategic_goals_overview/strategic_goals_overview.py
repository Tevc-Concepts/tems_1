import frappe


def execute(filters=None):
    columns = [
        {"label": "Code", "fieldname": "code", "fieldtype": "Data", "width": 120},
        {"label": "Title", "fieldname": "title", "fieldtype": "Data", "width": 250},
        {"label": "Language", "fieldname": "language", "fieldtype": "Data", "width": 90},
        {"label": "Owner", "fieldname": "owner_employee", "fieldtype": "Link", "options": "Employee", "width": 160},
        {"label": "Effective From", "fieldname": "effective_from", "fieldtype": "Date", "width": 110},
        {"label": "Effective To", "fieldname": "effective_to", "fieldtype": "Date", "width": 110},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]
    data = frappe.get_all(
        "Strategic Goal",
        fields=[
            "code",
            "title",
            "language",
            "owner_employee",
            "effective_from",
            "effective_to",
            "status",
        ],
        order_by="status asc, code asc",
    )
    return columns, data
