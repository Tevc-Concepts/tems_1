from __future__ import annotations
import random
import frappe

CUSTOMER_NAMES = [
    "BlueMart Retail", "AgroFoods Ltd", "Sunrise Traders", "Northern Mining", "Delta Steel", "Prime Cement",
    "Evergreen Farms", "Metro Construction", "Eastern Textiles", "Global Plastics", "FreshHarvest",
    "Unity Superstores", "CargoHub", "ExpressChem", "GreenLife Healthcare", "Oceanic Drinks",
    "Kinetic Energy", "AeroParts", "City Builders", "FarmGate" ]


def seed_customers_and_orders(context, count: int = 20):
    customers = []
    for name in CUSTOMER_NAMES[:count]:
        if not frappe.db.exists("Customer", name):
            c = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": name,
                "customer_group": "All Customer Groups",
                "territory": "All Territories"
            }).insert(ignore_permissions=True)
            customers.append(c.name)
    context.setdefault("customers", []).extend(customers)

    # Orders (custom 'Order' doctype may differ; fallback skip if missing)
    if frappe.db.exists("DocType", "Order"):
        orders = []
        vehicles = context.get("vehicles", [])
        for i in range(count):
            cust = random.choice(customers) if customers else None
            veh = random.choice(vehicles) if vehicles else None
            o = frappe.get_doc({
                "doctype": "Order",
                "customer": cust,
                "vehicle": veh,
                "status": "Open"
            })
            try:
                o.insert(ignore_permissions=True)
                orders.append(o.name)
            except Exception:
                frappe.db.rollback()
        context.setdefault("orders", []).extend(orders)
