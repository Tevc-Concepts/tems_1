import frappe
from frappe.utils import nowdate

def test_basic_insert_asset_utilization_log():
    """Insert a minimal utilization log and verify validation passes."""
    existing_asset = None
    assets = frappe.get_all("Asset", fields=["name"], limit_page_length=1)
    if assets:
        existing_asset = assets[0].name

    log = frappe.get_doc({
        "doctype": "Asset Utilization Log",
        "asset": existing_asset,
        "utilization_hours": 2,
        "log_date": nowdate()
    })
    log.insert()
    assert log.name
