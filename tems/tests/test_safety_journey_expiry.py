from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, nowdate


class TestJourneyDriverExpiry(FrappeTestCase):
    def setUp(self):  # noqa: D401
        # Ensure an active Employee exists
        existing = frappe.get_all("Employee", filters={"employee_name": "Test Driver Exp"}, pluck="name")
        if existing:
            self.employee = existing[0]
            return
        # Ensure a company exists
        companies = frappe.get_all("Company", pluck="name", limit=1)
        if not companies:
            comp = frappe.get_doc({
                "doctype": "Company",
                "company_name": "_Test Company",
                "default_currency": "USD",
                "country": "United States",
            })
            comp.insert(ignore_permissions=True, ignore_mandatory=True)
            company_name = comp.name
        else:
            company_name = companies[0]
        emp = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": "Test Driver Exp",
            "first_name": "Test",
            "last_name": "Driver",
            "gender": "Male",
            "status": "Active",
            "company": company_name,
            "date_of_birth": "1990-01-01",
            "date_of_joining": nowdate(),
        })
        try:
            emp.insert(ignore_permissions=True)
        except Exception:
            # Fallback ignoring mandatory (some HRMS fields vary by configuration)
            emp.insert(ignore_permissions=True, ignore_mandatory=True)
        self.employee = emp.name

    def _ensure_qualification(self, days_offset: int):
        # days_offset < 0 => expired
        expiry = add_days(nowdate(), days_offset)
        if not frappe.db.exists("Driver Qualification", {"employee": self.employee}):
            frappe.get_doc({
                "doctype": "Driver Qualification",
                "employee": self.employee,
                # Some configs expect either license_no or license_number; include both for safety
                "license_no": "X123",
                "license_number": "X123",
                "expiry_date": expiry,
                # Use allowed status; treat future as Active, past as Expired
                "status": "Active" if days_offset >= 0 else "Expired",
            }).insert(ignore_permissions=True)
        else:
            qname = frappe.get_all("Driver Qualification", filters={"employee": self.employee}, pluck="name")[0]
            frappe.db.set_value("Driver Qualification", qname, {
                "expiry_date": expiry,
                "status": "Active" if days_offset >= 0 else "Expired"
            })

    def test_journey_rejected_if_driver_qualification_expired(self):
        self._ensure_qualification(-5)  # expired 5 days ago
        jp = frappe.get_doc({
            "doctype": "Journey Plan",
            "driver": self.employee,
            "route": "TEST",
            "start_time": nowdate(),
            "end_time": nowdate(),
        })
        with self.assertRaises(frappe.ValidationError):
            jp.insert(ignore_permissions=True)

    def test_journey_allowed_if_driver_qualification_valid(self):
        self._ensure_qualification(10)  # valid in future
        jp = frappe.get_doc({
            "doctype": "Journey Plan",
            "driver": self.employee,
            "route": "TEST",
            "start_time": nowdate(),
            "end_time": nowdate(),
        })
        # Should not raise
        jp.insert(ignore_permissions=True)
        self.assertTrue(jp.name)
