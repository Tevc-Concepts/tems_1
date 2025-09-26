import frappe


def execute(filters=None):
    columns = [
        {"label": "Context", "fieldname": "context", "fieldtype": "Data"},
        {"label": "Count", "fieldname": "count", "fieldtype": "Int"},
    ]
    data = frappe.db.sql(
        """
        select context, count(*) as count
        from `tabDocument Checklist`
        group by context
        order by context
        """,
        as_dict=True,
    )
    return columns, data
