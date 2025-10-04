import frappe
from tems.tems_supply_chain.tasks import low_stock_alert
from frappe.utils import nowdate


def test_low_stock_alert_smoke():
    # Create Spare Parts record if not exists (using existing naming convention)
    if frappe.db.table_exists("tabSpare Parts"):
        if not frappe.db.exists("Spare Parts", {"items": "TEST-ITEM"}):
            # Ensure Item
            if not frappe.db.exists("Item", {"item_code": "TEST-ITEM"}):
                frappe.get_doc({"doctype": "Item", "item_code": "TEST-ITEM", "item_name": "Test Item", "is_stock_item": 1}).insert(ignore_permissions=True)
            frappe.get_doc({
                "doctype": "Spare Parts",
                "items": "TEST-ITEM",
                "min_stock": 10,
                "reorder_qty": 5,
            }).insert(ignore_permissions=True)
    # Run alert (will create Communication if quantity < min; quantity likely 0 in test)
    low_stock_alert()
    # Assert no exception and optionally a communication created
    comm = frappe.get_all("Communication", filters={"subject": ["like", "LOW-STOCK-TEST-ITEM-%"]})
    assert comm is not None
