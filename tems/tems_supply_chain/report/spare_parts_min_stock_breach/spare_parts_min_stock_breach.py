import frappe


def execute(filters=None):
    columns = [
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item"},
        {"label": "Min Stock", "fieldname": "min_stock", "fieldtype": "Float"},
        {"label": "Available Qty", "fieldname": "qty", "fieldtype": "Float"},
    ]
    # If an Item has a stock_qty field in Item default warehouse, we may join; otherwise, leave data empty
    if frappe.db.table_exists("Item") and frappe.db.table_exists("Spare Part"):
        # Try to fetch qty from Bin table if exists
        if frappe.db.table_exists("Bin"):
            data = frappe.db.sql(
                """
                select sp.item, sp.min_stock,
                       coalesce(sum(b.actual_qty), 0) as qty
                from `tabSpare Part` sp
                left join `tabBin` b on b.item_code = sp.item
                group by sp.item, sp.min_stock
                having qty < coalesce(sp.min_stock, 0)
                order by sp.item
                """,
                as_dict=True,
            )
        else:
            data = []
    else:
        data = []
    return columns, data
