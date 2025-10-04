import frappe
from tems.tems_finance.handlers import recalculate_vehicle_profitability
from frappe.utils import nowdate
from frappe.tests.utils import FrappeTestCase


class TestFinanceProfitability(FrappeTestCase):
    def test_profitability_rollup(self):
        # Create Vehicle
        vehicle = frappe.get_doc({
            "doctype": "Vehicle",
            "vehicle_name": "TEST-V1",
            "license_plate": "TEST-V1-PLATE",
            "make": "TestMake",
            "model": "TestModel",
            "last_odometer": 0,
            "uom": "Km",
            "custom_assigned_driver": None,
            "custom_asset_id": None,
        })
        existing = frappe.get_all("Vehicle", filters={"license_plate": "TEST-V1-PLATE"}, pluck="name")
        if existing:
            vname = existing[0]
        else:
            # Bypass mandatory custom fields not essential for profitability logic
            vehicle.insert(ignore_permissions=True, ignore_mandatory=True)
            vname = vehicle.name
        # Insert revenue & cost
        for row in [
            {"type": "Revenue", "amount": 1000},
            {"type": "Cost", "amount": 400},
        ]:
            if not frappe.db.exists("Cost And Revenue Ledger", {"vehicle": vname, "type": row["type"], "amount": row["amount"]}):
                frappe.get_doc({
                    "doctype": "Cost And Revenue Ledger",
                    "vehicle": vname,
                    "type": row["type"],
                    "amount": row["amount"],
                    "date": nowdate(),
                }).insert(ignore_permissions=True)
        dummy = frappe._dict(vehicle=vname)
        recalculate_vehicle_profitability(dummy)
        profitability_raw = frappe.get_value("Vehicle", vname, "custom_profitability") or 0
        try:
            profitability = float(profitability_raw or 0)  # type: ignore[arg-type]
        except Exception:
            profitability = 0.0
        self.assertEqual(round(profitability, 2), 600)
