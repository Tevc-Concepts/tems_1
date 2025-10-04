import frappe
from tems.tems_people.api import validate_driver_active
from frappe.utils import add_days, nowdate


def test_validate_driver_active_future_and_expired():
    # Create Employee
    if not frappe.db.exists("Employee", {"employee_name": "Test Driver"}):
        emp = frappe.get_doc({"doctype": "Employee", "employee_name": "Test Driver"}).insert(ignore_permissions=True)
    emp_name_raw = frappe.get_value("Employee", {"employee_name": "Test Driver"}, "name")
    emp_name = str(emp_name_raw or "")
    # Active qualification future expiry
    future = add_days(nowdate(), 10)
    if not frappe.db.exists("Driver Qualification", {"employee": emp_name, "expiry_date": future}):
        frappe.get_doc({
            "doctype": "Driver Qualification",
            "employee": emp_name,
            "license_no": "LIC-1",
            "expiry_date": future,
            "status": "Active",
        }).insert(ignore_permissions=True)
    assert validate_driver_active(emp_name) is True
    # Expired qualification
    past = add_days(nowdate(), -10)
    if not frappe.db.exists("Driver Qualification", {"employee": emp_name, "expiry_date": past}):
        frappe.get_doc({
            "doctype": "Driver Qualification",
            "employee": emp_name,
            "license_no": "LIC-OLD",
            "expiry_date": past,
            "status": "Expired",
        }).insert(ignore_permissions=True)
    # Active still because a valid active exists
    assert validate_driver_active(emp_name) is True
