from __future__ import annotations
import random
import frappe
from frappe.utils import add_days, nowdate

FIRST_NAMES = ["John", "Amina", "Chidi", "Grace", "Ibrahim", "Sophia", "Kwame", "Lara", "Tunde", "Fatima", "Omar", "Henry", "Olivia", "Nkechi", "Peter", "Abiola", "Jonas", "Maria", "Elena", "Victor", "Zainab", "Hassan", "Efe", "Samuel", "Anita"]


def seed_employees_and_qualifications(context, count: int = 30, drivers: int = 20):
    employees = []
    driver_qual = []
    company = context.get("company")
    for i in range(count):
        name = f"{random.choice(FIRST_NAMES)} {random.choice(['Okoro','Balogun','Mensah','Adeyemi','Ibrahim','Sule'])}"
        if frappe.db.exists("Employee", {"employee_name": name}):
            continue
        e = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": name,
            "first_name": name.split()[0],
            "gender": random.choice(["Male", "Female"]),
            "date_of_birth": nowdate(),
            "date_of_joining": nowdate(),
            "status": "Active",
            "company": company if frappe.db.has_column("Employee", "company") else None,
        }).insert(ignore_permissions=True)
        employees.append(e.name)
    context.setdefault("employees", []).extend(employees)

    # Mark subset as drivers
    drivers_list = employees[:drivers]
    for d in drivers_list:
        # create qualification with future expiry
        qual = frappe.get_doc({
            "doctype": "Driver Qualification",
            "employee": d,
            "license_no": f"LIC-{random.randint(10000,99999)}",
            "expiry_date": add_days(nowdate(), random.randint(30, 400)),
            "status": "Active"
        })
        try:
            qual.insert(ignore_permissions=True)
            driver_qual.append(qual.name)
        except Exception:
            frappe.db.rollback()
    context.setdefault("driver_qualifications", []).extend(driver_qual)
