import frappe


def after_insert(doc, method=None):
    """Hook for Asset after_insert to create related TEMS records (stub)."""
    frappe.logger().info("TEMS.assets.after_insert for %s", getattr(doc, 'name', 'unknown'))
