from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPermissions(FrappeTestCase):
    def setUp(self):
        # Ensure Driver role exists and test user
        if not frappe.db.exists("Role", "Driver"):
            frappe.get_doc({"doctype": "Role", "role_name": "Driver"}).insert(ignore_permissions=True)
        if not frappe.db.exists("User", "driver_perm@test.local"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "driver_perm@test.local",
                "first_name": "Driver",
                "roles": [{"role": "Driver"}],
            })
            user.insert(ignore_permissions=True)
        self.user = "driver_perm@test.local"

    def test_driver_cannot_create_asset(self):
        from frappe import set_user
        # Ensure prerequisite Company and Asset Category exist
        company_list = frappe.get_all("Company", pluck="name", limit=1)
        if not company_list:
            try:
                frappe.get_doc({
                    "doctype": "Company",
                    "company_name": "_Perm Test Company",
                    "default_currency": "USD",
                    "country": "United States",
                }).insert(ignore_permissions=True, ignore_mandatory=True)
            except Exception:
                pass
        if not frappe.get_all("Asset Category", pluck="name"):
            try:
                frappe.get_doc({
                    "doctype": "Asset Category",
                    "asset_category_name": "Test Fleet Cat",
                }).insert(ignore_permissions=True, ignore_mandatory=True)
            except Exception:
                pass
        asset_cat = frappe.get_all("Asset Category", pluck="name", limit=1)[0]
        set_user(self.user)
        try:
            with self.assertRaises(frappe.PermissionError):
                frappe.get_doc({
                    "doctype": "Asset",
                    "asset_name": "TEST-DRIVER-ASSET",
                    "asset_category": asset_cat,
                    "company": frappe.get_all("Company", pluck="name", limit=1)[0],
                }).insert()
        finally:
            set_user("Administrator")
