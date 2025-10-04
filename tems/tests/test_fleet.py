import frappe
from frappe.utils import nowdate

def test_tems_asset_utilization_log_minimal():
    """Ensure custom utilization log can be created linking to existing Asset if available or skips gracefully."""
    # Find any existing Asset (core ERPNext) for linking
    asset_name = None
    assets = frappe.get_all("Asset", fields=["name"], limit_page_length=1)
    if assets:
        asset_name = assets[0].name
    log = frappe.get_doc({
        "doctype": "Asset Utilization Log",
        "asset": asset_name,
        "vehicle": None,
        "utilization_hours": 1,
        "log_date": nowdate()
    })
    log.insert()
    assert log.name

def test_maintenance_work_order_core_fields():
    """Verify Maintenance Work Order basic insert (uses vehicle link only)."""
    wo = frappe.get_doc({
        "doctype": "Maintenance Work Order",
        "vehicle": None,
        "status": "Open"
    })
    wo.insert()
    wo.reload()
    assert hasattr(wo, "status")


def test_predictive_maintenance_generation():
    """If an Asset exists with utilization near interval, predictive task should create a Work Order (asset link)."""
    assets = frappe.get_all("Asset", fields=["name"], limit=1)
    if not assets:
        return  # skip if no asset in test DB
    asset = assets[0].name
    # Set interval and utilization (simulate 92%)
    frappe.db.set_value("Asset", asset, {
        "maintenance_interval_hours": 100,
        "total_utilization_hours": 92,
    })
    frappe.db.commit()
    frappe.get_attr('tems.tems_fleet.tasks.compute_predictive_maintenance')()
    wo = frappe.get_all("Maintenance Work Order", filters={"asset": asset, "status": ["in", ["Open", "In Progress"]]}, limit=1)
    if assets:  # only assert if asset present
        assert wo, "Predictive maintenance did not create a Maintenance Work Order"


def test_asset_utilization_rollup():
    assets = frappe.get_all("Asset", fields=["name"], limit=1)
    if not assets:
        return
    asset = assets[0].name
    before = frappe.db.get_value("Asset", asset, "total_utilization_hours") or 0
    log = frappe.get_doc({
        "doctype": "Asset Utilization Log",
        "asset": asset,
        "utilization_hours": 3,
        "log_date": nowdate()
    })
    log.insert()
    after = frappe.db.get_value("Asset", asset, "total_utilization_hours") or 0
    assert after >= before + 3 - 0.0001
