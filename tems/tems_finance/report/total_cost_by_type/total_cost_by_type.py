import frappe


def execute(filters=None):
    columns = [
        {"label": "Cost Type", "fieldname": "cost_type", "fieldtype": "Data"},
        {"label": "Total Amount", "fieldname": "total", "fieldtype": "Currency"},
    ]
    data = frappe.db.sql(
        """
        select cost_type, sum(amount) as total
        from `tabFleet Cost`
        group by cost_type
        order by cost_type
        """,
        as_dict=True,
    )
    return columns, data
