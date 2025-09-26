import frappe

def execute(filters=None):
    columns = [
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle"},
        {"label": "Month", "fieldname": "month", "fieldtype": "Data"},
        {"label": "CO2e (kg)", "fieldname": "co2e_kg", "fieldtype": "Float"},
    ]
    rows = frappe.db.sql(
        """
        select vehicle, date_format(coalesce(modified, now()), '%Y-%m') as month, sum(coalesce(co2e_kg,0)) as co2e_kg
        from `tabEmissions Log`
        group by vehicle, date_format(coalesce(modified, now()), '%Y-%m')
        order by month desc
        """,
        as_dict=True,
    )
    return columns, rows
