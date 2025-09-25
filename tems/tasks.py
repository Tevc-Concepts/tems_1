import frappe


def daily_sync_checkpoint():
    frappe.logger().info("TEMS.daily_sync_checkpoint ran")


def daily_interest_compute():
    frappe.logger().info("TEMS.daily_interest_compute ran")


def compute_nightly_jobs():
    frappe.logger().info("TEMS.compute_nightly_jobs ran")
