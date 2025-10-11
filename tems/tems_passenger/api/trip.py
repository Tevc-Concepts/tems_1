import frappe


@frappe.whitelist()
def create_trip(operation_plan: str, vehicle: str, route: str = "", departure_time: str | None = None, seat_capacity: int | None = None):
    doc = frappe.get_doc({
        "doctype": "Passenger Trip",
        "operation_plan": operation_plan,
        "vehicle": vehicle,
        "route": route,
        "departure_time": departure_time,
        "seat_capacity": seat_capacity,
    })
    doc.insert(ignore_permissions=True)
    return doc.name
