import frappe

def execute(filters=None):
    columns = [
        {"label": "Journey Plan", "fieldname": "journey_plan", "fieldtype": "Link", "options": "Journey Plan"},
        {"label": "Border Post", "fieldname": "border_post", "fieldtype": "Data"},
        {"label": "Arrival", "fieldname": "arrival_time", "fieldtype": "Datetime"},
        {"label": "Departure", "fieldname": "departure_time", "fieldtype": "Datetime"},
        {"label": "Wait (mins)", "fieldname": "wait_duration", "fieldtype": "Int"},
    ]
    data = frappe.get_all(
        "Border Crossing",
        fields=["journey_plan", "border_post", "arrival_time", "departure_time", "wait_duration"],
        order_by="arrival_time desc",
    )
    return columns, data
