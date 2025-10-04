from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import nowdate


class TestFinanceSafetyIntegration(FrappeTestCase):
    def test_journey_and_profitability_interplay(self):
        # Setup minimal vehicle
        if not frappe.db.exists("Vehicle", {"license_plate": "INT-PLATE"}):
            v = frappe.get_doc({
                "doctype": "Vehicle",
                "license_plate": "INT-PLATE",
                "vehicle_name": "INT-VEH",
                "make": "Make",
                "model": "Model",
                "last_odometer": 0,
                "uom": "Km",
            })
            v.insert(ignore_permissions=True, ignore_mandatory=True)
        vehicle_name = frappe.get_all("Vehicle", filters={"license_plate": "INT-PLATE"}, pluck="name")[0]

        # Create cost & revenue ledger entries
        for row in [
            {"type": "Revenue", "amount": 500},
            {"type": "Cost", "amount": 200},
        ]:
            if not frappe.db.exists("Cost And Revenue Ledger", {"vehicle": vehicle_name, "type": row["type"], "amount": row["amount"]}):
                frappe.get_doc({
                    "doctype": "Cost And Revenue Ledger",
                    "vehicle": vehicle_name,
                    "type": row["type"],
                    "amount": row["amount"],
                    "date": nowdate(),
                }).insert(ignore_permissions=True)

        # Recompute profitability
        from tems.tems_finance.tasks import update_vehicle_profitability
        update_vehicle_profitability()
        raw_net = frappe.get_value("Vehicle", vehicle_name, "custom_profitability") or 0
        try:
            net_val = float(raw_net)  # type: ignore[arg-type]
        except Exception:
            net_val = 0.0
        self.assertEqual(round(net_val, 2), 300.00)

        # Prepare driver & qualification valid (create deterministically)
        emp_list = frappe.get_all("Employee", filters={"employee_name": "Int Driver"}, pluck="name")
        if not emp_list:
            e = frappe.get_doc({
                "doctype": "Employee",
                "employee_name": "Int Driver",
                "first_name": "Int",
                "gender": "Male",
                "status": "Active",
                "date_of_birth": "1990-01-01",
                "date_of_joining": nowdate(),
            })
            try:
                e.insert(ignore_permissions=True)
            except Exception:
                e.insert(ignore_permissions=True, ignore_mandatory=True)
            emp_list = [e.name]
        emp = emp_list[0]
        if not frappe.db.exists("Driver Qualification", {"employee": emp}):
            frappe.get_doc({
                "doctype": "Driver Qualification",
                "employee": emp,
                "license_no": "INT-123",
                "expiry_date": nowdate(),  # today counts as non-expired per validator (>= today ok)
                "status": "Active",
            }).insert(ignore_permissions=True)

        # Create Journey Plan (should succeed)
        jp = frappe.get_doc({
            "doctype": "Journey Plan",
            "driver": emp,
            "route": "R1",
            "start_time": nowdate(),
            "end_time": nowdate(),
        })
        jp.insert(ignore_permissions=True)
        self.assertTrue(jp.name)
