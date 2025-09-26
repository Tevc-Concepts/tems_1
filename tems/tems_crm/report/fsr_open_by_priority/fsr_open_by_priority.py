import frappe


def execute(filters=None):
    columns = [
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data"},
        {"label": "Open Count", "fieldname": "open_count", "fieldtype": "Int"},
    ]
    data = frappe.db.sql(
        """
        select priority, count(*) as open_count
        from `tabField Service Request`
        where status = 'Open'
        group by priority
        order by priority
        """,
        as_dict=True,
    )
    return columns, data
