import frappe
from frappe.utils import now_datetime

def execute():
    # Seed minimal sample records to make workspace usable
    if not frappe.db.exists("Dispatch Schedule", {"date": [">=", now_datetime().date().strftime("%Y-%m-%d")] } ):
        ds = frappe.get_doc({
            "doctype": "Dispatch Schedule",
            "date": now_datetime().date(),
            "route": "Main Corridor",
            "shift": "Morning",
            # dispatcher is optional; skip linking to Employee unless one is present
            "planned_departures": [
                {"departure_time": "08:00:00"},
                {"departure_time": "08:30:00"}
            ]
        })
        ds.insert(ignore_if_duplicate=True)

    # Duty Assignment example
    if not frappe.db.exists("Duty Assignment", {"status": "Planned"}):
        frappe.get_doc({
            "doctype": "Duty Assignment",
            "driver": None,
            "schedule_slot": now_datetime(),
            "status": "Planned"
        }).insert(ignore_if_duplicate=True)
