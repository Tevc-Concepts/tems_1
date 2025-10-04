from __future__ import annotations
import frappe


def execute(filters=None):
    columns = [
        {"label": "Asset", "fieldname": "asset", "fieldtype": "Link", "options": "Asset", "width": 150},
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "Cost Type", "fieldname": "cost_type", "fieldtype": "Data", "width": 120},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
    ]
    # Gather cost entries referencing asset via Cost And Revenue Ledger asset field
    rows = frappe.db.sql(
        """
        select asset, vehicle, type as cost_type, amount
        from `tabCost And Revenue Ledger`
        where asset is not null and type='Cost'
        """,
        as_dict=True,
    )
    return columns, rows
